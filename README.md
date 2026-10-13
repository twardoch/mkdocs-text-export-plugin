<!-- this_file: README.md -->
# vexy-mkdocs-text-export

**Your MkDocs site, as plain text. Grep-friendly.**

**Documentation:** https://vexy.dev/vexy-mkdocs-text-export/

Every page MkDocs builds is HTML. This plugin writes a second copy of each page as
plain text or Markdown, right beside the `.html` file. Feed it to an NLP pipeline,
index it for search, or migrate the content elsewhere.

## Visual

<img src="https://vexy.dev/vexy-mkdocs-text-export/assets/icon.png" alt="A documentation page becoming a plain-text file, with a grep magnifier" width="180">

## Quick start

```bash
pip install vexy-mkdocs-text-export
```

```yaml
# mkdocs.yml — add the plugin near the end of the list
plugins:
  - search
  - text-export
```

```bash
mkdocs build
```

Now `docs/guide/setup.md` produces `site/guide/setup/index.html` and, beside it,
`site/guide/setup/setup.txt` (the text file is named after the source file). Want
Markdown instead? Set `markdown: true`.

The plugin converts the whole HTML page, theme navigation included. Use
`kill_tags` (CSS selectors) to drop menus and footers from the text.

## How it works

The plugin runs on the final rendered HTML, at the tail of the build, after every
other plugin has finished. It hands that HTML to a bundled copy of `html22text`,
which strips tags and reflows the content into text or Markdown, then writes the
result next to the page. A per-theme handler adds a small "download as text" link to each page so
readers can find the export.

Place `text-export` **last** in your plugin list so it sees the fully processed
HTML from plugins that run before it.

## Configuration

```yaml
plugins:
  - text-export:
      markdown: false          # true → .md output, false → .txt (default)
      plain_tables: false      # accepted, currently has no effect
      open_quote: "“"          # opening quote for <q> tags
      close_quote: "”"         # closing quote for <q> tags
      default_image_alt: ""    # Markdown mode: alt text for images without one
      hide_strikethrough: false # no effect on MkDocs output; use kill_tags: [del, s]
      kill_tags:               # CSS selectors removed before conversion
        - script
        - style
      theme_handler_path: ""   # path to a custom theme handler
      enabled_if_env: ""       # only run when this env var == "1"
      verbose: false           # debug logging
```

Most options pass straight through to `html22text`. See the
[configuration reference](https://vexy.dev/vexy-mkdocs-text-export/configuration/)
for details.

### Run only in production

```yaml
plugins:
  - text-export:
      enabled_if_env: ENABLE_TEXT_EXPORT
```

```bash
ENABLE_TEXT_EXPORT=1 mkdocs build   # exports run
mkdocs build                        # exports skipped
```

## Theme handlers

After writing each text file, the plugin adds a "download as text" link to the
page. How it does so depends on the theme:

| Theme | Link placement |
|---|---|
| `mkdocs`, `basic`, other | invisible `<head>` alternate link |
| `mkdocs-material` | visible download button in the article header |
| `cinder` | visible "Open text" link in the footer |

To control placement yourself, point `theme_handler_path` at a Python module that
exposes `modify_html(html, href) -> str`. See the
[theme handlers guide](https://vexy.dev/vexy-mkdocs-text-export/theme-handlers/).

## Development

```bash
uv venv --python 3.12 && source .venv/bin/activate
uv pip install -e ".[dev]"
pytest                                   # run tests
ruff check . && mypy mkdocs_text_export_plugin
```

The version is derived from git tags via `hatch-vcs`; there is no hardcoded
version string. CI runs tests on Python 3.12/3.13 across Linux and Windows, plus
against multiple MkDocs minor versions.

## License

MIT. See [LICENSE](LICENSE).

## Acknowledgements

Built on [`html22text`](https://github.com/twardoch/html22text) (MIT, vendored in
`mkdocs_text_export_plugin/_vendor/html22text/` because it is not on PyPI) and inspired by
[mkdocs-pdf-export-plugin](https://github.com/zhaoterryy/mkdocs-pdf-export-plugin)
by Terry Zhao.
