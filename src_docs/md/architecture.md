# Architecture

This page describes how the plugin is put together, for readers who want to
change it or debug it.

## Package layout

| Path | Role |
|---|---|
| `mkdocs_text_export_plugin/plugin.py` | `MdTxtExportPlugin`, the MkDocs plugin class. Reads the options and handles the build events. |
| `mkdocs_text_export_plugin/renderer.py` | `Renderer`. Maps the options onto `html22text`, writes the text files and loads the theme handler. |
| `mkdocs_text_export_plugin/themes/` | Built-in theme handlers: `generic`, `mkdocs`, `material`, `cinder`, `basictheme`. |
| `mkdocs_text_export_plugin/_vendor/html22text/` | Bundled copy of `html22text` 1.0.0 (MIT). |
| `mkdocs_text_export_plugin/__version__.py` | Written by `hatch-vcs` at build time. Not in git. |

MkDocs finds the plugin through this entry point in `pyproject.toml`:

```toml
[project.entry-points."mkdocs.plugins"]
text-export = "mkdocs_text_export_plugin.plugin:MdTxtExportPlugin"
```

## Build events

`MdTxtExportPlugin` uses four MkDocs events, in this order.

### `on_config`

1. If `enabled_if_env` is set and the named environment variable is not `"1"`,
   the plugin sets `self.enabled = False`, prints a message and returns. Every
   later event checks `self.enabled` and returns straight away.
2. If `markdown` is true, the output extension becomes `md`; otherwise it stays
   `txt`.
3. The plugin logger level becomes `DEBUG` with `verbose: true`, else `ERROR`.

### `on_nav`

The plugin imports `Renderer` here, not at module level, so a disabled plugin
never imports BeautifulSoup or `html2text`. It creates one `Renderer` with the
theme name and the conversion options, and records the URL of every page in
navigation order.

`Renderer` loads the theme handler at this point (see
[Theme handlers](theme-handlers.md)).

### `on_post_page`

MkDocs calls this once per page with the final HTML. For each page the plugin:

1. Takes the page's output path (`page.file.abs_dest_path`) and source path
   (`page.file.src_path`).
2. Builds the text file name from the source file name: `setup.md` gives
   `setup.txt` or `setup.md`.
3. Builds a `base_url` from the output folder and the file name. `html22text`
   uses it to turn relative image and stylesheet URLs into absolute ones.
4. Calls `Renderer.write_txt()`, which converts the HTML and writes the file.
5. Calls `Renderer.add_link()`, which passes the HTML and the file name to the
   theme handler's `modify_html()`.
6. Returns the changed HTML to MkDocs.

If step 4 or 5 raises an exception, the plugin logs
`Error converting <source path> to text: <error>`, counts the error and returns
the HTML it received. The build continues.

### `on_post_build`

Logs the number of converted files and the time taken at `INFO` level, and, if
any page failed, `<n> conversion errors occurred (see above)` at `ERROR` level.

## The conversion

`Renderer.render_doc()` calls `html22text()` with these arguments:

| `html22text` argument | Value |
|---|---|
| `html_content` | The page HTML |
| `markdown` | The `markdown` option |
| `base_url` | Built in `on_post_page` |
| `open_quote`, `close_quote` | The options of the same name |
| `default_image_alt` | The `default_image_alt` option |
| `kill_strikethrough` | The `hide_strikethrough` option |
| `kill_tags` | The `kill_tags` list joined with commas |
| `file_ext_override` | `md` in Markdown mode, else empty |

`html22text` then:

1. Parses the HTML with BeautifulSoup.
2. In Markdown mode, rewrites relative `.html`/`.htm` links to the output
   extension, and makes `src` and `<link href>` URLs absolute against
   `base_url`.
3. Replaces every `<mark>` and `<kbd>` element with its text.
4. Removes every element that matches a `kill_tags` selector.
5. Converts the result with `html2text.HTML2Text`, with line wrapping turned off
   and mode-specific settings for emphasis, links, images and tables.

The `plain_tables` option is stored on the `Renderer` but not passed to
`html22text`, so it has no effect.

## Why `html22text` is bundled

`html22text` is not published on PyPI, and PyPI rejects packages that depend on
a `git+https` URL. To make the plugin installable from PyPI, its two modules
(`html22text.py` and `url_utils.py`, from tag `v1.0.0`) are copied into
`mkdocs_text_export_plugin/_vendor/html22text/` together with their license. The
command-line entry point of `html22text` is left out, so the plugin does not
need `fire`.

The vendored files are excluded from `ruff` and `mypy`. To update them, copy the
same two files from a newer `html22text` release and update the version noted in
`_vendor/html22text/__init__.py`.
