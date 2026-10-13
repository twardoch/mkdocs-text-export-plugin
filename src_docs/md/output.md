# Output format

This page shows what the plugin writes for one sample page, in both modes, and
explains where each part of the output comes from.

## File names and locations

For each page in the navigation, the plugin writes one file into the folder that
holds the page's HTML. The file name is the source file name with a new
extension:

| Source file | HTML file (`use_directory_urls: true`) | Text file |
|---|---|---|
| `docs/index.md` | `site/index.html` | `site/index.txt` |
| `docs/guide/setup.md` | `site/guide/setup/index.html` | `site/guide/setup/setup.txt` |

With `markdown: true`, the extension is `.md` instead of `.txt`.

The plugin then adds a link to the text file into the HTML page. The link target
is the bare file name (`setup.txt`), which works because both files sit in the
same folder.

## Sample page

The examples below use this source file, `docs/index.md`:

```markdown
# Welcome

This is **bold**, _italic_ and a [link to the guide](guide/setup.md).

> A short quote.

Inline <q>quoted</q> text and ~~gone~~ <del>deleted</del> text.

![Logo](logo.png)

| Name | Value |
|------|-------|
| a    | 1     |
```

The site uses the default `mkdocs` theme, and `kill_tags` removes the theme's
navigation (`.navbar`, `.col-md-3`, `.modal`, `footer`).

## Plain-text output

`site/index.txt`:

```text
# Welcome

This is bold, italic and a link to the guide.

> A short quote.

Inline “quoted” text and ~~gone~~ ~~deleted~~ text.

Name | Value  
---|---  
a | 1  
```

In plain-text mode the plugin configures `html2text` to:

- drop emphasis markers, so `**bold**` becomes `bold`;
- keep link text and drop link targets;
- remove images, including their alt text;
- replace `<q>` with `open_quote` and `close_quote`;
- write tables as pipe-separated rows without padding;
- write list items with plain indentation and code blocks as indented text;
- never wrap lines.

Headings still start with `#` and block quotes with `>`, because `html2text`
writes those markers in every mode.

## Markdown output

With `markdown: true`, `site/index.md` contains (the image path is shortened):

```markdown
# Welcome

This is **bold** , _italic_ and a [link to the guide](<guide/setup/>).

> A short quote.

Inline “quoted” text and ~~gone~~ ~~deleted~~ text.

![Logo](/…/site/logo.png)

| Name | Value |
|------|-------|
| a    | 1     |
```

In Markdown mode the plugin:

- keeps bold (`**`) and italic (`_`) markers;
- keeps links inline, wrapped in angle brackets: `[text](<url>)`;
- rewrites relative links that end in `.html` or `.htm` so they end in `.md`;
- keeps images and turns their `src` into an absolute path, resolved against the
  page's location in the output folder on disk;
- pads tables so the columns line up;
- wraps code blocks in `[code]` and `[/code]` lines;
- uses `-` for bullet list items.

!!! note
    With `use_directory_urls: true` (the MkDocs default), MkDocs writes page links
    as folder URLs such as `guide/setup/`. Those links do not end in `.html`, so
    the `.md` rewrite does not apply to them.

!!! warning
    Image paths in Markdown output point to the build machine's file system, for
    example `/home/runner/work/site/logo.png`. If you publish the `.md` files,
    rewrite those paths afterwards.

## Elements that become plain text

In both modes, `<mark>` and `<kbd>` elements are replaced by their text, so
`<kbd>Ctrl</kbd>` becomes `Ctrl`.

## Empty pages

If a page converts to nothing but whitespace, the plugin writes an empty file.
