import os

from .links import replace_asset_hrefs, rel_txt_href

from bs4 import BeautifulSoup

def get_separate(soup: BeautifulSoup, base_url: str, file_ext: str = "txt"):
    # transforms all relative hrefs pointing to other html docs
    # into relative txt hrefs
    for a in soup.find_all('a', href=True):
        a['href'] = rel_txt_href(a['href'], file_ext)

    soup = replace_asset_hrefs(soup, base_url)
    return soup