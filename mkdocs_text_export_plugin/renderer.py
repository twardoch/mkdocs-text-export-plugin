import logging
import os
from importlib import import_module
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from html22text import html22text

from .themes import generic as generic_theme


class Renderer:
    def __init__(
        self,
        theme: str,
        theme_handler_path: str = None,  # type: ignore
        markdown: bool = False,
        plain_tables: bool = False,
        open_quote: str = "“",
        close_quote: str = "”",
        default_image_alt: str = "",
        hide_strikethrough: bool = False,
        kill_tags: list = [],  # type: ignore
        file_ext: str = "txt",
    ):
        self.page_order: list = []
        self.pages: list = []
        self.markdown: bool = markdown
        self.plain_tables: bool = plain_tables
        self.open_quote: str = open_quote
        self.close_quote: str = close_quote
        self.default_image_alt: str = default_image_alt
        self.hide_strikethrough: bool = hide_strikethrough
        self.kill_tags: list = kill_tags
        self.theme = self._load_theme_handler(theme, theme_handler_path)
        self.file_ext: str = file_ext

    def write_txt(self, content: str, base_url: str, filename: str):
        Path(filename).write_text(self.render_doc(content, base_url))

    def render_doc(self, content: str, base_url: str = ""):
        # Convert kill_tags list to comma-separated string if needed
        kill_tags_str = None
        if self.kill_tags:
            kill_tags_str = ",".join(self.kill_tags)

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

    def add_doc(self, content: str, base_url: str, rel_url: str):
        pos = self.page_order.index(rel_url)
        self.pages[pos] = (content, base_url, rel_url)

    def add_link(self, content: str, filename: str):
        return self.theme.modify_html(content, filename)

    @staticmethod
    def _load_theme_handler(theme: str, custom_handler_path: str = None):  # type: ignore
        module_name = "." + (theme or "generic").replace("-", "_")

        if custom_handler_path:
            try:
                spec = spec_from_file_location(
                    module_name, os.path.join(os.getcwd(), custom_handler_path)
                )
                mod = module_from_spec(spec)  # type: ignore
                spec.loader.exec_module(mod)  # type: ignore
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
