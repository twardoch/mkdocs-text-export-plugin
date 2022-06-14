import os

from weasyprint import urls
from bs4 import BeautifulSoup

# check if href is relative --
# if it is relative it *should* be an html that generates a text file
def is_doc(href: str):
    tail = os.path.basename(href)
    _, ext = os.path.splitext(tail)

    absurl = urls.url_is_absolute(href)
    abspath = os.path.isabs(href)
    htmlfile = ext.startswith('.html')
    if absurl or abspath or not htmlfile:
        return False

    return True

def rel_txt_href(href: str, file_ext: str = '.txt'):
    head, tail = os.path.split(href)
    filename, _ = os.path.splitext(tail)

    internal = href.startswith('#')
    if not is_doc(href) or internal:
        return href

    return urls.iri_to_uri(os.path.join(head, f'{filename}.{file_ext}'))

def abs_asset_href(href: str, base_url: str):
    if urls.url_is_absolute(href) or os.path.isabs(href):
        return href

    return urls.iri_to_uri(urls.urljoin(base_url, href))

# makes all relative asset links absolute
def replace_asset_hrefs(soup: BeautifulSoup, base_url: str):
    for link in soup.find_all('link', href=True):
        link['href'] = abs_asset_href(link['href'], base_url)

    for asset in soup.find_all(src=True):
        asset['src'] = abs_asset_href(asset['src'], base_url)

    return soup

# normalize href to site root
def normalize_href(href: str, rel_url: str):
    # foo/bar/baz/../../index.html -> foo/index.html
    def reduce_rel(x):
        try:
            i = x.index('..')
            if i == 0:
                return x

            del x[i]
            del x[i - 1]
            return reduce_rel(x)
        except ValueError:
            return x

    rel_dir = os.path.dirname(rel_url)
    href = str.split(os.path.join(rel_dir, href), '/')
    href = reduce_rel(href)
    href[-1], _ = os.path.splitext(href[-1])

    return os.path.join(*href)


def get_separate(soup: BeautifulSoup, base_url: str, file_ext: str = "txt"):
    # transforms all relative hrefs pointing to other html docs
    # into relative txt hrefs
    for a in soup.find_all('a', href=True):
        a['href'] = rel_txt_href(a['href'], file_ext)

    soup = replace_asset_hrefs(soup, base_url)
    return soup