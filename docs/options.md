---
title: Configuration options
layout: default
nav_order: 2
---

<!-- this_file: docs/options.md -->

# Configuration options

Configure the plugin under the `text-export` key in `mkdocs.yml`:

```yaml
plugins:
  - text-export:
      markdown: false
      plain_tables: false
      open_quote: "“"
      close_quote: "”"
      default_image_alt: ""
      hide_strikethrough: false
      kill_tags:
        - script
        - style
      theme_handler_path: ""
      enabled_if_env: ""
      verbose: false
```

Every option, and what it does:

| Option | Type | Default | Effect |
|---|---|---|---|
| `markdown` | bool | `false` | Export Markdown (`.md`) instead of plain text (`.txt`). |
| `plain_tables` | bool | `false` | Render tables as simple lists rather than ASCII borders. |
| `open_quote` | str | `“` | Character used for opening quotes (`<q>` tags). |
| `close_quote` | str | `”` | Character used for closing quotes. |
| `default_image_alt` | str | `""` | Replace every image with this text; empty keeps `html22text`'s default. |
| `hide_strikethrough` | bool | `false` | Drop content inside `<s>`/`<del>` tags. |
| `kill_tags` | list | `[]` | HTML tags (e.g. `script`, `nav`) removed entirely before conversion. |
| `theme_handler_path` | str | `""` | Path to a custom theme handler (see [Theme handlers]({{ '/theme-handlers' | relative_url }})). |
| `enabled_if_env` | str | `None` | Only run when this environment variable equals `1`. Useful for production-only exports. |
| `verbose` | bool | `false` | Emit debug logging from the plugin. |

Most options (`open_quote`, `close_quote`, `default_image_alt`,
`hide_strikethrough`, `kill_tags`, `plain_tables`) are passed straight through to
[`html22text`](https://github.com/twardoch/html22text) and behave exactly as they
do there.

## Enabling conditionally

Set `enabled_if_env` to skip the export unless an environment variable is set:

```yaml
plugins:
  - text-export:
      enabled_if_env: ENABLE_TEXT_EXPORT
```

```bash
ENABLE_TEXT_EXPORT=1 mkdocs build   # exports run
mkdocs build                        # exports skipped
```
