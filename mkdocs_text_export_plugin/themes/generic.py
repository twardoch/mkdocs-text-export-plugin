# this_file: mkdocs_text_export_plugin/themes/generic.py
"""Fallback theme handler used when a site's theme has no dedicated module.

It adds an invisible ``<link rel="alternate">`` to the page ``<head>`` pointing at
the exported text file — safe for any theme, with no visible UI change.
"""

from bs4 import BeautifulSoup


def get_stylesheet() -> str:
    """Return theme CSS to inject; none is needed for a text export."""
    return ""


def modify_html(html: str, href: str) -> str:
    """Add an ``<link rel="alternate">`` to ``<head>`` referencing ``href``."""
    soup = BeautifulSoup(html, "html.parser")

    if soup.head:
        link = soup.new_tag("link", href=href, rel="alternate", title="Text export")
        soup.head.append(link)

    return str(soup)
