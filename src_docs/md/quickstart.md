# Quick start

This page adds the plugin to an existing MkDocs site and checks the files it
writes.

## Prerequisites

- An MkDocs site with a `mkdocs.yml` file and a `docs/` folder.
- The plugin installed in the same environment as MkDocs (see
  [Installation](installation.md)).

## Add the plugin

1. Open `mkdocs.yml`.
2. Add `text-export` to the `plugins` list. Put it last, so it sees the HTML
   after every other plugin has changed it:

    ```yaml
    plugins:
      - search
      - text-export
    ```

    When you add a `plugins` list, MkDocs no longer enables `search` for you,
    so keep `search` in the list if you want it.

3. Build the site:

    ```bash
    mkdocs build
    ```

MkDocs writes the site into `site/`, and the plugin adds one `.txt` file per page.

## Follow one page through the build

Say `docs/index.md` contains:

```markdown
# Welcome

This is **bold**, _italic_ and a [link to the guide](guide/setup.md).

> A short quote.

| Name | Value |
|------|-------|
| a    | 1     |
```

After `mkdocs build` with the default `mkdocs` theme, `site/index.txt` contains
this text, below the site navigation (shortened here):

```text
# Welcome

This is bold, italic and a link to the guide.

> A short quote.

Name | Value  
---|---  
a | 1  
```

What happened:

- Bold and italic markers were dropped, because plain-text mode turns off
  emphasis.
- The link kept its text and lost its URL.
- Headings and block quotes kept their `#` and `>` markers. They come from
  `html2text`, which writes these even in plain-text mode.
- The table became a pipe-separated table.

`site/index.html` now also contains
`<link href="index.txt" rel="alternate" title="Text export"/>` in its `<head>`.

## Remove the site navigation from the text

The plugin converts the whole HTML document, so the theme's navigation bar,
search dialog and footer appear in the text as well. Remove them with
`kill_tags`, which takes CSS selectors:

```yaml
plugins:
  - search
  - text-export:
      kill_tags:
        - .navbar
        - .col-md-3
        - .modal
        - footer
```

With these four selectors and the default `mkdocs` theme, `site/index.txt`
starts directly with `# Welcome`. `.navbar` is the top bar, `.col-md-3` the
table-of-contents sidebar, `.modal` the search and keyboard-shortcut dialogs, and
`footer` the page footer.

The selectors depend on the theme. For another theme, open one built `.html`
file and look for the elements that wrap the navigation.

## Export Markdown instead

Set `markdown: true`:

```yaml
plugins:
  - text-export:
      markdown: true
```

The plugin then writes `index.md` instead of `index.txt`, and keeps links,
emphasis, images and tables as Markdown. See [Output format](output.md).

## Export only in some builds

To export only when an environment variable is set, name the variable in
`enabled_if_env`:

```yaml
plugins:
  - text-export:
      enabled_if_env: ENABLE_TEXT_EXPORT
```

```bash
ENABLE_TEXT_EXPORT=1 mkdocs build   # writes the text files
mkdocs build                        # skips the export
```

When the variable is missing or not exactly `1`, the plugin prints
`Text export is disabled (set environment variable ENABLE_TEXT_EXPORT to 1 to enable)`
and does nothing else.
