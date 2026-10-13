# this_file: mkdocs_text_export_plugin/_vendor/html22text/url_utils.py
# Vendored from https://github.com/twardoch/html22text v1.0.0 (MIT). Do not edit; re-vendor instead.
from pathlib import Path
from urllib.parse import quote as urlquote
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from bs4.element import Tag

SelectorSyntaxError: type[Exception]  # Forward declaration for type checkers
try:
    from bs4 import SelectorSyntaxError  # type: ignore[attr-defined, no-redef]
except ImportError:
    try:
        # Attempt fallback: soupsieve might be where it originates
        from soupsieve.util import (  # type: ignore[no-redef]
            SelectorSyntaxError as SoupsieveSelectorSyntaxError,
        )

        SelectorSyntaxError = SoupsieveSelectorSyntaxError
    except ImportError:
        # If all imports fail, define a dummy exception to allow code to run.
        # This might mask selector errors if they occur, but prevents import crashes.
        class SelectorSyntaxError(Exception):  # type: ignore[no-redef]
            """Dummy SelectorSyntaxError if not found in bs4 or soupsieve."""


# Helper function for IRI to URI conversion using urllib.parse
def _iri_to_uri_urllib(iri_string: str) -> str:
    """
    Converts an IRI (Internationalized Resource Identifier) to a URI
    (Uniform Resource Identifier) using urllib.parse.
    Handles IDNA for domain names.
    """
    if not iri_string:
        return ""
    parsed_iri = urlparse(iri_string)
    # Encode domain to Punycode if it's an IDN
    try:
        # urlparse netloc can be "hostname:port"
        hostname = parsed_iri.hostname
        if hostname:
            # Encode to IDNA (Punycode)
            encoded_hostname = hostname.encode("idna").decode("ascii")
            # Reconstruct netloc if port exists
            netloc = encoded_hostname
            if parsed_iri.port:
                netloc = f"{encoded_hostname}:{parsed_iri.port}"

            # Replace the netloc in the parsed result.
            # Namedtuples are immutable, so direct reconstruction or _replace is needed.
            parsed_iri = parsed_iri._replace(netloc=netloc)

    except UnicodeError:
        # If domain encoding fails, proceed with the original (e.g. IP, already ASCII)
        pass

    # Percent-encode the path.
    # urljoin and Path operations handle path normalization.
    # Safe chars for path: alphanumeric + common symbols not needing encoding.
    # Include % in safe chars to avoid double-encoding already-percent-encoded sequences
    quoted_path = urlquote(parsed_iri.path, safe="/:@-._~!$&'()*+,;=%")
    parsed_iri = parsed_iri._replace(path=quoted_path)

    # urlunparse will reassemble the URI
    return parsed_iri.geturl()


def is_doc(href: str) -> bool:
    """Check if href is relative and points to an HTML-like file.

    If it is relative it *should* be an html that generates a text file.

    Args:
        href (str): input URL

    Returns:
        bool: True if relative and HTML-like.
    """
    href_path = Path(href)
    ext = href_path.suffix

    # Use urllib.parse.urlparse to check for a scheme
    parsed_href = urlparse(href)
    absurl = bool(parsed_href.scheme)

    # For local paths, check if it's absolute using Path.is_absolute()
    # We assume href is a path-like string if not a URL
    # This logic remains the same: if it's not a scheme-based URL, check path absolutism
    abspath = False if absurl else href_path.is_absolute()
    htmlfile = ext.lower() in {".html", ".htm"}

    return not (absurl or abspath or not htmlfile)


def rel_txt_href(href: str, file_ext: str = ".txt") -> str:
    """Converts a relative HTML href to a relative text href.

    Args:
        href (str): URL.
        file_ext (str, optional): Target file extension. Defaults to ".txt".

    Returns:
        str: URL.
    """
    href_path = Path(href)
    filename = href_path.stem

    internal = href.startswith("#")
    if not is_doc(href) or internal:
        return href

    # Construct new path using Path objects for robustness
    new_path = href_path.with_name(f"{filename}.{file_ext.lstrip('.')}")
    return _iri_to_uri_urllib(str(new_path))


def abs_asset_href(href: str, base_url: str) -> str:
    """Makes a possibly relative asset URL absolute.

    Args:
        href (str): URL.
        base_url (str): Base URL to resolve relative links.

    Returns:
        str: Absolute URL.
    """
    href_path = Path(href)
    parsed_href = urlparse(href)
    is_url_absolute = bool(parsed_href.scheme)

    if is_url_absolute or href_path.is_absolute():
        return _iri_to_uri_urllib(
            href
        )  # Ensure even absolute URLs are correctly IRI encoded

    # Use urllib.parse.urljoin for joining
    joined_url = urljoin(base_url, href)
    return _iri_to_uri_urllib(joined_url)


def replace_asset_hrefs(soup: BeautifulSoup, base_url: str) -> BeautifulSoup:
    """Makes all relative asset links absolute in the soup.

    Args:
        soup (BeautifulSoup): Parsed HTML.
        base_url (str): Base URL.

    Returns:
        BeautifulSoup: Modified soup.
    """
    for element in soup.find_all("link", href=True):
        if isinstance(element, Tag):
            link_tag: Tag = element
            current_href = link_tag.get("href")
            if isinstance(current_href, str):
                link_tag["href"] = abs_asset_href(current_href, base_url)
            elif isinstance(current_href, list):  # Should not happen for 'href'
                # Changed to TypeError as per TRY004 suggestion
                error_message = (
                    f"Unexpected list value for 'href' attribute in <link>: "
                    f"{current_href}"
                )
                raise TypeError(error_message)

    for element in soup.find_all(src=True):
        if isinstance(element, Tag):
            asset_tag: Tag = element
            current_src = asset_tag.get("src")
            if isinstance(current_src, str):
                asset_tag["src"] = abs_asset_href(current_src, base_url)
            elif isinstance(current_src, list):  # Should not happen for 'src'
                asset_tag["src"] = abs_asset_href(str(current_src[0]), base_url)

    return soup


def prep_doc(
    soup: BeautifulSoup, base_url: str, file_ext: str = "txt"
) -> BeautifulSoup:
    """Transforms relative HTML doc hrefs to relative text hrefs.

    Args:
        soup (BeautifulSoup): Parsed HTML.
        base_url (str): Base URL.
        file_ext (str, optional): Target file extension. Defaults to "txt".

    Returns:
        BeautifulSoup: Modified soup.
    """
    for element in soup.find_all("a", href=True):
        if isinstance(element, Tag):
            anchor_tag: Tag = element
            current_href = anchor_tag.get("href")
            if isinstance(current_href, str):
                anchor_tag["href"] = rel_txt_href(current_href, file_ext)
            # Removed check for `isinstance(current_href, list)` for anchor tags'
            # href, as this is highly unlikely for standard HTML and
            # `rel_txt_href` expects a string.

    # The RET504 for this was valid, direct return.
    return replace_asset_hrefs(soup, base_url)
