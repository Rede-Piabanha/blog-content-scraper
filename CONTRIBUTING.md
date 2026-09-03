# Contributing to Blog Content Scraper

Contributions are welcome.

## Guidelines

- Keep pull requests focused and avoid unrelated changes.
- Explain what changed, why it changed, and how it was tested.
- Do not include credentials, API keys, personal data, private URLs, scraped content, or other sensitive information.
- Keep compatibility with Python 3 and avoid unnecessary dependencies.
- Update the README when behavior, arguments, dependencies, output, or supported usage changes.
- Preserve the tool's scope: accessing content available through WordPress REST API endpoints without bypassing authentication or access controls.

## Testing

At minimum, verify that the script compiles:

```sh
python -m py_compile blog-content-scraper.py
```

When changing URL handling, pagination, HTTP behavior, or output generation, add or update automated tests when practical.

## Security issues

Do not report suspected security vulnerabilities in public issues. Follow `SECURITY.md`.

## License

By contributing code or documentation, you agree that your contribution may be distributed under the MIT License used by this repository.
