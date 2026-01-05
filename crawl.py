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
    soup = BeautifulSoup(html, "html.parser")
    first_p = soup.find("p")
    return first_p.get_text() if first_p else None
    
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
        return resp.text
        sys.exit(0)

def crawl_page(base_url, current_url=None, page_data=None):
    # instantiate data stores
    if current_url == None:
        current_url = base_url
    if page_data == None:
        page_data = {}

    # get url objects
    # if path doesn't match, return empty dict
    base_url_obj = urlparse(base_url)
    current_url_obj = urlparse(current_url)
    if current_url_obj.netloc != base_url_obj.netloc:
        return page_data

    # normalize the url
    # if it's already in the dict, return it (go next)
    normalized_url = normalize_url(current_url)
    if normalized_url in page_data:
        return page_data

    # start crawling the page
    # if it's empty, return empty dict page_data
    print(f"Crawling {current_url}")
    html = get_html(current_url)
    if html == None:
        return page_data

    # nest the page's metadata inside of the main dict that stores all the urls
    page_info = extract_page_data(html, current_url) 
    page_data[normalized_url] = page_info

    # 
    next_urls = get_urls_from_html(html, base_url)
    for next_url in next_urls:
        page_data = crawl_page(base_url, next_url, page_data) # recursion!

    return page_data

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
