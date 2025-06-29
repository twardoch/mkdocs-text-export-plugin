# `mkdocs-text-export-plugin`

**Convert your MkDocs documentation pages to clean Markdown or plain text effortlessly.**

`mkdocs-text-export-plugin` is an MkDocs plugin that processes the fully rendered HTML of your documentation site. It leverages the powerful [`html22text`](https://github.com/twardoch/html22text) library, along with theme-specific adjustments, to extract either a plain-text or a simplified Markdown representation of your content.

This plugin is ideal for:

*   **Content Creators & Technical Writers:** Generate simplified Markdown from complex MkDocs setups (e.g., those using multiple plugins for includes, snippets, or macros) for easier content reuse or migration.
*   **Developers & Researchers:** Create plain-text versions of documentation for natural language processing (NLP), content indexing, search engine optimization (SEO), or simply for quick, offline consumption.
*   **Anyone using MkDocs:** If you need a text-based version of your beautifully rendered MkDocs site, this plugin is for you.

**Key Benefits:**

*   **Accurate Conversion:** Works on the final HTML output, ensuring that what you see in the browser is what gets converted.
*   **Flexible Output:** Choose between plain text (`.txt`) for maximum simplicity or simplified Markdown (`.md`) for a structured text format.
*   **Highly Configurable:** Fine-tune the conversion process with various options inherited from `html22text` and plugin-specific settings.
*   **Theme Aware (Basic):** Includes basic support for common MkDocs themes and allows for custom theme handlers to optimize output for specific site structures.
*   **Easy Integration:** Simple to install and add to your MkDocs project.

## Features

*   Exports pages to either plain text (`.txt`) or simplified Markdown (`.md`).
*   Processes the final HTML rendered by MkDocs and other plugins.
*   Utilizes `html22text` for robust HTML-to-text conversion.
*   Offers options to control table formatting, image handling, quote characters, and more.
*   Allows specifying HTML tags whose content should be entirely removed (e.g., `<script>`, `<style>`).
*   Adds a `<link rel="alternate">` tag to the HTML `<head>` of each page, pointing to its text/Markdown export, improving discoverability.
*   Can be conditionally enabled/disabled using an environment variable.
*   Provides basic handlers for common MkDocs themes (e.g., `mkdocs`, `material`) and supports custom theme handlers for tailored output.
*   Verbose logging option for troubleshooting.

## Installation

Install the plugin using pip:

```bash
pip install mkdocs-text-export-plugin
```

Ensure you have MkDocs installed as well.

## Usage

1.  Add `text-export` to the `plugins` section of your `mkdocs.yml` file.
2.  It's generally recommended to place `text-export` towards the **end** of the plugin list. This allows it to process the HTML output after other plugins (e.g., for search, navigation, content manipulation) have completed their modifications.

### Basic Configuration

Here's a minimal example for your `mkdocs.yml`:

```yaml
site_name: "My Awesome Documentation"
nav:
  - Home: index.md
  - About: about.md

plugins:
  - search                 # Example: search plugin
  - another-plugin         # Example: another plugin
  - text-export:
      markdown: false      # Set to true for .md output, false for .txt
```

### Output Files

*   If `markdown: false` (default), the plugin generates a `.txt` file for each page.
*   If `markdown: true`, it generates an `.md` file for each page.

These files are placed in the same directory structure as the original HTML files within your `site_dir` (usually `site/`). For example, if you have a page `docs/topic/page.md` which renders to `site/topic/page/index.html`, the text export will be `site/topic/page/index.txt` (or `.md`).

The plugin also attempts to add a `<link rel="alternate" type="text/plain" title="Plain text" href="...">` (or `text/markdown`) tag to the `<head>` of each HTML page, pointing to its corresponding text or Markdown export.

## Configuration Options

You can customize the plugin's behavior by adding options under `text-export` in your `mkdocs.yml`:

```yaml
plugins:
  - text-export:
      # --- General Options ---
      enabled_if_env: MY_ENV_VARIABLE  # Optional: Only enable the plugin if the environment
                                       # variable MY_ENV_VARIABLE is set to "1".
                                       # Default: null (plugin is always enabled)

      verbose: false                   # Set to true for detailed plugin logging.
                                       # Default: false

      # --- Output Format ---
      markdown: false                  # If true, exports to simplified Markdown (.md).
                                       # If false, exports to plain text (.txt).
                                       # Default: false

      # --- Plain Text Specific Options (used when markdown: false) ---
      plain_tables: false              # If true, uses a simpler list-like format for tables
                                       # instead of ASCII art tables in plain text.
                                       # Default: false

      default_image_alt: ""            # If non-empty, replaces all images with this alt text
                                       # in plain text mode. If empty, images are typically
                                       # converted to their actual alt text or a link.
                                       # Default: ""

      # --- Markdown & Plain Text Common Options (passed to html22text) ---
      open_quote: "“"                  # Character for the opening <q> tag.
                                       # Default: "“"

      close_quote: "”"                 # Character for the closing <q> tag.
                                       # Default: "”"

      hide_strikethrough: false        # If true, removes content enclosed in <s> or <del> tags.
                                       # Default: false

      kill_tags:                       # List of HTML tags whose content will be completely removed.
        - script                       # Example: remove all <script> tags and their content
        - style                        # Example: remove all <style> tags and their content
        # - pre                        # Uncomment to remove preformatted text blocks
        # - figure                     # Uncomment to remove figures
        # - .admonition-title          # Example: remove admonition titles by CSS selector (requires html22text support for selectors)
                                       # Default: [] (empty list)

      # --- Theme Handling ---
      theme_handler_path: ""           # Path to a custom Python script for theme-specific HTML
                                       # modifications before text conversion.
                                       # Example: "custom_handlers/my_theme_tweaks.py"
                                       # See "Custom Theme Handlers" section for details.
                                       # Default: "" (use built-in theme handlers)
```

---

## Part 2: Technical Documentation & Contribution Guide

### How It Works

The `mkdocs-text-export-plugin` integrates into the MkDocs build process using standard plugin events:

1.  **`on_config`**:
    *   Initializes plugin configuration from `mkdocs.yml`.
    *   Sets up logging verbosity.
    *   Checks the `enabled_if_env` condition. If the specified environment variable is not set to "1", the plugin disables itself.
    *   Determines the output file extension (`.txt` or `.md`) based on the `markdown` option.

2.  **`on_nav`**:
    *   If enabled, initializes the `Renderer` instance.
    *   The `Renderer` is configured with options from `mkdocs.yml` and the current MkDocs theme name.
    *   It attempts to load a theme-specific handler (see "Theme Handling" below).
    *   It records the order of pages in the navigation for later use (though this specific feature seems less critical for the current export functionality).

3.  **`on_post_page`**:
    *   This is the core conversion step, triggered after each page's HTML is rendered.
    *   If enabled, the plugin takes the `output_content` (HTML of the page).
    *   It determines the source and destination paths for the output file.
    *   The `Renderer.write_txt()` method is called:
        *   This method uses `html22text()` to convert the HTML string to either plain text or Markdown, applying all relevant formatting options (`plain_tables`, `open_quote`, `kill_tags`, etc.).
        *   The resulting text is written to the corresponding `.txt` or `.md` file in the `site_dir`.
    *   The `Renderer.add_link()` method is called:
        *   This method, typically via a theme handler, modifies the original HTML `output_content` to insert a `<link rel="alternate">` tag in the `<head>`, pointing to the newly created text file.
    *   Errors during conversion are logged.

4.  **`on_post_build`**:
    *   If enabled, logs the total number of files converted, total time taken, and any errors that occurred.

**Core Conversion Engine: `html22text`**

The actual HTML-to-text (or Markdown) conversion is performed by the [`html22text`](https://github.com/twardoch/html22text) library. This plugin acts as a bridge between MkDocs and `html22text`, configuring it based on your `mkdocs.yml` and handling the file I/O within the MkDocs build lifecycle. Most of the conversion logic and options like `plain_tables`, `hide_strikethrough`, `kill_tags`, etc., are features of `html22text`.

**HTML Manipulation: `BeautifulSoup4`**

Theme handlers (see below) use `BeautifulSoup4` to parse and modify the HTML content, primarily to inject the `<link rel="alternate">` tag.

### Theme Handling

The plugin aims to correctly insert the `<link rel="alternate">` tag into the HTML of various MkDocs themes.

*   **Built-in Handlers:** It includes basic handlers for common themes like `mkdocs` (generic), `material`, and `cinder`. These handlers know where to best inject the link tag for those themes.
*   **Loading Logic:** The `Renderer` attempts to load a handler based on `config["theme"].name`. If a specific handler (e.g., `material.py`) isn't found, it falls back to `generic.py`.
*   **`modify_html(html: str, href: str) -> str` function:** This is the primary function within a theme handler file. It receives the page's HTML content and the URL of the exported text file. Its job is to parse the HTML, add the `<link>` tag appropriately, and return the modified HTML.
*   **`get_stylesheet()` function:** While present in theme handler examples (likely inherited from patterns in plugins like `mkdocs-pdf-export-plugin`), this function is **not currently used** by `mkdocs-text-export-plugin` for its core text export functionality, as CSS styling is irrelevant to plain text or basic Markdown output.

**Custom Theme Handlers:**

If the default link insertion doesn't work well with your specific theme, or if you need other theme-specific HTML modifications before text conversion (though `kill_tags` is often sufficient), you can provide a custom theme handler.

1.  Create a Python script (e.g., `my_custom_handler.py`).
2.  This script should define at least the `modify_html(html: str, href: str) -> str` function. You can refer to `mkdocs_text_export_plugin/themes/generic.py` or `docs/theme-handler/cinder.py` for an example structure.
3.  In your `mkdocs.yml`, set the `theme_handler_path` option to the path of your script:

    ```yaml
    plugins:
      - text-export:
          theme_handler_path: "path/to/your/my_custom_handler.py"
    ```

    The path should be relative to your MkDocs project root (where `mkdocs.yml` is located).

### Dependencies

Key dependencies include:

*   **MkDocs:** The documentation generator this plugin extends.
*   **`html22text`:** The core library for HTML to text/Markdown conversion.
*   **`BeautifulSoup4`:** Used for HTML parsing and manipulation within theme handlers.
*   **`weasyprint`:** (Indirectly used via `from weasyprint import urls` for `path2url` utility in `plugin.py`). This seems like a potentially heavy dependency if only `path2url` is used. *Developer Note: Consider replacing with `pathlib.Path.as_uri()` or `urllib.parse.urljoin` if feasible to reduce dependency footprint, though `html22text` itself might pull `weasyprint`.*

### Development & Testing

This project uses standard Python development tools.

**Prerequisites:**

*   Python (>=3.10, as specified in `setup.py` and CI)
*   `pip` for installing dependencies.

**Setup:**

1.  Clone the repository.
2.  It's recommended to create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  Install dependencies, including development dependencies:
    ```bash
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    pip install -e .  # Install the plugin in editable mode
    ```

**Running Tests:**

The project uses `pytest` for testing.

```bash
pytest
```

Tests cover plugin configuration, file generation for both text and Markdown modes, and behavior when enabled/disabled.

**Code Style & Linting:**

*   **Black:** For code formatting. Check with `black --check .`. Apply formatting with `black .`.
*   **Flake8:** For linting. Run with `flake8 .`.
*   **MyPy:** For static type checking. Run with `mypy . --exclude venv --exclude docs/theme-handler/cinder.py --ignore-missing-imports`.

These checks are also part of the CI pipeline (see `.github/workflows/ci.yml`).

### Contributing

Contributions are highly welcome! Whether it's a bug report, a feature request, or a pull request, your input is valuable.

1.  **Check Existing Issues:** Before submitting a new issue or PR, please search the [issue tracker](https://github.com/twardoch/mkdocs-text-export-plugin/issues) to see if your concern or idea has already been discussed.
2.  **Open an Issue:** For bugs, provide detailed steps to reproduce. For features, clearly describe the proposed functionality and its use case.
3.  **Pull Requests:**
    *   For significant changes, it's best to open an issue first to discuss the approach.
    *   Ensure your code adheres to the project's style (run `black .` and `flake8 .`).
    *   Add tests for any new features or bug fixes.
    *   Make sure all tests pass (`pytest`).
    *   Update documentation (README.md, docstrings) if your changes affect usage or functionality.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

The development of this plugin was inspired by and based on the foundational work of several other projects and individuals:

*   [mkdocs-pdf-export-plugin](https://github.com/zhaoterryy/mkdocs-pdf-export-plugin/) by [Terry Zhao](https://github.com/zhaoterryy)
*   The work of [Stephan Hauser][shauser]
*   [mkdocs-awesome-pages-plugin][awesome-pages-plugin] by [Lukas Geiter][lukasgeiter]

This version has been further developed and may include significant modifications from the original concepts.

[shauser]: https://github.com/shauser
[awesome-pages-plugin]: https://github.com/lukasgeiter/mkdocs-awesome-pages-plugin
[lukasgeiter]: https://github.com/lukasgeiter
