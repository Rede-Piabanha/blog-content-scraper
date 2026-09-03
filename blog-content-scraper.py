#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path
from urllib.parse import urlparse, urlunparse

import requests
from bs4 import BeautifulSoup

DEFAULT_OUTPUT = "posts_titulos_e_textos.txt"
DEFAULT_TIMEOUT = 10.0
POSTS_ENDPOINT = "/wp-json/wp/v2/posts"
USER_AGENT = "BlogContentScraper/1.0 (+https://piabanha.net/)"


class ScraperError(RuntimeError):
    """Raised when the scraper cannot complete a request or parse a response."""


def normalize_api_url(url):
    """Return a WordPress posts REST endpoint from a site URL or endpoint URL."""
    raw_url = url.strip()
    parsed = urlparse(raw_url)

    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("Informe uma URL HTTP ou HTTPS válida.")

    path = parsed.path.rstrip("/")
    if path.endswith(POSTS_ENDPOINT):
        endpoint_path = path
    else:
        endpoint_path = f"{path}{POSTS_ENDPOINT}"

    return urlunparse((parsed.scheme, parsed.netloc, endpoint_path, "", "", ""))


def html_to_text(value, separator="\n"):
    """Convert rendered WordPress HTML to clean text."""
    if not value:
        return ""
    return BeautifulSoup(value, "html.parser").get_text(separator, strip=True)


def _is_invalid_page_response(response):
    if response.status_code != 400:
        return False

    try:
        payload = response.json()
    except ValueError:
        return False

    return (
        isinstance(payload, dict)
        and payload.get("code") == "rest_post_invalid_page_number"
    )


def get_all_posts_content(api_url, timeout=DEFAULT_TIMEOUT):
    """Fetch all public WordPress posts and return cleaned title/content strings."""
    posts_content = []
    page = 1
    total_pages = None

    with requests.Session() as session:
        session.headers.update({"User-Agent": USER_AGENT})

        while True:
            try:
                response = session.get(
                    api_url,
                    params={
                        "page": page,
                        "per_page": 100,
                        "_fields": "title,content,link",
                    },
                    timeout=timeout,
                )
            except requests.RequestException as exc:
                raise ScraperError(
                    f"Erro ao acessar a API na página {page}: {exc}"
                ) from exc

            if page > 1 and _is_invalid_page_response(response):
                break

            try:
                response.raise_for_status()
            except requests.HTTPError as exc:
                raise ScraperError(
                    f"Erro HTTP na página {page}: {response.status_code}"
                ) from exc

            try:
                posts = response.json()
            except ValueError as exc:
                raise ScraperError(
                    f"A API retornou JSON inválido na página {page}."
                ) from exc

            if not isinstance(posts, list):
                raise ScraperError(
                    f"Resposta inesperada da API na página {page}."
                )

            if not posts:
                break

            if total_pages is None:
                header_value = response.headers.get("X-WP-TotalPages")
                if header_value:
                    try:
                        total_pages = int(header_value)
                    except ValueError:
                        total_pages = None

            for post in posts:
                title = html_to_text(
                    post.get("title", {}).get("rendered", ""),
                    separator=" ",
                )
                content = html_to_text(
                    post.get("content", {}).get("rendered", "")
                )

                full_text = "\n\n".join(
                    part for part in (title, content) if part
                ).strip()

                if full_text:
                    posts_content.append(full_text)
                else:
                    post_link = post.get("link", "(sem URL)")
                    print(
                        f"Post vazio ignorado: {post_link}",
                        file=sys.stderr,
                    )

            print(
                f"Página {page} processada: {len(posts)} post(s).",
                file=sys.stderr,
            )

            if total_pages is not None and page >= total_pages:
                break

            page += 1

    return posts_content


def write_posts(posts_content, output_path):
    """Write collected posts to a UTF-8 text file."""
    output = Path(output_path).expanduser()
    if output.parent != Path("."):
        output.parent.mkdir(parents=True, exist_ok=True)

    separator = "\n" + "=" * 80 + "\n"

    with output.open("w", encoding="utf-8") as file:
        for index, content in enumerate(posts_content):
            if index:
                file.write(separator)
            file.write(content)
            file.write("\n")

    return output


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description=(
            "Extrai títulos e textos de posts públicos de um site WordPress "
            "usando a REST API nativa."
        )
    )
    parser.add_argument(
        "--url",
        required=True,
        help="URL do site WordPress ou endpoint /wp-json/wp/v2/posts.",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help=f"Arquivo de saída (padrão: {DEFAULT_OUTPUT}).",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help=f"Timeout HTTP em segundos (padrão: {DEFAULT_TIMEOUT:g}).",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    if args.timeout <= 0:
        print("Erro: --timeout deve ser maior que zero.", file=sys.stderr)
        return 2

    try:
        api_url = normalize_api_url(args.url)
        posts_content = get_all_posts_content(
            api_url,
            timeout=args.timeout,
        )
        output = write_posts(posts_content, args.output)
    except (ValueError, ScraperError, OSError) as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 1

    print(
        f"{len(posts_content)} post(s) salvo(s) em '{output}'."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
