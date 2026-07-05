# this_file: mkdocs_text_export_plugin/themes/cinder.py
"""Theme handler for the ``cinder`` theme.

Unlike the head-link handlers, this one adds a *visible* "Open text" link to the
page footer so readers can reach the export directly.
"""

from bs4 import BeautifulSoup


def get_stylesheet() -> str:
    """Return theme CSS to inject; none is needed for a text export."""
    return ""


def modify_html(html: str, href: str) -> str:
    """Prepend a small "Open text" link to the page ``<footer>``."""
    soup = BeautifulSoup(html, "html.parser")

    sm_wrapper = soup.new_tag("small")

    a = soup.new_tag("a", href=href, title="Text export")
    a["download"] = None  # type: ignore[assignment]  # valueless boolean attribute
    a["class"] = "txt-download"
    a.string = "Open text"

    sm_wrapper.append(a)
    if soup.body:
        footer = getattr(soup.body, "footer", None)
        if footer:
            footer.insert(0, sm_wrapper)

    return str(soup)
