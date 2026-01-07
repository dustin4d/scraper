import unittest     # import python's unit testing framework
from main import ( 
    normalize_url,
    get_h1_from_html,
    get_first_paragraph_from_html,
    get_urls_from_html,
    get_images_from_html,
    extract_page_data,
    main,
    AsyncCrawler
)

class TestCrawl(unittest.TestCase): # create test obj, inherit from `unittest`'s TestCase obj
    # uses the `normalize_url()` fn to test an input URL against a normalized URL `expected`
    def test_normalize_url(self): 
        input_url = "https://blog.boot.dev/path"
        actual = normalize_url(input_url) # where the magic happens
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected) # tests whether input given is the same as the normalized URL

    # lowercase all input
    def test_normalize_url_caps(self):
        input_url = "https://blog.boot.DEV/path"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    # if input is empty
    def test_normalize_url_empty(self):
        input_url = ""
        actual = normalize_url(input_url)
        expected = False
        self.assertEqual(actual, expected)

    def test_get_h1_from_html(self):
        input_body = '<html><body><h1>Test Title</h1></body></html>'
        h1 = get_h1_from_html(input_body) # returns the h1 from html input
        expected = "Test Title"
        self.assertEqual(h1, expected) # Test 1, string match

    def test_get_h1_from_html_present(self):
        input_body = '<html><body><h1></h1></body></html>'
        actual = get_h1_from_html(input_body)
        expected = None
        self.assertEqual(actual, expected)

    def test_get_h1_from_html_balls(self):
        pass

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

# Get URLs
    def test_get_urls_from_html_absolute(self):
        input_url = "https://blog.boot.dev" # dummy data
        input_body = '<html><body><a href="https://blog.boot.dev"><span>Boot.dev</span></a></body></html>' # dummy data
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev"]
        self.assertEqual(actual, expected)

    # does each link use https
    # TODO: finish re-writing this
    def test_get_urls_from_html_relative(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><a href="/post1"></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/post1"]
        self.assertEqual(actual, expected)

    # is the url from a known site
    def test_get_urls_from_html_known_ai(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><a href="/post1"></body></html>' 
        actual = get_urls_from_html(input_body, input_url)
        known_ai = ['https://chatgpt.com/', 'https://claude.ai/', 'https://grok.com/', "https://gemini.com", ]
        for link in known_ai:
            self.assertTrue(
                link in known_ai
            )
# Get Images
    def test_get_images_from_html_relative(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_amount(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = 1
        self.assertEqual(len(actual), expected)

    def test_get_images_from_html_filetype(self): # test for certain filetypes only
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = {".png", ".jpg", ".jpeg"} # whitelist of filetypes as a set(), so we don't get duplicates

        for file in actual: # for every filetype returned
            self.assertTrue( # return true/false if
                file.endswith(tuple(expected)) # filetype ends with any of the extensions allowed
                # ^ this call to tuple() reads in the `expected` set as a tuple by default
            )

#    def test_get_all_links(self):
#        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
#        actual = get_urls_from_html(input_body, None)
#        expected = ["https://chatgpt.com/", "https://claude.ai/", "https://grok.com/", ]
#        self.assertEqual(actual, expected)


    # use all functions from above to load page data into a dict
    def test_extract_page_data_basic(self):
        input_url = "https://blog.boot.dev"
        input_body = '''<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
            </body></html>
            '''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://blog.boot.dev",
            "h1": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://blog.boot.dev/link1"],
            "image_urls": ["https://blog.boot.dev/image1.jpg"]
        }
        self.assertEqual(actual, expected)

    # create test fn for AsyncCrawler's base_domain variable
    # TODO: handle country code domains
    def test_AsyncCrawler_base_domain(self):
        test_cases = [
            ("https://example.com/poop/shit/fuck", "example.com"),
            ("http://example.com", "example.com"),
            ("https://www.github.com/explore", "github.com"),
            #("http://subdomain.example.co.uk/path", "example.co.uk"),
            ("https://localhost:8000/dashboard", "localhost"),
            ("http://deep.nested.site.org", "site.org"),
        ]

        for url, expected in test_cases: # loop over the tuples in test_cases
            with self.subTest(url=url): # unittest's context manager for testing in a loop
                crawler = AsyncCrawler(base_url=url) # instantiate the AsyncCrawler class, provide the base_url from tests
                self.assertEqual(crawler.base_domain, expected) # test the base_domain == expected

    def test_AsyncCrawler_page_data_init(self):
        # test to check if page_data is initialized as empty
        crawler = AsyncCrawler("https://example.com/poop/shit/fuck")

       # Check type and initial state
        self.assertIsInstance(crawler.page_data, dict)
        self.assertEqual(len(crawler.page_data), 0)
        self.assertEqual(crawler.page_data, {})


    def test_AsyncCrawler_page_data_info(self):
        crawler = AsyncCrawler("https://example.com/")

        test_cases = {
            # url                   # info
            "https://example.com/": {"status_code": 200, "title": "Home"},
            "https://example.com/blog": {"status_code": 200, "title": "Blog"},
            "https://example.com/404": {"status_code": 404, "title": "Not Found"},
        }

        # add data to the test's crawler object
        # loop through, grab the URL and the info. create a key of url and value of info
        for url, info in test_cases.items():
            crawler.page_data[url] = info

        # test multiple cases
        for url, expected in test_cases.items():
            with self.subTest(url=url):
                self.assertIn(url, crawler.page_data)
                self.assertEqual(crawler.page_data[url]["status_code"], expected["status_code"])
                self.assertEqual(crawler.page_data[url]["title"], expected["title"])
        
if __name__ == "__main__":
    unittest.main()
