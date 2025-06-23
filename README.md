# mkdocs-text-export-plugin

An MkDocs plugin to convert your documentation pages to Markdown or plain text.

This plugin processes the fully rendered HTML of your MkDocs site. It then uses the [`html22text`](https://github.com/twardoch/html22text) library, along with theme-specific handlers, to extract either a plain-text or a simplified Markdown representation of your content.

- **Markdown Output**: Useful if your source files use many MkDocs plugins for features like code inclusion, content embedding, or other preprocessing. The output will be a simplified Markdown document, which may not preserve all custom Markdown constructs or raw HTML present in your original source.
- **Plain Text Output**: Ideal for tasks such as natural language processing (NLP), content indexing, or creating easily consumable text versions of your documentation.

## Installation

Install the plugin using pip:

```bash
pip install mkdocs-text-export-plugin
```

## Usage

Add `text-export` to the `plugins` section of your `mkdocs.yml`. It's generally recommended to place it towards the **end** of the plugin list to ensure it processes the final HTML output from other plugins.

Example `mkdocs.yml` configuration:

```yaml
plugins:
  - search # Example: ensure search is loaded before
  - another-plugin
  - text-export:
      # --- General Options ---
      # enabled_if_env: MY_ENV_VARIABLE # Only enable if MY_ENV_VARIABLE=1
      verbose: false # Set to true for detailed logging

      # --- Output Format ---
      markdown: false # if true, exports to Markdown; otherwise, exports to plain text

      # --- Plain Text Specific Options (when markdown: false) ---
      plain_tables: false # if true, uses a simpler list-like format for tables
      default_image_alt: "" # if non-empty, replaces all images with this alt text.
                            # If empty, images are typically converted to their alt text or a link.

      # --- Markdown & Plain Text Common Options (via html22text) ---
      open_quote: "“" # Character for the opening <q> tag
      close_quote: "”" # Character for the closing <q> tag
      hide_strikethrough: false # if true, removes content enclosed in <s> or <del> tags

      kill_tags: # List of HTML tags whose content will be completely removed
        - script # Example: remove all script tags and their content
        - style  # Example: remove all style tags and their content
        # - pre
        # - ins.new
        # - p.admonition-title

      # --- Theme Handling ---
      # theme_handler_path: "path/to/my_custom_theme_handler.py" # Path to a custom theme handler script
                                                              # See docs/theme-handler/cinder.py for an example.
```

### Output Files

- If `markdown` is `false` (default), the plugin writes the plain-text representation of each page as a `.txt` file in the same directory as the original HTML page within your `site_dir`.
- If `markdown` is `true`, it writes the Markdown representation as an `.md` file, also in the same relative path within your `site_dir`.

The plugin also attempts to add a `<link rel="alternate" ...>` tag to the HTML `<head>` of each page, pointing to its corresponding text or Markdown export.

## Dependencies

This plugin relies on several key libraries:

- [`html22text`](https://github.com/twardoch/html22text): For the core HTML to text/Markdown conversion.
- `BeautifulSoup4`: For parsing and manipulating HTML, especially within theme handlers.
- `MkDocs`: The 당연하지! (naturally!)

## Contributing

Contributions are welcome! If you find a bug, have a feature request, or want to improve the plugin:

1.  Please check the [issue tracker](https://github.com/twardoch/mkdocs-text-export-plugin/issues) to see if your concern has already been reported.
2.  If not, open a new issue.
3.  Pull requests are greatly appreciated. For larger changes, please open an issue first to discuss the proposed changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

The development of this plugin was inspired by and based on the foundational work of several other projects and individuals:

- [mkdocs-pdf-export-plugin](https://github.com/zhaoterryy/mkdocs-pdf-export-plugin/) by [Terry Zhao](https://github.com/zhaoterryy)
- The work of [Stephan Hauser][shauser]
- [mkdocs-awesome-pages-plugin][awesome-pages-plugin] by [Lukas Geiter][lukasgeiter]

This version has been further developed and may include significant modifications from the original concepts.

