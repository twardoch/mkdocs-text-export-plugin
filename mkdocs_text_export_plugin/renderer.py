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
from .preprocessor import get_separate as prep_separate


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
        self.pgnum = 0
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

    def render_doc(self, content: str, base_url: str, rel_url: str = None):
        soup = bs4.BeautifulSoup(content, "html.parser")

        self.inject_pgnum(soup)

        if stylesheet := self.theme.get_stylesheet():
            style_tag = soup.new_tag("style")
            style_tag.string = stylesheet

            soup.head.append(style_tag)

        soup = prep_separate(soup, base_url, self.file_ext)

        for tag in soup.find_all(True):
            if tag.name in ("mark", "kbd"):
                tag.replace_with(tag.get_text(""))
            if self.plain_tables and tag.name == "table":
                rows = []
                for tr in tag.find_all("tr"):
                    cells = [td.get_text(" ") for td in tr.find_all(["th", "td"])]
                    rows.append(", ".join(cells))
                tag.replace_with(". ".join(rows))
            if not self.markdown:
                if tag.name in ("ul", "ol", "blockquote", "figure"):
                    tag.name = "div"
                elif tag.name in (
                    "label",
                    "h1",
                    "h2",
                    "h3",
                    "h4",
                    "h5",
                    "h6",
                    "figcaption",
                    "li",
                ):
                    tag.name = "p"
                elif tag.name in ("code"):
                    tag.name = "q"
        for kill_tag in self.kill_tags:
            for tag in soup.select(kill_tag):
                tag.replace_with("")

        # return str(soup)
        html = HTML2Text()
        html.body_width = 0
        html.bypass_tables = False
        html.close_quote = self.close_quote
        html.default_image_alt = self.default_image_alt
        html.emphasis_mark = "_" if self.markdown else ""
        html.escape_snob = False
        html.google_doc = False
        html.google_list_indent = 0
        # html.blockquote = 1 if self.markdown else 0
        html.hide_strikethrough = self.hide_strikethrough
        html.ignore_emphasis = not self.markdown
        html.ignore_images = not self.markdown
        html.ignore_links = not self.markdown
        html.ignore_mailto_links = not self.markdown
        html.ignore_tables = not self.markdown
        html.images_as_html = False
        html.images_to_alt = not self.markdown
        html.images_with_size = False
        html.inline_links = bool(self.markdown)
        html.links_each_paragraph = False
        html.mark_code = False
        html.open_quote = self.open_quote
        html.pad_tables = bool(self.markdown)
        html.protect_links = True
        html.single_line_break = False
        html.skip_internal_links = not self.markdown
        html.strong_mark = "**" if self.markdown else ""
        html.tag_callback = None
        html.ul_item_mark = "-" if self.markdown else ""
        html.unicode_snob = True
        html.use_automatic_links = bool(self.markdown)
        html.wrap_links = False
        html.wrap_list_items = False
        html.wrap_tables = False
        return html.handle(str(soup))

    def add_doc(self, content: str, base_url: str, rel_url: str):
        pos = self.page_order.index(rel_url)
        self.pages[pos] = (content, base_url, rel_url)

    def add_link(self, content: str, filename: str):
        return self.theme.modify_html(content, filename)

    def inject_pgnum(self, soup):
        pgnum_counter = soup.new_tag("style")
        pgnum_counter.string = """
        @page :first {{
            counter-reset: __pgnum__ {};
        }}
        @page {{
            counter-increment: __pgnum__;
        }}
        """.format(
            self.pgnum
        )

        soup.head.append(pgnum_counter)

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
