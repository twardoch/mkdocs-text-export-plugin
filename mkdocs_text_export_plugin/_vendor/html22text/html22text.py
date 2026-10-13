# this_file: mkdocs_text_export_plugin/_vendor/html22text/html22text.py
# Vendored from https://github.com/twardoch/html22text v1.0.0 (MIT). Do not edit; re-vendor instead.

import contextlib
from pathlib import Path
from typing import cast
from html2text import HTML2Text
from bs4 import BeautifulSoup
from bs4.element import NavigableString, PageElement, Tag

from .url_utils import (
    _iri_to_uri_urllib,
    is_doc,
    rel_txt_href,
    abs_asset_href,
    replace_asset_hrefs,
    prep_doc,
    SelectorSyntaxError,
)


def html22text(  # noqa: PLR0913, PLR0915
    html_content: str,  # Renamed from html to avoid confusion with module
    is_input_path: bool = False,  # Renamed from input
    markdown: bool = False,
    selector: str = "html",
    base_url: str = "",
    open_quote: str = "“",
    close_quote: str = "”",
    block_quote: bool = False,
    default_image_alt: str = "",
    kill_strikethrough: bool = False,
    kill_tags: str | list[str] | None = None,  # Comma-separated string or list of CSS selectors
    kill_images: bool = False,
    file_ext_override: str = "",  # Renamed file_ext to avoid confusion
) -> str:
    """Convert HTML text or file to Markdown or plain-text text.

    Args:
        html_content (str): Input HTML text or file path.
        is_input_path (bool, optional): `html_content` is a file path.
            Defaults to False.
        markdown (bool, optional): Output Markdown if True or plain-text if False.
            Defaults to False.
        selector (str, optional): Select the portion of HTML to extract.
            Defaults to "html".
        base_url (str, optional): Base URL for link conversion. Defaults to "".
        open_quote (str, optional): If plain-text, char to use for `<q>`.
            Defaults to "“".
        close_quote (str, optional): If plain-text, char to use for `</q>`.
            Defaults to "”".
        block_quote (bool, optional): If plain-text, treat `<blockquote>` as `<q>`.
            Defaults to False.
        default_image_alt (str, optional): If plain-text, default text placeholder
            for images. Defaults to "".
        kill_strikethrough (bool, optional): If plain-text, remove content of
            `<s></s>`. Defaults to False.
        kill_tags (str | list[str] | None, optional): CSS selectors whose content
            should be removed. Accepts a comma-separated string or a list of
            selector strings. Defaults to None.
        file_ext_override (str, optional): If markdown, file extension for relative
            `.html` link conversion. Defaults to "".

    Returns:
        str: Markdown or plain-text as string.
    """
    actual_kill_tags: list[str] = []
    if isinstance(kill_tags, list):
        actual_kill_tags = [tag.strip() for tag in kill_tags if tag.strip()]
    elif kill_tags:
        actual_kill_tags = [tag.strip() for tag in kill_tags.split(",") if tag.strip()]

    if is_input_path:
        html_content = Path(html_content).read_text(encoding="utf-8")

    soup = BeautifulSoup(html_content, "html.parser")
    with contextlib.suppress(IndexError, SelectorSyntaxError):  # SIM105
        # Ensure we operate on a copy if selection happens, to avoid modifying original
        selected_tag = soup.select(selector)
        if selected_tag:  # Check if selector found anything
            soup = BeautifulSoup(selected_tag[0].encode("utf-8"), "html.parser")

    current_file_ext = file_ext_override
    if not current_file_ext:  # SIM108 applied here
        current_file_ext = "md" if markdown else "txt"

    if markdown:
        soup = prep_doc(soup, base_url, current_file_ext)

    tag_or_element: Tag | PageElement | NavigableString
    for tag_or_element in soup.find_all(True):
        if isinstance(tag_or_element, Tag):
            tag: Tag = tag_or_element  # Narrowing type

            if tag.name in ("mark", "kbd"):
                tag.replace_with(tag.get_text(""))  # type: ignore[arg-type]
            # Custom plain_tables logic removed as html2text native handling is
            # preferred.
            if not markdown and tag.name == "blockquote" and block_quote:
                # If block_quote is True for plain text, transform <blockquote>
                # to <p><q> for custom quoting. Otherwise, <blockquote> is
                # passed through for native html2text handling.
                tag.name = "q"
                tag.wrap(soup.new_tag("p"))
            # Other specific tag transformations for plain text mode have been
            # removed to rely more on html2text's default behavior.

    for kill_item in actual_kill_tags:  # Use the initialized list
        for element_to_kill in soup.select(kill_item):  # select usually returns Tags
            if isinstance(element_to_kill, Tag):
                found_tag_to_kill: Tag = element_to_kill
                found_tag_to_kill.replace_with("")  # type: ignore[arg-type]

    h = HTML2Text()

    # Universal settings
    h.body_width = 0  # No line wrapping
    h.bypass_tables = False
    h.escape_snob = False
    h.google_doc = False
    h.google_list_indent = 0
    h.images_as_html = False
    h.images_with_size = False
    h.links_each_paragraph = False
    h.protect_links = True
    h.single_line_break = False
    h.tag_callback = None
    h.unicode_snob = True
    h.wrap_links = False
    h.wrap_list_items = False
    h.wrap_tables = False

    # Settings from direct pass-through parameters
    h.close_quote = close_quote
    h.default_image_alt = default_image_alt
    h.hide_strikethrough = kill_strikethrough
    h.open_quote = open_quote

    # Conditional settings based on markdown mode or other parameters
    h.emphasis_mark = "_" if markdown else ""
    h.ignore_emphasis = not markdown
    h.ignore_images = not markdown or kill_images
    h.ignore_links = not markdown
    h.ignore_mailto_links = not markdown
    h.ignore_tables = False  # Always let html2text process tables natively
    h.images_to_alt = not markdown  # Convert images to alt text if not markdown
    h.inline_links = bool(markdown)
    h.mark_code = bool(markdown)  # Enable code marking for Markdown
    h.pad_tables = bool(markdown)
    h.skip_internal_links = not markdown
    h.strong_mark = "**" if markdown else ""
    h.ul_item_mark = "-" if markdown else ""
    h.use_automatic_links = bool(markdown)

    result = cast("str", h.handle(str(soup)))
    return result if result.strip() else ""
