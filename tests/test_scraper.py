import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "blog-content-scraper.py"
SPEC = importlib.util.spec_from_file_location("blog_content_scraper", MODULE_PATH)
SCRAPER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SCRAPER)


class NormalizeApiUrlTests(unittest.TestCase):
    def test_site_url_is_converted_to_posts_endpoint(self):
        self.assertEqual(
            SCRAPER.normalize_api_url("https://example.com"),
            "https://example.com/wp-json/wp/v2/posts",
        )

    def test_existing_posts_endpoint_is_preserved(self):
        self.assertEqual(
            SCRAPER.normalize_api_url(
                "https://example.com/wp-json/wp/v2/posts/"
            ),
            "https://example.com/wp-json/wp/v2/posts",
        )

    def test_subdirectory_installation_is_supported(self):
        self.assertEqual(
            SCRAPER.normalize_api_url("https://example.com/blog"),
            "https://example.com/blog/wp-json/wp/v2/posts",
        )

    def test_invalid_url_is_rejected(self):
        with self.assertRaises(ValueError):
            SCRAPER.normalize_api_url("example.com")


class TextConversionTests(unittest.TestCase):
    def test_html_is_converted_to_clean_text(self):
        self.assertEqual(
            SCRAPER.html_to_text("<p>Hello <strong>world</strong></p>"),
            "Hello\nworld",
        )


class OutputTests(unittest.TestCase):
    def test_posts_are_written_with_separator(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "nested" / "posts.txt"
            result = SCRAPER.write_posts(["Post one", "Post two"], output)

            self.assertEqual(result, output)
            content = output.read_text(encoding="utf-8")
            self.assertIn("Post one", content)
            self.assertIn("=" * 80, content)
            self.assertIn("Post two", content)


if __name__ == "__main__":
    unittest.main()
