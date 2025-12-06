from urllib.parse import urlparse

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
