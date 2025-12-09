from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

def normalize_url(url):
    # remove protocol/scheme
    parsed = urlparse(url)

    # concat the netloc and the path
    normalized = parsed.netloc + parsed.path
    return normalized



def get_h1_from_html(html):
    # return the text from h1
    data = BeautifulSoup(html, 'html.parser')
    h1 = data.h1.string
    return h1


def get_first_paragraph_from_html(html):
    data = BeautifulSoup(html, "html.parser")
    actual = data.find("p").get_text()
    return actual

# return an un-normalized list of all the URLs found within the HTML
def get_urls_from_html(html, base_url):
    data = BeautifulSoup(html, "html.parser")
    links = []
    for link in data.find_all('a'): # find all anchor tags in the soup
        links.append(link.get('href')) # append the link's href attr to the list

    return links # return the list
