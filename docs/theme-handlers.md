---
title: Theme handlers
layout: default
nav_order: 3
---

<!-- this_file: docs/theme-handlers.md -->

# Theme handlers

After writing the text file, the plugin adds a "download as text" link to the
built HTML page. *How* that link is added depends on the theme — a Material page
has a content toolbar, a plain `mkdocs` page does not. Theme handlers encapsulate
that difference.

## Built-in handlers

The plugin ships a handler per theme and picks the one matching your site's
`theme.name`. If none matches, the generic handler is used.

| Handler | Theme | What it injects |
|---|---|---|
| `generic` | fallback | Invisible `<link rel="alternate">` in `<head>`. |
| `mkdocs` | default `mkdocs` | Same head link as generic. |
| `basictheme` | `basic` | Same head link as generic. |
| `material` | `mkdocs-material` | Visible download button in the article header. |
| `cinder` | `cinder` | Visible "Open text" link in the page footer. |

## Writing a custom handler

Point `theme_handler_path` at a Python file, relative to your project root:

```yaml
plugins:
  - text-export:
      theme_handler_path: "my_handler.py"
```

A handler is a plain module with two functions:

```python
# my_handler.py
from bs4 import BeautifulSoup


def get_stylesheet() -> str:
    # Optional CSS; unused for text export, return "".
    return ""


def modify_html(html: str, href: str) -> str:
    # `html` is the rendered page; `href` is the exported text file's name.
    # Return the HTML with your link added.
    soup = BeautifulSoup(html, "html.parser")
    if soup.head:
        link = soup.new_tag("link", href=href, rel="alternate", title="Text export")
        soup.head.append(link)
    return str(soup)
```

`modify_html` is the only function the plugin calls. Use
[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) (already a
dependency) to place the link wherever your theme has room for it.
