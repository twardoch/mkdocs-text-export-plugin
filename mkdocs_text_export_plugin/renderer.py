from email.mime import base
import sys
import os
from pathlib import Path
from importlib import import_module
from importlib.util import spec_from_file_location, module_from_spec
import logging


from html2text import HTML2Text
import bs4

from .themes import generic as generic_theme
from html22text import html22text


class Renderer(object):
    def __init__(
        self,
        theme: str,
        theme_handler_path: str = None,
        markdown: bool = False,
        plain_tables: bool = False,
        open_quote: str = "“",
        close_quote: str = "”",
        default_image_alt: str = "",
        hide_strikethrough: bool = False,
        kill_tags: list = [],
        file_ext: str = "txt",
    ):
        self.page_order = []
        self.pages = []
        self.markdown = markdown
        self.plain_tables = plain_tables
        self.open_quote = open_quote
        self.close_quote = close_quote
        self.default_image_alt = default_image_alt
        self.hide_strikethrough = hide_strikethrough
        self.kill_tags = kill_tags
        self.theme = self._load_theme_handler(theme, theme_handler_path)
        self.file_ext = file_ext

    def write_txt(self, content: str, base_url: str, filename: str):
        Path(filename).write_text(self.render_doc(content, base_url))

    def render_doc(self, content: str, base_url: str = ""):
        return html22text(
            content=content,
            markdown=self.markdown,
            base_url=base_url,
            plain_tables=self.plain_tables,
            open_quote=self.open_quote,
            close_quote=self.close_quote,
            default_image_alt=self.default_image_alt,
            hide_strikethrough=self.hide_strikethrough,
            kill_tags=self.kill_tags,
            file_ext=self.file_ext,
        )

    def add_doc(self, content: str, base_url: str, rel_url: str):
        pos = self.page_order.index(rel_url)
        self.pages[pos] = (content, base_url, rel_url)

    def add_link(self, content: str, filename: str):
        return self.theme.modify_html(content, filename)

    @staticmethod
    def _load_theme_handler(theme: str, custom_handler_path: str = None):
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
                logging.warn(
                    f'Could not load theme handler {theme} from custom directory "{custom_handler_path}": {e}'
                )

        try:
            return import_module(module_name, "mkdocs_text_export_plugin.themes")
        except ImportError as e:
            logging.warn(f"Could not load theme handler {theme}: {e}")
            return generic_theme
