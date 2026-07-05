---
title: Home
layout: default
nav_order: 1
---

<!-- this_file: docs/index.md -->

# Your MkDocs site, as plain text

Every page your MkDocs build produces is HTML. This plugin writes a second copy
of each page as clean plain text or Markdown, right next to the `.html` file. No
theme chrome, no navigation, no scripts — just the words, ready to grep, feed to
an NLP pipeline, or migrate somewhere else.

```yaml
# mkdocs.yml — add the plugin near the end of the list
plugins:
  - search
  - text-export
```

Build your site, and `site/page/index.html` gains a sibling `site/page/index.txt`.
Want Markdown instead of plain text? Set `markdown: true`.

## Install

The plugin depends on [`html22text`](https://github.com/twardoch/html22text), which
is not yet on PyPI, so install from GitHub:

```bash
pip install "git+https://github.com/vexyart/vexy-mkdocs-text-export"
```

## How it works

The plugin runs at the very end of the build, on the fully rendered HTML — after
every other plugin has had its say. It hands that HTML to `html22text`, which
strips tags and reflows the content, and drops the result beside the page. A
theme handler adds a small "download as text" link to each page so readers can
find the export.

- **Plain text (`.txt`)** — the default. Tables, quotes, and images are flattened
  for reading and indexing.
- **Markdown (`.md`)** — set `markdown: true` to keep links and structure as
  portable Markdown.

## Next steps

- [Configuration options]({{ '/options' | relative_url }}) — every setting the
  plugin accepts.
- [Theme handlers]({{ '/theme-handlers' | relative_url }}) — how the download link
  is injected, and how to write your own handler.

## License

MIT. See the [LICENSE](https://github.com/vexyart/vexy-mkdocs-text-export/blob/main/LICENSE)
on GitHub.
