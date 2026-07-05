# this_file: mkdocs_text_export_plugin/themes/mkdocs.py
"""Theme handler for the default ``mkdocs`` theme.

The default theme exposes no obvious toolbar slot for an extra button, so this
handler behaves like the generic one: a ``<head>`` ``<link rel="alternate">``.
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
