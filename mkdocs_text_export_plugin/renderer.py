# this_file: mkdocs_text_export_plugin/renderer.py
"""Convert rendered page HTML to text and load the matching theme handler.

:class:`Renderer` is a thin wrapper around ``html22text`` (vendored in
``_vendor/html22text``): it maps the plugin's config options onto that library's
arguments and picks a theme handler that knows how to inject the download link
for the site's active MkDocs theme.
"""

import logging
import os
from importlib import import_module
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType

from ._vendor.html22text import html22text
from .themes import generic as generic_theme

log = logging.getLogger(__name__)


class Renderer:
    """Render page HTML to text/Markdown and delegate link injection to a theme."""

    def __init__(
        self,
        theme: str,
        theme_handler_path: str | None = None,
        markdown: bool = False,
        plain_tables: bool = False,
        open_quote: str = "“",
        close_quote: str = "”",
        default_image_alt: str = "",
        hide_strikethrough: bool = False,
        kill_tags: list[str] | None = None,
        file_ext: str = "txt",
    ) -> None:
        self.page_order: list[str] = []
        self.pages: list = []
        self.markdown: bool = markdown
        self.plain_tables: bool = plain_tables
        self.open_quote: str = open_quote
        self.close_quote: str = close_quote
        self.default_image_alt: str = default_image_alt
        self.hide_strikethrough: bool = hide_strikethrough
        self.kill_tags: list[str] = kill_tags if kill_tags is not None else []
        self.theme = self._load_theme_handler(theme, theme_handler_path)
        self.file_ext: str = file_ext

    def write_txt(self, content: str, base_url: str, filename: str) -> None:
        """Render ``content`` and write it to ``filename``."""
        Path(filename).write_text(self.render_doc(content, base_url))

    def render_doc(self, content: str, base_url: str = "") -> str:
        """Convert one page's HTML into plain text or Markdown via html22text."""
        # html22text wants kill_tags as a comma-separated string, not a list.
        kill_tags_str = ",".join(self.kill_tags) if self.kill_tags else None

        return html22text(
            html_content=content,
            markdown=self.markdown,
            base_url=base_url,
            open_quote=self.open_quote,
            close_quote=self.close_quote,
            default_image_alt=self.default_image_alt,
            kill_strikethrough=self.hide_strikethrough,
            kill_tags=kill_tags_str,
            file_ext_override=self.file_ext if self.markdown else "",
        )

    def add_doc(self, content: str, base_url: str, rel_url: str) -> None:
        """Record a page's converted content in navigation order."""
        pos = self.page_order.index(rel_url)
        self.pages[pos] = (content, base_url, rel_url)

    def add_link(self, content: str, filename: str) -> str:
        """Insert the theme-specific "download as text" link into the page HTML."""
        return self.theme.modify_html(content, filename)

    @staticmethod
    def _load_theme_handler(theme: str, custom_handler_path: str | None = None) -> ModuleType:
        """Resolve the theme handler module for ``theme``.

        A ``custom_handler_path`` (relative to the CWD) wins if it loads; otherwise
        a built-in handler named after the theme is imported, falling back to the
        generic handler when the theme has no dedicated module.
        """
        module_name = "." + (theme or "generic").replace("-", "_")

        if custom_handler_path:
            try:
                spec = spec_from_file_location(
                    module_name, os.path.join(os.getcwd(), custom_handler_path)
                )
                mod = module_from_spec(spec)  # type: ignore[arg-type]
                spec.loader.exec_module(mod)  # type: ignore[union-attr]
                return mod
            except FileNotFoundError as e:
                log.warning(
                    f'Could not load theme handler {theme} from custom directory "{custom_handler_path}": {e}'
                )

        try:
            return import_module(module_name, "mkdocs_text_export_plugin.themes")
        except ImportError as e:
            log.warning(f"Could not load theme handler {theme}: {e}")
            return generic_theme
