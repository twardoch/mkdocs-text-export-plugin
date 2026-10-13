# Theme handlers

After the plugin writes a text file, it adds a link to that file into the page's
HTML. A theme handler decides where the link goes. A theme with a content
toolbar can show a visible button; a plain theme gets a hidden `<head>` link.

## Built-in handlers

The plugin picks a handler by the `theme.name` value in `mkdocs.yml`. It
replaces hyphens in the name with underscores and looks for a module of that
name in `mkdocs_text_export_plugin/themes/`.

| `theme.name` | Handler module | What the handler adds |
|---|---|---|
| `mkdocs` | `mkdocs` | `<link href="…" rel="alternate" title="Text export"/>` in `<head>` |
| `material` | `material` | A download button inside `<article class="md-content__inner md-typeset">` |
| `cinder` | `cinder` | A small "Open text" link at the start of `<footer>` |
| Any other name | `generic` | The same `<head>` link as `mkdocs` |

When no module matches, the plugin prints a message such as
`Could not load theme handler readthedocs: No module named 'mkdocs_text_export_plugin.themes.readthedocs'`
and uses `generic`. The message is printed outside the MkDocs logger, so it does
not count as a warning in `mkdocs build --strict`.

!!! note
    The package also contains `themes/basictheme.py`, which adds the same head
    link. A theme named `basic` looks for `themes/basic.py`, does not find it,
    and ends up with `generic`, so the result is the same.

### The `material` button

The `material` handler inserts this element right after the opening
`<article class="md-content__inner md-typeset">` tag:

```html
<a class="md-content__button md-icon" download href="index.txt" title="Text export"><svg …></svg></a>
```

It does a plain text replacement on that exact tag. A theme that is based on
Material but writes the tag differently, or uses another theme name such as
`materialx`, does not get the button. It gets the `generic` head link instead.

### The `cinder` link

The `cinder` handler wraps an `<a download class="txt-download">Open text</a>`
element in `<small>` and inserts it as the first child of the page `<footer>`.
If the page has no `<footer>`, nothing is added.

## Write your own handler

A handler is a Python file with one required function:

```python
def modify_html(html: str, href: str) -> str: ...
```

- `html` is the full page HTML, after every other plugin has run.
- `href` is the file name of the text copy, for example `setup.txt`.
- The function returns the HTML that MkDocs will write.

Built-in handlers also define `get_stylesheet() -> str`, which returns CSS. The
plugin never calls it, so a custom handler does not need it.

### Steps

1. Create a file in your project, for example `text_link.py`:

    ```python
    from bs4 import BeautifulSoup


    def modify_html(html: str, href: str) -> str:
        """Add a visible link to the text copy at the end of the main content."""
        soup = BeautifulSoup(html, "html.parser")
        main = soup.find("main") or soup.body
        if main is not None:
            p = soup.new_tag("p")
            a = soup.new_tag("a", href=href)
            a.string = "Plain-text version"
            p.append(a)
            main.append(p)
        return str(soup)
    ```

    `beautifulsoup4` is already installed, because the plugin depends on it.

2. Point `theme_handler_path` at the file:

    ```yaml
    plugins:
      - text-export:
          theme_handler_path: text_link.py
    ```

3. Run `mkdocs build` from the folder that contains `text_link.py`. The path is
   resolved against the current working directory, not against the location of
   `mkdocs.yml`.

Each built page now ends with a "Plain-text version" link.

### How a custom handler is loaded

The plugin loads the file with `importlib` when MkDocs builds the navigation.

- If the file does not exist, the plugin prints
  `Could not load theme handler <theme> from custom directory "<path>": …` and
  uses the built-in handler for the theme.
- Any other error in the file, such as a syntax error, is not caught and stops
  the build.
- If `modify_html` raises an exception for a page, the plugin logs
  `Error converting <page> to text: …`, leaves that page's HTML unchanged and
  continues. The text file for that page has already been written at that point.
