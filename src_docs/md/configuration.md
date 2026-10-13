# Configuration

Configure the plugin under the `text-export` key in the `plugins` list of
`mkdocs.yml`. Every option is optional. This block lists all options with their
default values:

```yaml
plugins:
  - text-export:
      markdown: false
      kill_tags: []
      open_quote: "“"
      close_quote: "”"
      default_image_alt: ""
      hide_strikethrough: false
      plain_tables: false
      theme_handler_path: ""
      enabled_if_env: null
      verbose: false
```

## Options

| Option | Type | Default | Effect |
|---|---|---|---|
| `markdown` | bool | `false` | Write Markdown (`.md`) instead of plain text (`.txt`). |
| `kill_tags` | list of str | `[]` | CSS selectors. Matching elements and their content are removed before conversion. |
| `open_quote` | str | `“` | Text written in place of an opening `<q>` tag. |
| `close_quote` | str | `”` | Text written in place of a closing `</q>` tag. |
| `default_image_alt` | str | `""` | Markdown mode only: text used as the alt text of images that have none. |
| `hide_strikethrough` | bool | `false` | Passed to `html2text`. Has no visible effect on MkDocs output; see below. |
| `plain_tables` | bool | `false` | Accepted but not used; see below. |
| `theme_handler_path` | str | `""` | Path to a Python file that adds the link to the text file. See [Theme handlers](theme-handlers.md). |
| `enabled_if_env` | str | `null` | Name of an environment variable. The plugin runs only when that variable equals `1`. |
| `verbose` | bool | `false` | Set the plugin's log level to `DEBUG` instead of `ERROR`. |

## `markdown`

With `markdown: false` (the default), the plugin writes `<name>.txt`. With
`markdown: true`, it writes `<name>.md`, where `<name>` is the source file name
without its extension.

The two modes differ in what they keep:

| Element | Plain text | Markdown |
|---|---|---|
| Bold and italic | Markers removed | `**bold**`, `_italic_` |
| Links | Link text only | `[text](<url>)`, with `.html` targets changed to `.md` |
| Images | Removed | `![alt](absolute path)` |
| Tables | Pipe-separated rows | Padded Markdown tables |
| Code blocks | Indented text | Wrapped in `[code]` and `[/code]` |

[Output format](output.md) shows real examples of both modes.

## `kill_tags`

A list of CSS selectors. Before the conversion, the plugin removes every element
that matches one of them, together with its content. Plain tag names such as
`script` or `footer` work, and so do class and attribute selectors such as
`.navbar` or `div[role=navigation]`.

```yaml
plugins:
  - text-export:
      kill_tags:
        - script
        - style
        - .navbar
        - footer
```

The plugin converts the whole HTML document, not only the article, so
`kill_tags` is how you keep navigation and footers out of the text.

## `open_quote` and `close_quote`

`html2text` replaces inline quotations (`<q>…</q>`) with these two strings. With
the defaults, `<q>quoted</q>` becomes `“quoted”`. Block quotes
(`<blockquote>`) are not affected; they become lines that start with `>`.

## `default_image_alt`

Only has an effect when `markdown: true`. An image without an `alt` attribute
gets this text as its alt text, so `<img src="a.png">` with
`default_image_alt: "image"` becomes `![image](/…/a.png)`. In plain-text mode,
images are removed completely, so the option does nothing there.

## `hide_strikethrough`

The plugin passes this value to `html2text` as `hide_strikethrough`.
`html2text` only applies that setting to Google Docs-style input, which this
plugin does not enable. As a result, `<del>` and `<s>` content stays in the
output in both modes, written as `~~text~~`. To remove struck-through text, add
`del` and `s` to `kill_tags` instead.

## `plain_tables`

The plugin reads this option and stores it, but does not pass it on to the
converter. Setting it has no effect on the output. Tables are always converted
by `html2text`'s own table handling.

## `theme_handler_path`

A path to a Python file, resolved against the current working directory (the
directory you run `mkdocs` from). The file replaces the built-in handler for
your theme. If the file does not exist, the plugin prints a message and falls
back to the built-in handler. See [Theme handlers](theme-handlers.md).

## `enabled_if_env`

When set, the plugin checks the named environment variable while MkDocs reads
its configuration. If the variable is not exactly `1`, the plugin prints a
message and skips every later step:

```text
Text export is disabled (set environment variable ENABLE_TEXT_EXPORT to 1 to enable)
```

When the option is not set, the plugin always runs.

## `verbose`

Sets the level of the `mkdocs_text_export_plugin.plugin` logger to `DEBUG`.
Without it, the level is `ERROR`, so only conversion errors are shown.
