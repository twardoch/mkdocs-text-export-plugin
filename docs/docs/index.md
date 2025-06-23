# MkDocs Text Export Plugin

Welcome to the documentation for the `mkdocs-text-export-plugin`. This plugin allows you to export your MkDocs pages to either plain text or simplified Markdown format.

## Overview

The plugin works by taking the final HTML rendered by MkDocs (after all other plugins have done their work) and converting it. This is particularly useful for:

- Generating plain text versions of your site for Natural Language Processing (NLP), indexing, or accessibility.
- Creating simplified Markdown versions that are stripped of complex MkDocs-specific syntax or HTML, which can be useful for content migration or re-purposing.

It uses the [`html22text`](https://github.com/twardoch/html22text) library for the core conversion and allows for theme-specific adjustments via [Custom Theme Handlers](theme_handlers.md).

## Key Features

- Export to plain text (`.txt`) or Markdown (`.md`).
- Configurable options for fine-tuning the output.
- Ability to use custom theme handlers for precise control over HTML pre-processing.
- Option to enable/disable the plugin via an environment variable.

## Installation

Install the plugin from PyPI using pip:

```bash
pip install mkdocs-text-export-plugin
```

Then, add the plugin to your `mkdocs.yml` file. It's recommended to place it late in the plugin list:

```yaml
plugins:
  - search # Example
  # - other_plugins_you_use
  - text-export
```

> **Note:** If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set, but now you have to enable it explicitly if you add a `plugins` section.

For detailed configuration, see the [Configuration Options](options.md) page.

## Requirements

- Python >= 3.10
- MkDocs >= 1.3.0 (though likely works with >=1.0)
- Key dependencies: `html22text`, `beautifulsoup4`

## Contributing

Contributions are welcome! Please refer to the main [README.md on GitHub](https://github.com/twardoch/mkdocs-text-export-plugin#contributing) for guidelines on reporting bugs, requesting features, or submitting pull requests.

## License

This plugin is licensed under the MIT License. See the [LICENSE file on GitHub](https://github.com/twardoch/mkdocs-text-export-plugin/blob/master/LICENSE) for more details.

## Acknowledgements

This plugin builds upon ideas and code from earlier projects, including:
- `mkdocs-pdf-export-plugin`
- Work by Stephan Hauser and Lukas Geiter in the MkDocs plugin ecosystem.
This current version has been significantly refactored and modernized.