import unittest     # import python's unit testing framework
from crawl import normalize_url     # import this function from `crawl.py`

class TestCrawl(unittest.TestCase): # create test obj, inherit from `unittest`'s TestCase obj
    # uses the `normalize_url()` fn to test an input URL against a normalized URL `expected`
    def test_normalize_url(self): 
        input_url = "https://blog.boot.dev/path"
        actual = normalize_url(input_url) # where the magic happens
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected) # tests whether input given is the same as the normalized URL

    def test_get_h1_from_html(html):
        pass

    def test_get_first_paragraph_from_html(html):
        pass

if __name__ == "__main__":
    unittest.main()
