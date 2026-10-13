# vexy-mkdocs-text-export

`vexy-mkdocs-text-export` is an MkDocs plugin. While MkDocs builds your site, it
writes a plain-text (`.txt`) or Markdown (`.md`) copy of every page into the same
folder as the page's `.html` file, and adds a link to that copy in the HTML.

![A documentation page becoming a plain-text file](assets/icon.png){ width="160" }

Use the text copies to index a site for search, feed its content to a language
model or a text-processing script, or move the content to another system.

## What goes in and what comes out

The plugin works on the finished HTML of each page, after MkDocs and every other
plugin have rendered it.

Take a site with this source file:

```text
docs/guide/setup.md
```

With the default settings, `mkdocs build` writes:

```text
site/guide/setup/index.html   # the normal page
site/guide/setup/setup.txt    # the plain-text copy
```

The text file is named after the source Markdown file (`setup.md` becomes
`setup.txt`), not after the HTML file. The plugin also adds this element to the
`<head>` of `index.html`, so tools can find the copy:

```html
<link href="setup.txt" rel="alternate" title="Text export"/>
```

Set `markdown: true` and the copy becomes `setup.md`, with links, emphasis and
tables kept as Markdown.

## How the conversion works

1. MkDocs renders the page to HTML.
2. The plugin passes the whole HTML document to
   [`html22text`](https://pypi.org/project/html22text/), which removes the
   tags you list in `kill_tags` and converts the rest with
   [`html2text`](https://pypi.org/project/html2text/).
3. The plugin writes the result next to the page.
4. A theme handler inserts a link to the result into the page HTML. The link is
   a hidden `<link rel="alternate">` for most themes, and a visible button or
   link for `material` and `cinder`.

The plugin converts the whole HTML document, so site navigation, headers and
footers also end up in the text unless you remove them with `kill_tags`. See
[Output format](output.md) for details.

## Where to go next

- [Installation](installation.md): install the plugin from PyPI or from source.
- [Quick start](quickstart.md): add the plugin to a site and check the result.
- [Configuration](configuration.md): every option, its default and its effect.
- [Output format](output.md): what plain-text and Markdown output look like.
- [Theme handlers](theme-handlers.md): how the link is added, and how to write
  your own handler.
- [Troubleshooting](troubleshooting.md): common problems and their causes.

## License

MIT. Its `html22text` dependency is also MIT-licensed.
