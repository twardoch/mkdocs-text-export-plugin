# Configuration Options

You can configure the `mkdocs-text-export-plugin` by passing options under the `text-export` key in your `mkdocs.yml` file.

```yaml
plugins:
  - text-export:
      # --- General Options ---
      enabled_if_env: YOUR_ENV_VARIABLE_NAME # Optional
      verbose: false

      # --- Output Format ---
      markdown: false

      # --- Plain Text Specific Options (when markdown: false) ---
      plain_tables: false
      default_image_alt: ""

      # --- Markdown & Plain Text Common Options (passed to html22text) ---
      open_quote: "“"
      close_quote: "”"
      hide_strikethrough: false
      kill_tags:
        - script
        - style

      # --- Theme Handling ---
      theme_handler_path: "" # Optional path to custom_handler.py
```

Below is a detailed description of each option:

## General Options

### `enabled_if_env`
<small>*Default: `None` (plugin is always enabled)*</small>

If set to an environment variable name (e.g., `ENABLE_TEXT_EXPORT`), the plugin will only run if that environment variable is set to `1`. This is useful for conditionally enabling the plugin, for example, only in production builds.

### `verbose`
<small>*Default: `false`*</small>

Set to `true` to enable verbose logging from the plugin, which can be helpful for debugging. This typically includes more detailed messages from the theme handler loading process and conversion steps.

## Output Format

### `markdown`
<small>*Default: `false`*</small>

- If `false` (default), pages are exported to plain text (`.txt`) files.
- If `true`, pages are exported to simplified Markdown (`.md`) files.

## Plain Text Specific Options

These options primarily affect the output when `markdown: false`.

### `plain_tables`
<small>*Default: `false`*</small>

If `true` and exporting to plain text, tables will be rendered in a simpler, list-like format instead of attempting to draw ASCII table borders. This option is passed to `html22text`.

### `default_image_alt`
<small>*Default: `""` (empty string)*</small>

If set to a non-empty string (e.g., `"[Image]"`), all images encountered during plain text conversion will be replaced by this string. If empty, `html22text`'s default behavior for images applies (which might be to use the image's actual `alt` text or a link).

## Markdown & Plain Text Common Options

These options are generally passed through to the underlying `html22text` library and affect both Markdown and plain text output.

### `open_quote`
<small>*Default: `"“"` (U+201C Left Double Quotation Mark)*</small>

The character or string to use for opening quotes (e.g., for the `<q>` HTML tag).

### `close_quote`
<small>*Default: `"”"` (U+201D Right Double Quotation Mark)*</small>

The character or string to use for closing quotes.

### `hide_strikethrough`
<small>*Default: `false`*</small>

If `true`, content within `<s>` or `<del>` (strikethrough) HTML tags will be removed from the output. If `false`, the content is typically preserved but without the strikethrough formatting.

### `kill_tags`
<small>*Default: `[]` (empty list)*</small>

A list of HTML tags (e.g., `script`, `style`, `nav.header`, `p.admonition-title`) whose content (including the tags themselves) will be completely removed from the HTML before conversion. This is useful for stripping out elements that are not relevant to the text or Markdown output.

## Theme Handling

### `theme_handler_path`
<small>*Default: `""` (empty string, uses built-in handlers)*</small>

Allows you to specify a path to a custom Python script that acts as a theme handler. The path should be relative to your MkDocs project root (where `mkdocs.yml` is located). See the [Custom Theme Handlers](theme_handlers.md) page for more details on creating one. If not specified, the plugin will try to use a built-in handler matching your site's theme, or a generic fallback.