from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import sys
import requests

# 3/3 tests written
def normalize_url(url):
    # remove protocol/scheme
    parsed = urlparse(url)

    # concat the netloc and the path
    normalized = parsed.netloc + parsed.path

    if url == "":
        return False
    else:
        return normalized.lower()

# 2/3 tests written
def get_h1_from_html(html):
    # return the text from h1, then make the bs4 object into a str
    data = BeautifulSoup(html, 'html.parser')
    h1 = data.h1.string
    return h1


def get_first_paragraph_from_html(html):
    data = BeautifulSoup(html, "html.parser")
    actual = data.find("p").get_text()
    return actual

# return an un-normalized list of all the URLs found within the HTML
def get_urls_from_html(html, base_url):
    # TODO: handle relative links -- write a unittest `test_get_urls_from_html_relative`
    data = BeautifulSoup(html, "html.parser")
    links = []
    # use urljoin
    for link in data.find_all('a'): # find all anchor tags in the soup
        links.append(urljoin(base_url, link.get('href'))) # append the link's href attr to the list
    return links # return the list of links in href tags

def get_images_from_html(html, base_url):
    data = BeautifulSoup(html, "html.parser") # get a bs4 object of the HTML tree
    links = [] # bs4 returns an array of links
    for link in data.find_all("img"): # find all the image tags
        links.append(base_url + link.get("src")) # grab the src attribute (rel path)
    return links

# 1/3 tests written
def extract_page_data(html, page_url):
    soup = BeautifulSoup(html, "html.parser")

    data = {
        "url": page_url,
        "h1": get_h1_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html, page_url),
        "image_urls": get_images_from_html(html, page_url),
    }

    return data

# try this on https://wagslane.dev
def get_html(url):
    resp = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})

    # status code handling
    if resp.status_code >= 400 and resp.status_code < 500:
        print(f"Error 4xx: {resp.status_code}")
        sys.exit(1)
    elif not resp.headers.get('Content-Type').startswith('text/html'):
        # if Content-Type is NOT text/html
        print(f"Error: Content-Type not text/html")
        print(f"Content-Type is: {resp.headers.get('Content-Type')}")
        sys.exit(1)
    elif resp.status_code > 300:
        print(f"Error: {resp.status_code}")
        sys.exit(1)
    else:
        # print the HTML, exit.
        print(resp.text)
        sys.exit(0)

def crawl_page(base_url, current_url=None, page_data=None):
    # grab the domains
    base_domain = urlparse(base_url).netloc
    if current_url == None: # initial run
        current_domain = base_domain
    else:
        # set current_domain to network location (domain)
        current_domain = urlparse(current_url).netloc

    print(f"Base domain: {base_domain}")
    print(f"Current domain: {current_domain}")

    # check domain is from base_url. if not, return.
    if current_domain != base_domain:
        print("Domain mismatch. Stop crawling.")
        return

    # get normalized current_url
    current_url_normalized = normalize_url(current_url)

    # check if page has already been crawled

    # Get the HTML from the current URL

    # if above get_html succeeds, use extract_page_data() and add to the `page_data` dict.
    
    # get all URLs from response body obj

    # recursively crawl each page returned from get_all_urls()

### COMMAND LINE STUFF ###
def main():
    if __name__ == "__main__":
        if len(sys.argv) < 2:
            print("no website provided")
            sys.exit(1)
        elif len(sys.argv) > 2:
            print("too many arguments provided")
            sys.exit(1)
        else:
            print(f"starting crawl of: {sys.argv[1]}")
            crawl_page(sys.argv[1])

main()