import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def get_link_inner_urls(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = set()
    base_domain = urlparse(url).netloc

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        full_url = urljoin(url, href)
        parsed_url = urlparse(full_url)

        if parsed_url.netloc == base_domain and not parsed_url.fragment:
            links.add(full_url)

    return list(links)
