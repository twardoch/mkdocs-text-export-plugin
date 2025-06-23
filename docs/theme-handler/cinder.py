# This is an EXAMPLE custom theme handler for mkdocs-text-export-plugin.
# It demonstrates the structure you would use to create your own.
#
# To use a custom handler:
# 1. Create a Python file like this one.
# 2. Place it in your MkDocs project (e.g., in a 'theme_handlers' directory).
# 3. In your mkdocs.yml, configure the plugin:
#    plugins:
#      - text-export:
#          theme_handler_path: "theme_handlers/your_custom_handler.py"

from bs4 import BeautifulSoup

def fix_html(html: str, base_url: str) -> str:
    """
    Modifies the HTML content of a page before it's converted to text or Markdown.
    This function is called by the core plugin.

    Args:
        html: The raw HTML string of the page.
        base_url: The base URL of the page (rarely needed for text conversion).

    Returns:
        The modified HTML string.
    """
    soup = BeautifulSoup(html, "html.parser")

    # --- Example Modifications (adapt these to your specific theme) ---

    # Example 1: Remove a specific navigation bar if it exists
    # nav_element = soup.find("nav", class_="main-navigation")
    # if nav_element:
    #     print(f"INFO: Custom theme handler removing '.main-navigation'") # Example logging
    #     nav_element.decompose()

    # Example 2: Remove a common MkDocs theme footer
    # footer_element = soup.find("footer", class_="md-footer")
    # if footer_element:
    #     print(f"INFO: Custom theme handler removing '.md-footer'")
    #     footer_element.decompose()

    # Example 3: Remove all <script> and <style> tags
    # for tag_name in ["script", "style"]:
    #     for tag in soup.find_all(tag_name):
    #         tag.decompose()

    # You can add more sophisticated logic to find and remove or alter elements
    # specific to your theme to improve the text/Markdown output.

    return str(soup)


def modify_html(html: str, href: str) -> str:
    """
    Modifies the original page's HTML, typically to add a <link rel="alternate">
    tag pointing to the exported text/Markdown file.
    This function is called by the core plugin.

    Args:
        html: The original HTML string of the page.
        href: The relative path to the generated text or Markdown file.

    Returns:
        The modified HTML string (with the added link tag).
    """
    soup = BeautifulSoup(html, "html.parser")

    if soup.head:
        link_tag = soup.new_tag(
            "link",
            rel="alternate",
            # The 'type' attribute (e.g., 'text/plain' or 'text/markdown')
            # will be automatically set by the plugin based on the output format.
            href=href,
            title="Text Export Version"  # A descriptive title for the link
        )
        soup.head.append(link_tag)
    else:
        # This case should be rare for valid MkDocs pages
        print(f"WARNING: Custom theme handler: No <head> tag found in page to add alternate link.")

    return str(soup)


def get_stylesheet() -> str:
    """
    Returns custom CSS for styling the page before conversion.
    This function is generally NOT USED by mkdocs-text-export-plugin,
    as its focus is on text content rather than visual styling for an
    intermediate format (like PDF generation plugins might use).

    It's included here for structural completeness if you are adapting
    a theme handler from a plugin that does use it (e.g., a PDF exporter).
    For mkdocs-text-export-plugin, you can safely have it return an empty string.
    """
    return ""
