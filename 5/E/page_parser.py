from html.parser import HTMLParser
from urllib.request import urlopen
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup


def is_internal(url, ref):
    return (urlparse(ref).netloc == urlparse(url).netloc and
            urlparse(ref).scheme == urlparse(url).scheme)


def parse_url(url, graph):
    graph[url] = set()
    page = BeautifulSoup(urlopen(url), "lxml")
    for ref in page.find_all('a'):
        child = urljoin(url, ref.get('href'))
        if is_internal(url, child):
            try:
                with urlopen(child):
                    graph[url].add(urljoin(url, child))
            except:
                pass


def parse_site(site, graph, depth=100, verbose=False):
    queue = [(site, 0)]
    parsed = set()
    current_site_index = 0
    while current_site_index < len(queue):
        url, d = queue[current_site_index]
        if d >= depth:
            break
        current_site_index += 1
        parsed.add(url)
        if verbose:
            print('parsing %s' % url)
        parse_url(url, graph)
        for ref in graph[url]:
            if ref not in parsed:
                queue.append((ref, d + 1))
                parsed.add(ref)
