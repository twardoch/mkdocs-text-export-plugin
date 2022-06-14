# mkdocs-plugin-toplaintext

MkDocs plugin to convert the pages to Markdown or plain text.

It uses MkDocs to render the final HTML documents, and some custom preprocessing to extract either a plain-text or a Markdown representation.

The Markdown output is useful if you use MkDocs plugins extensively, for various code inclusions, preprocessing etc. So your sources may not really be simple Markdown but a complicated labyrinth. If you use this plugin convert to Markdown, you’ll get simplfied Markdown output. Note that this will not maintain your custom Markdown constructs or HTML-in-Markdown formatting, because the plugin uses [`html2text`](https://github.com/Alir3z4/html2text/) to create the Markdown from the fully rendered HTML files.

The plain-text output is useful for tasks such as natural language processing (NLP).

## Usage

At the **end** of you `plugins` section of your `mkdocs.yml` add `text-export`.

Example:

```yaml
plugins:
  - ... # other plugins
  - text-export:
      verbose: false
      markdown: false # exports to plain text, or if `true`, exports to Markdown
      plain_tables: false # if `true` for plain-text export, makes a plain form of tables
      open_quote: "“" # default character for the opening char of the `<q>` tag
      close_quote: "”" # default character for the opening char of the `<q>` tag
      default_image_alt: "" # if non-empty for plain-text export, writes this instead of images
      hide_strikethrough: false # if `true`, removes content enclosed in `<s>` tag
      kill_tags: # list selectors for which the content will be removed
        - pre
        - ins.new
        - p.admonition-title
      theme_handler_path: "" # special handler for a theme
```

If `markdown` is `false`, writes the plain-text representation of each `.html` file as `.txt` file with the same path.

If `markdown` is `true`, writes the Markdown representation of each `.html` file as `.md` file with the same path.

## Special thanks

- Based on [mkdocs-pdf-export-plugin](https://github.com/zhaoterryy/mkdocs-pdf-export-plugin/)  by [Terry Zhao](https://github.com/zhaoterryy)
- Based on the work of [Stephan Hauser][shauser]
- Based on [mkdocs-awesome-pages-plugin][awesome-pages-plugin] by [Lukas Geiter][lukasgeiter]

