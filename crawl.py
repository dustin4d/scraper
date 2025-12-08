from urllib.parse import urlparse
from bs4 import BeautifulSoup

def normalize_url(url):
    print("### DEBUG normalize_url() ###")
    # remove protocol/scheme
    print(f"Input URL: {url}")
    parsed = urlparse(url)
    print(parsed)

    # concat the netloc and the path
    normalized = parsed.netloc + parsed.path
    print(f"NORMALIZED URL: {normalized}")
    return normalized

    print("### END DEBUG ###")

def get_h1_from_html(html):
    pass

def get_first_paragraph_from_html(html):
    pass
