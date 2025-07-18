# Refactoring Plan: Splitting Large Code Files

This plan outlines a strategy for a junior software developer to split larger Python code files within the `mkdocs-text-export-plugin` project into smaller, more manageable units. The primary goal is to improve readability, maintainability, and testability without altering the existing functionality.

## Guiding Principles

*   **Single Responsibility Principle (SRP):** Each module or function should have one clear responsibility.
*   **Cohesion:** Group related code together.
*   **Loose Coupling:** Minimize dependencies between modules.
*   **Maintain Functionality:** All changes must preserve the existing behavior and pass all tests.
*   **Idiomatic Python:** Adhere to PEP 8 and common Python best practices.
*   **Clear Naming:** Use descriptive names for new files, modules, classes, and functions.

## Files to Refactor

Based on the `REFACTOR_FILELIST.txt` and analysis, the following files will be addressed:

1.  `./tests/test_plugin.py`
2.  `./mkdocs_text_export_plugin/plugin.py`
3.  `./mkdocs_text_export_plugin/renderer.py`
4.  `./mkdocs_text_export_plugin/themes/material.py` (Minor refactoring, primarily for consistency)
5.  `./docs/theme-handler/cinder.py` (Fixing existing issues and minor refactoring for clarity)

---

## Detailed Plan for Each File

### 1. Refactoring `./tests/test_plugin.py`

**Current State:** This file contains all unit tests for the `MdTxtExportPlugin` class, including tests for `on_config`, `on_nav`, and `on_post_page` methods, along with mock objects and fixtures. Its size (12 KB) suggests it can be logically segmented.

**Proposed Changes:** Split the tests into separate files based on the plugin's lifecycle events or the methods they test.

**Steps:**

1.  **Create New Test Files:**
    *   `./tests/test_plugin_config.py`: For tests related to `on_config` method and plugin configuration.
    *   `./tests/test_plugin_nav.py`: For tests related to `on_nav` method and navigation processing.
    *   `./tests/test_plugin_post_page.py`: For tests related to `on_post_page` method and page content processing.

2.  **Move Test Functions and Fixtures:**
    *   **`test_plugin_config.py`**:
        *   Move `test_on_config_defaults`
        *   Move `test_on_config_markdown_true`
        *   Move `test_on_config_enabled_if_env_set`
        *   Move `test_on_config_enabled_if_env_not_set`
        *   Move `plugin_config` fixture.
        *   Move `plugin` fixture (and ensure it correctly loads `plugin_config`).
        *   Move `mkdocs_config` fixture.
        *   Ensure `MdTxtExportPlugin`, `Config`, `config_options` are imported.
    *   **`test_plugin_nav.py`**:
        *   Move `test_on_nav`
        *   Move `test_on_nav_disabled`
        *   Move `MockNav` class.
        *   Move `MockPage` class.
        *   Move `MockFile` class.
        *   Move `mock_nav_fixture`.
        *   Ensure `MdTxtExportPlugin`, `Config`, `config_options` are imported, and `plugin`, `mkdocs_config` fixtures are available (either by re-defining them or importing if a shared `conftest.py` is set up later). For now, re-defining is simpler for a junior developer.
    *   **`test_plugin_post_page.py`**:
        *   Move `test_on_post_page_creates_file`
        *   Move `test_on_post_page_markdown_output`
        *   Move `test_on_post_page_disabled`
        *   Ensure `MockPage`, `MockFile`, `mock_nav_fixture` are available.
        *   Ensure `MdTxtExportPlugin`, `Config`, `config_options`, `Path` are imported.

3.  **Update Imports:** Adjust imports in the new test files to correctly reference `MdTxtExportPlugin` and other necessary components.

4.  **Remove Duplicates:** After moving, delete the moved functions and classes from the original `test_plugin.py`. The original `test_plugin.py` might become empty or contain only shared fixtures if any.

5.  **Verify:** Run `pytest` to ensure all tests still pass.

### 2. Refactoring `./mkdocs_text_export_plugin/plugin.py`

**Current State:** This file contains the core `MdTxtExportPlugin` class, handling configuration, event hooks (`on_config`, `on_nav`, `on_post_page`, `on_post_build`), and orchestrating the rendering process. The `on_post_page` method is quite dense.

**Proposed Changes:** Extract the logic for handling file paths and the `weasyprint.urls` dependency into a dedicated utility module.

**Steps:**

1.  **Create a New Utility Module:**
    *   `./mkdocs_text_export_plugin/utils.py`: This module will house helper functions.

2.  **Move `path2url` and Path Handling Logic:**
    *   In `plugin.py`, identify the lines related to `from weasyprint import urls` and `urls.path2url`.
    *   Create a function in `utils.py`, e.g., `get_base_url_from_paths(abs_dest_path: str, src_path: str) -> str`, that encapsulates this logic.
    *   **Crucially, address the `weasyprint` dependency:** As noted in `PLAN.md` and `TODO.md`, `weasyprint` is an unnecessary dependency if only `path2url` is used. Replace `weasyprint.urls.path2url` with `urllib.parse.urljoin` or `pathlib.Path.as_uri()` within the new utility function. `urllib.parse.urljoin` is generally more robust for creating URLs from paths.

    ```python
    # mkdocs_text_export_plugin/utils.py
    import os
    from urllib.parse import urljoin
    from pathlib import Path

    def get_base_url_from_paths(abs_dest_path: str, src_path: str) -> str:
        """
        Generates a base URL from absolute destination path and source path.
        Replaces weasyprint.urls.path2url to reduce dependencies.
        """
        path = os.path.dirname(abs_dest_path)
        filename = os.path.splitext(os.path.basename(src_path))[0]
        # Construct a file URL. pathlib.Path.as_uri() is a good alternative for local files.
        # For general web URLs, urljoin might be more appropriate if base_url is a web URL.
        # Given it's for local files, Path.as_uri() is cleaner.
        return Path(os.path.join(path, filename)).as_uri()

    # mkdocs_text_export_plugin/plugin.py (after refactoring)
    # ...
    # Remove: from weasyprint import urls
    from .utils import get_base_url_from_paths
    # ...
    # Inside on_post_page:
    # ...
    # base_url = urls.path2url(os.path.join(path, filename)) # OLD
    base_url = get_base_url_from_paths(abs_dest_path, src_path) # NEW
    # ...
    ```

3.  **Refactor `on_config` Logging Setup:**
    *   The logging setup in `on_config` is somewhat verbose. While not strictly a "split," it can be made cleaner.
    *   Consider moving the logging configuration into a separate helper function or a dedicated `logging_setup.py` if it becomes more complex, but for now, just simplifying it within `on_config` is sufficient.

4.  **Update Imports:** Ensure `plugin.py` imports from `utils.py` and removes the `weasyprint` import.

5.  **Verify:** Run `pytest` to ensure all tests still pass.

### 3. Refactoring `./mkdocs_text_export_plugin/renderer.py`

**Current State:** The `Renderer` class handles the core conversion and theme handler loading. The `_load_theme_handler` method is a static method that handles file system operations and module loading.

**Proposed Changes:** Extract the theme handler loading logic into a separate utility function or module, especially if the loading mechanism becomes more complex (e.g., handling multiple custom handler paths, caching).

**Steps:**

1.  **Create a New Utility Module:**
    *   `./mkdocs_text_export_plugin/theme_loader.py`: This module will contain functions related to loading theme handlers.

2.  **Move `_load_theme_handler`:**
    *   Move the `_load_theme_handler` static method from `renderer.py` to `theme_loader.py`.
    *   Rename it to a more descriptive function name, e.g., `load_theme_handler(theme: str, custom_handler_path: str = None)`.
    *   Ensure all necessary imports (`logging`, `os`, `import_module`, `spec_from_file_location`, `module_from_spec`, `generic_theme`) are present in `theme_loader.py`.

3.  **Update `Renderer` Class:**
    *   In `renderer.py`, remove the `_load_theme_handler` method.
    *   Update the `__init__` method to call the new `load_theme_handler` function from `theme_loader.py`.

    ```python
    # mkdocs_text_export_plugin/theme_loader.py
    import logging
    import os
    from importlib import import_module
    from importlib.util import module_from_spec, spec_from_file_location

    from .themes import generic as generic_theme

    def load_theme_handler(theme: str, custom_handler_path: str = None):
        module_name = "." + (theme or "generic").replace("-", "_")

        if custom_handler_path:
            try:
                spec = spec_from_file_location(
                    module_name, os.path.join(os.getcwd(), custom_handler_path)
                )
                mod = module_from_spec(spec)
                spec.loader.exec_module(mod)
                return mod
            except FileNotFoundError as e:
                logging.warning(
                    f'Could not load theme handler {theme} from custom directory "{custom_handler_path}": {e}'
                )

        try:
            return import_module(module_name, "mkdocs_text_export_plugin.themes")
        except ImportError as e:
            logging.warning(f"Could not load theme handler {theme}: {e}")
            return generic_theme

    # mkdocs_text_export_plugin/renderer.py (after refactoring)
    # ...
    from .theme_loader import load_theme_handler
    # ...
    class Renderer:
        def __init__(self, ...):
            # ...
            self.theme = load_theme_handler(theme, theme_handler_path) # OLD: self._load_theme_handler(...)
            # ...
    ```

4.  **Verify:** Run `pytest` to ensure all tests still pass.

### 4. Refactoring `./mkdocs_text_export_plugin/themes/material.py`

**Current State:** This file contains `get_stylesheet` and `modify_html` functions. The `modify_html` function constructs an SVG icon string directly within the Python code.

**Proposed Changes:** While the file itself is not excessively large, the SVG string can be moved to a separate constant or a small data file if it becomes more complex or if other icons are introduced. For now, a minor refactoring to improve readability is sufficient.

**Steps:**

1.  **Extract SVG to a Constant:**
    *   Define the SVG string as a module-level constant within `material.py` to improve readability of the `modify_html` function.

    ```python
    # mkdocs_text_export_plugin/themes/material.py
    # ...
    DOWNLOAD_ICON_SVG = '<svg style="height: 1.2rem; width: 1.2rem;" viewBox="0 0 384 512" xmlns="http://www.w3.org/2000/svg"><path d="M224 136V0H24C10.7 0 0 10.7 0 24v464c0 13.3 10.7 24 24 24h336c13.3 0 24-10.7 24-24V160H248c-13.2 0-24-10.8-24-24zm76.45 211.36l-96.42 95.7c-6.65 6.61-17.39 6.61-24.04 0l-96.42-95.7C73.42 337.29 80.54 320 94.82 320H160v-80c0-8.84 7.16-16 16-16h32c8.84 0 16 7.16 16 16v80h65.18c14.28 0 21.4 17.29 11.27 27.36zM377 105L279.1 7c-4.5-4.5-10.6-7-17-7H256v128h128v-6.1c0-6.3-2.5-12.4-7-16.9z"></path></svg>'

    def modify_html(html: str, href: str) -> str:
        a_tag = (
            '<a class="md-content__button md-icon" download href="%s" title="Text export">'
            % href
        )
        button_tag = a_tag + DOWNLOAD_ICON_SVG + "</a>" # Use the constant here
        # ...
    ```

2.  **Verify:** No functional change, so existing tests (if any) should still pass.

### 5. Refactoring `./docs/theme-handler/cinder.py`

**Current State:** This file is an *example* custom theme handler provided in the documentation. It has syntax errors (duplicate `return str(soup)`) and malformed `get_stylesheet` function (it attempts to parse `html` which is not a parameter). It also contains commented-out example modifications.

**Proposed Changes:** Fix the syntax errors, correct the `get_stylesheet` function, and clean up the example to be a clear, working template for users. This is more of a fix and cleanup than a splitting, but it's important for the project's quality.

**Steps:**

1.  **Fix `get_stylesheet`:**
    *   Remove the `soup = BeautifulSoup(html, "html.parser")` line and all subsequent commented-out example modifications from `get_stylesheet`. This function should only return a string.

2.  **Fix `modify_html`:**
    *   Remove the duplicate `return str(soup)` at the end of the `modify_html` function.

3.  **Clean Up Comments:**
    *   Ensure comments clearly explain the purpose of the file and how to use it as an example.

    ```python
    # docs/theme-handler/cinder.py (after fixes)
    from bs4 import BeautifulSoup

    def get_stylesheet() -> str:
        return """
        body > .container {
            margin-top: -100px;
        }
        @page {
            @bottom-left {
                content: counter(__pgnum__);
            }
            size: letter;
        }
        @media print {
            .noprint {
                display: none;
            }
        }
        """

    def modify_html(html: str, href: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        sm_wrapper = soup.new_tag("small")

        a = soup.new_tag("a", href=href, title="Text export", download=None)
        a["class"] = "txt-download"
        a.string = "Open text"

        sm_wrapper.append(a)
        if soup.body:
            footer = getattr(soup.body, 'footer', None)
            if footer:
                footer.insert(0, sm_wrapper)

        return str(soup) # Only one return statement here
    ```

4.  **Verify:** Manually inspect the file to ensure it's syntactically correct and serves as a clear example.

---

## General Verification Steps After Each Refactoring

After completing the refactoring for each file or logical group of changes, the junior developer should perform the following:

1.  **Run Tests:** Execute `pytest` from the project root to ensure no regressions were introduced.
    ```bash
    pytest
    ```
2.  **Run Linters/Formatters:**
    ```bash
    black --check .
    flake8 .
    mypy . --exclude venv --exclude docs/theme-handler/cinder.py --ignore-missing-imports
    ```
    Fix any issues reported.
3.  **Build Documentation (if applicable):** If changes affect the documentation, build the MkDocs site to ensure it still functions correctly.
    ```bash
    mkdocs build
    ```
4.  **Manual Inspection:** Review the changed code and the surrounding files to ensure consistency and adherence to the guiding principles.

This systematic approach will help the junior developer safely and effectively split the codebase while maintaining its integrity.
