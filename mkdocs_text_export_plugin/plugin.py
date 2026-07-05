# this_file: mkdocs_text_export_plugin/plugin.py
"""MkDocs plugin that writes a plain-text or Markdown twin of every built page.

The plugin hooks the tail end of the MkDocs build: once a page has been rendered
to its final HTML (after every other plugin has run), :meth:`on_post_page` hands
that HTML to :class:`~mkdocs_text_export_plugin.renderer.Renderer`, which strips
it down to ``.txt`` or ``.md`` and drops the result next to the ``.html`` file.
"""

import logging
import os
from timeit import default_timer as timer
from typing import Any
from urllib.request import pathname2url

from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin

log = logging.getLogger(__name__)


class MdTxtExportPlugin(BasePlugin):
    """Export each built page as a sibling plain-text or Markdown file."""

    config_scheme = (
        ("verbose", config_options.Type(bool, default=False)),
        # None means "always enabled"; a string names an env var that must equal "1".
        ("enabled_if_env", config_options.Type(str, default=None)),
        ("markdown", config_options.Type(bool, default=False)),
        ("plain_tables", config_options.Type(bool, default=False)),
        ("open_quote", config_options.Type(str, default="“")),
        ("close_quote", config_options.Type(str, default="”")),
        ("default_image_alt", config_options.Type(str, default="")),
        ("hide_strikethrough", config_options.Type(bool, default=False)),
        ("kill_tags", config_options.Type(list, default=[])),
        ("theme_handler_path", config_options.Type(str, default="")),
    )

    def __init__(self) -> None:
        self.renderer: Any = None
        self.enabled: bool = True
        self.markdown: bool = False
        self.file_ext: str = "txt"
        self.num_files: int = 0
        self.num_errors: int = 0
        self.total_time: float = 0.0

    def on_config(self, config: Any) -> Any:
        """Resolve the enabled state and output extension from plugin options.

        Returns ``None`` when ``enabled_if_env`` names an env var that is not set
        to ``"1"``, which is MkDocs' signal to skip the rest of this plugin.
        """
        # Access plugin config via self.config, not the passed-in site config.
        if self.config["enabled_if_env"]:
            env_name = self.config["enabled_if_env"]
            self.enabled = os.environ.get(env_name) == "1"
            if not self.enabled:
                log.warning(
                    f"Text export is disabled (set environment variable {env_name} to 1 to enable)"
                )
                return None

        self.markdown = self.config["markdown"]
        if self.markdown:
            self.file_ext = "md"

        log.setLevel(logging.DEBUG if self.config["verbose"] else logging.ERROR)
        return config

    def on_nav(self, nav: Any, config: Any, files: Any) -> Any:
        """Build the :class:`Renderer` once the theme and navigation are known."""
        if not self.enabled:
            return nav

        # Imported lazily so a disabled plugin never pays for html22text/bs4.
        from .renderer import Renderer

        self.renderer = Renderer(
            theme=config["theme"].name,
            theme_handler_path=self.config["theme_handler_path"],
            markdown=self.markdown,
            plain_tables=self.config["plain_tables"],
            open_quote=self.config["open_quote"],
            close_quote=self.config["close_quote"],
            default_image_alt=self.config["default_image_alt"],
            hide_strikethrough=self.config["hide_strikethrough"],
            kill_tags=self.config["kill_tags"],
            file_ext=self.file_ext,
        )

        self.renderer.pages = [None] * len(nav.pages)
        for page in nav.pages:
            self.renderer.page_order.append(page.file.url)

        return nav

    def on_post_page(self, output_content: str, page: Any, config: Any) -> str:
        """Write the text twin of ``page`` and return the (link-augmented) HTML."""
        if not self.enabled:
            return output_content

        start = timer()
        self.num_files += 1

        try:
            abs_dest_path = page.file.abs_dest_path
            src_path = page.file.src_path
        except AttributeError:
            # Fallback for the pre-1.0 MkDocs page API.
            abs_dest_path = page.abs_output_path
            src_path = page.input_path

        path = os.path.dirname(abs_dest_path)
        os.makedirs(path, exist_ok=True)

        filename = os.path.splitext(os.path.basename(src_path))[0]
        # base_url lets html22text resolve page-relative links against this file.
        base_url = pathname2url(os.path.join(path, filename))
        txt_file = f"{filename}.{self.file_ext}"

        try:
            self.renderer.write_txt(output_content, base_url, os.path.join(path, txt_file))
            output_content = self.renderer.add_link(output_content, txt_file)
        except Exception as e:
            log.error(f"Error converting {src_path} to text: {e}")
            self.num_errors += 1

        self.total_time += timer() - start
        return output_content

    def on_post_build(self, config: Any) -> None:
        """Log a one-line summary of how many files were converted."""
        if not self.enabled:
            return

        log.info(f"Converting {self.num_files} files to text took {self.total_time:.1f}s")
        if self.num_errors > 0:
            log.error(f"{self.num_errors} conversion errors occurred (see above)")
