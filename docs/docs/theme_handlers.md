# Custom Theme Handlers

The `mkdocs-text-export-plugin` allows for theme-specific adjustments to the HTML content before it's converted to text or Markdown. This is achieved through "theme handlers."

## Purpose

Different MkDocs themes structure their HTML in various ways. A theme handler can:

- Remove theme-specific navigation, headers, footers, or sidebars that are irrelevant to a text export.
- Restructure content for better text-based readability.
- Make other modifications to the HTML to improve the quality of the text or Markdown output.

## How it Works

The plugin attempts to load a built-in handler corresponding to your site's theme name (e.g., `material.py` for the `mkdocs-material` theme). If a specific handler for your theme isn't found, it defaults to a `generic.py` handler which performs minimal modifications.

## Using a Custom Theme Handler

You can provide your own theme handler script using the `theme_handler_path` option in the plugin configuration:

```yaml
plugins:
  - text-export:
      theme_handler_path: "path/to/your/custom_handler.py"
```

The specified path should be relative to your MkDocs project root (where `mkdocs.yml` is located).

### Theme Handler Script Structure

A theme handler script must implement at least one function:

- `fix_html(html: str, base_url: str) -> str`:
    - Takes the raw HTML content of a page and its base URL as input.
    - Should return the modified HTML string.
    - This function is called by the main `Renderer` before passing the HTML to `html22text`.

Additionally, for more advanced integration (like adding custom links or modifying the final output path, though less common for this plugin's direct text output compared to, say, PDF generation plugins), a theme handler *could* implement:

- `modify_html(html: str, href: str) -> str`:
    - This function is called by the plugin to allow the theme handler to modify the original page's HTML, for example, to add a `<link rel="alternate">` tag. The `href` parameter is the path to the generated text file.
    - The default theme handlers in this plugin already provide a basic implementation for this.
- `get_stylesheet() -> str`:
    - Less relevant for text export, but for PDF or other rich outputs, this could provide custom CSS. For text export, it's unlikely to be used.

### Example

An example of a custom theme handler can be found at `docs/theme-handler/cinder.py` within this plugin's repository. While it was originally for the `cinder` theme and potentially for a PDF export context, it demonstrates the structure of such a handler.

```python
# Example structure (docs/theme-handler/cinder.py)
from bs4 import BeautifulSoup

def fix_html(html: str, base_url: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    # Example: Remove a specific element
    # nav = soup.find("nav", class_="md-tabs")
    # if nav:
    #     nav.decompose()

    return str(soup)

def modify_html(html: str, href: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    if soup.head:
        link_tag = soup.new_tag(
            "link",
            rel="alternate",
            # type attribute will be set by the plugin based on output format
            href=href,
            title="Text Export"
        )
        soup.head.append(link_tag)
    return str(soup)

# def get_stylesheet() -> str:
# return ""
```

When creating your own handler, you'll typically use a library like `BeautifulSoup4` to parse and manipulate the HTML. Remember to install any necessary dependencies for your custom handler in your MkDocs environment.
