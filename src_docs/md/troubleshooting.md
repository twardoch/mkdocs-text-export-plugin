# Troubleshooting

## No text files appear

Check these causes in order.

1. **The plugin is not in the `plugins` list.** Run `mkdocs build` and look for
   `.txt` files next to the `.html` files in `site/`. If there are none, check
   that `mkdocs.yml` lists `text-export` under `plugins`.
2. **`enabled_if_env` is set.** The build prints
   `Text export is disabled (set environment variable <NAME> to 1 to enable)`.
   Set the variable to exactly `1`: `<NAME>=1 mkdocs build`.
3. **You are looking for the wrong file name.** The text file is named after the
   source file. `docs/guide/setup.md` produces
   `site/guide/setup/setup.txt`, not `site/guide/setup/index.txt`.

## The text contains the site menu, search dialog and footer

The plugin converts the whole HTML document. Remove the theme's navigation with
`kill_tags`. For the default `mkdocs` theme:

```yaml
plugins:
  - text-export:
      kill_tags: [.navbar, .col-md-3, .modal, footer]
```

For other themes, open a built `.html` file and pick selectors for the elements
that wrap the menus. See [Configuration](configuration.md#kill_tags).

## `Could not load theme handler …`

The build prints, for example:

```text
Could not load theme handler readthedocs: No module named 'mkdocs_text_export_plugin.themes.readthedocs'
```

The plugin has no handler for your theme and uses the generic one, which adds a
hidden `<head>` link. The text files are still written. To get a visible link,
write a [custom handler](theme-handlers.md#write-your-own-handler).

The message does not count as a warning, so `mkdocs build --strict` still
succeeds.

## `Could not load theme handler … from custom directory …`

The file named in `theme_handler_path` was not found. The path is resolved
against the folder you run `mkdocs` from. Either run `mkdocs` from the project
folder, or give a path that is correct from where you run it.

## `Error converting <page> to text: …`

The conversion or the theme handler raised an exception for that page. The page
HTML is kept as it was, and the build goes on. At the end the build prints
`<n> conversion errors occurred (see above)`.

A common cause is a custom handler without a `modify_html` function:

```text
Error converting index.md to text: module '.mkdocs' has no attribute 'modify_html'
```

## Struck-through text is still in the output

`hide_strikethrough` does not remove `<del>` or `<s>` content in MkDocs output.
Add the tags to `kill_tags`:

```yaml
plugins:
  - text-export:
      kill_tags: [del, s]
```

## `plain_tables` changes nothing

The option is accepted but not used by the converter. Tables are always written
in `html2text`'s table format.

## Image paths in Markdown output point to my disk

In Markdown mode, image URLs are made absolute against the page's output folder
on the build machine. Rewrite them after the build if you publish the `.md`
files.

## The Material download button is missing

The `material` handler only runs when `theme.name` is `material`, and only
finds its insertion point if the page contains
`<article class="md-content__inner md-typeset">` exactly. Other theme names,
including `materialx`, get the hidden head link instead.
