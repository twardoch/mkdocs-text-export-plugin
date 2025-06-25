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


def get_stylesheet() -> str:
    return """
    body > .container {
        margin-top: -100px;
    }

    @page {
        @bottom-left {
            content: counter(__pgnum__);
        }
        size: letter;
    }
    
    @media print {
        .noprint {
            display: none;
        }
    }
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
    soup = BeautifulSoup(html, "html.parser")
    sm_wrapper = soup.new_tag("small")

    a = soup.new_tag("a", href=href, title="Text export", download=None)
    a["class"] = "txt-download"
    a.string = "Open text"

    return str(soup)

    return str(soup)
