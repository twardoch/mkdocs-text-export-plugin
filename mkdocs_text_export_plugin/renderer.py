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
from .preprocessor import get_separate as prep_separate, get_combined as prep_combined


class Renderer(object):
    def __init__(self,
        combined: bool,
        markdown: bool = False,
        plain_tables: bool = False,
        open_quote: str = "“",
        close_quote: str = "”",
        default_image_alt: str = "",
        hide_strikethrough: bool = False,
        kill_tags: list = [],
        theme: str,
        theme_handler_path: str = None,
        ):
        self.combined = combined
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

    def write_txt(self, content: str, base_url: str, filename: str):
        Path(filename).write_text(self.render_doc(content, base_url))

    def render_doc(self, content: str, base_url: str, rel_url: str = None):
        soup = bs4.BeautifulSoup(content, "html.parser")

        self.inject_pgnum(soup)

        if stylesheet := self.theme.get_stylesheet():
            style_tag = soup.new_tag("style")
            style_tag.string = stylesheet

            soup.head.append(style_tag)

        if self.combined:
            soup = prep_combined(soup, base_url, rel_url)
        else:
            soup = prep_separate(soup, base_url)

        for tag in soup.find_all(True):
            if self.markdown and tag.name in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
                tag.replace_with(soup.new_tag("p"))
            if tag.name in ('mark', 'kbd'):
                tag.replace_with(tag.get_text(''))
            if self.plain_tables and tag.name in ('table'):
                tag.replace_with(tag.get_text(' '))
            if self.markdown:
                if tag.name in ('ul', 'ol'):
                    tag.replace_with(soup.new_tag("div"))
                if tag.name in ('li'):
                    tag.replace_with(soup.new_tag("p"))
            if tag.name in (self.kill_tags):
                tag.replace_with('')

        html = HTML2Text()
        html.body_width = 0
        html.bypass_tables = False
        html.close_quote = self.close_quote
        html.default_image_alt = self.default_image_alt
        html.emphasis_mark = "_" if self.markdown else ""
        html.escape_snob = False
        html.google_doc = False
        html.google_list_indent = 0
        html.blockquote = 1 if self.markdown else 0
        html.hide_strikethrough = self.hide_strikethrough
        html.ignore_emphasis = True if self.markdown else False
        html.ignore_images = True if self.markdown else False
        html.ignore_links = True if self.markdown else False
        html.ignore_mailto_links = True if self.markdown else False
        html.ignore_tables = True if self.markdown else False
        html.images_as_html = False
        html.images_to_alt = True
        html.images_with_size = False
        html.inline_links = True if self.markdown else False
        html.links_each_paragraph = False
        html.mark_code = False
        html.open_quote = self.open_quote
        html.pad_tables = True if self.markdown else False
        html.protect_links = True
        html.single_line_break = False
        html.skip_internal_links = False if self.markdown else True
        html.strong_mark = "**" if self.markdown else ""
        html.tag_callback = None
        html.ul_item_mark = "-" if self.markdown else ""
        html.unicode_snob = True
        html.use_automatic_links = True if self.markdown else False
        html.wrap_links = False
        html.wrap_list_items = False
        html.wrap_tables = False
        return html.handle(str(soup))

    def add_doc(self, content: str, base_url: str, rel_url: str):
        pos = self.page_order.index(rel_url)
        self.pages[pos] = (content, base_url, rel_url)

    def write_combined_pdf(self, output_path: str):
        rendered_pages = []
        for p in self.pages:
            if p is None:
                print("Unexpected error - not all pages were rendered properly")
                continue

            render = self.render_doc(p[0], p[1], p[2])
            self.pgnum += len(render.pages)
            rendered_pages.append(render)

        flatten = lambda l: [item for sublist in l for item in sublist]
        all_pages = flatten([p.pages for p in rendered_pages if p != None])

        rendered_pages[0].copy(all_pages).write_txt(output_path)

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
                print(
                    f'Could not load theme handler {theme} from custom directory "{custom_handler_path}": {e}',
                    file=sys.stderr,
                )

        try:
            return import_module(module_name, "mkdocs_pdf_export_plugin.themes")
        except ImportError as e:
            print(f"Could not load theme handler {theme}: {e}", file=sys.stderr)
            return generic_theme
