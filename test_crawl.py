import unittest     # import python's unit testing framework
from crawl import ( # import functions from `crawl.py`
    normalize_url,
    get_h1_from_html,
    get_first_paragraph_from_html,
    get_urls_from_html,
    get_images_from_html,
)

dummy_html = """
        <html>
            <body>
                <main>
                    <a href="https://chatgpt.com/">ChatGPT</a>
                    <img src="chatgpt.jpg">
                    <a href="https://claude.ai/">Claude</a>
                    <img src="claude.jpg">
                    <a href="https://grok.com/">Grok</a>
                    <img src="grok.jpg">
                </main>
            </body>
        </html>
        """

class TestCrawl(unittest.TestCase): # create test obj, inherit from `unittest`'s TestCase obj
    # uses the `normalize_url()` fn to test an input URL against a normalized URL `expected`
    def test_normalize_url(self): 
        input_url = "https://blog.boot.dev/path"
        actual = normalize_url(input_url) # where the magic happens
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected) # tests whether input given is the same as the normalized URL

    def test_get_h1_from_html(self):
        input_body = '<html><body><h1>Test Title</h1></body></html>'
        h1 = get_h1_from_html(input_body) # returns the h1 from html input
        expected = "Test Title"
        self.assertEqual(h1, expected) # Test 1, string match

    def test_get_first_paragraph_from_html(self):
        input_body = """
        <html>
            <body>
                <p>Outside paragraph.</p>
                <main>
                    <p>Main paragraph.</p>
                </main>
            </body>
        </html>
        """
        data = get_first_paragraph_from_html(input_body)
        expected = "Outside paragraph."
        self.assertEqual(data, expected)

# TODO: run unit tests on `get_urls_from_*` and `get_images_from_*`

# Get URLs
    def test_get_urls_from_html_absolute(self):
        input_url = "https://blog.boot.dev" # dummy data
        input_body = '<html><body><a href="https://blog.boot.dev"><span>Boot.dev</span></a></body></html>' # dummy data
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev"]
        self.assertEqual(actual, expected)

    # does each link use https
    def test_get_urls_from_html_https(self):
        input_url = "https://agents.llms.com"
        input_body = dummy_html
        actual = get_urls_from_html(input_body, input_url)
        expected = True

        # if any links don't have https, test fails
        for link in actual:
            self.assertEqual(link.startswith("https://"), expected)

# Get Images
    def test_get_images_from_html_relative(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_all_links(self):
        input_body = dummy_html
        actual = get_urls_from_html(input_body, None)
        expected = ["https://chatgpt.com/", "https://claude.ai/", "https://grok.com/", ]
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
