from urllib.parse import urlparse
from bs4 import BeautifulSoup

def normalize_url(url):
    # remove protocol/scheme
    parsed = urlparse(url)
    print(parsed)

    # concat the netloc and the path
    normalized = parsed.netloc + parsed.path
    return normalized



# EACH FN NEEDS 3 TEST CASES MINIMUM
def get_h1_from_html(html):
    # return the text from h1
    data = BeautifulSoup(html, 'html.parser')
    h1 = data.h1()
    return h1


def get_first_paragraph_from_html(html):
    pass
