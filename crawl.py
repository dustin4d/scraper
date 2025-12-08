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


# EACH FN NEEDS 3 TEST CASES MINIMUM
def get_h1_from_html(html):
    # return the text from h1
    data = BeautifulSoup(html, 'html.parser')
    h1 = data.h1()
    return h1


def get_first_paragraph_from_html(html):
    pass
