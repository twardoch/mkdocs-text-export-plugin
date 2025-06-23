import os
from timeit import default_timer as timer

from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
import logging


class MdTxtExportPlugin(BasePlugin):

    config_scheme = (
        ("verbose", config_options.Type(bool, default=False)),
        ("enabled_if_env", config_options.Type(str, default=None)), # Allow None
        ("markdown", config_options.Type(bool, default=False)),
        ("plain_tables", config_options.Type(bool, default=False)),
        ("open_quote", config_options.Type(str, default="“")),
        ("close_quote", config_options.Type(str, default="”")),
        ("default_image_alt", config_options.Type(str, default="")),
        ("hide_strikethrough", config_options.Type(bool, default=False)),
        ("kill_tags", config_options.Type(list, default=[])),
        ("theme_handler_path", config_options.Type(str, default="")),
    )

    def __init__(self):
        self.renderer = None
        self.enabled = True
        self.markdown = False
        self.file_ext = "txt"
        self.num_files = 0
        self.num_errors = 0
        self.total_time = 0

    def on_config(self, config):
        # Access plugin config via self.config, not config argument
        if self.config["enabled_if_env"]:
            env_name = self.config["enabled_if_env"]
            self.enabled = os.environ.get(env_name) == "1"
            if not self.enabled:
                # Ensure logging is available here
                log = logging.getLogger(__name__)
                log.warning(
                    f"Text export is disabled (set environment variable {env_name} to 1 to enable)"
                )
                return # Return None to disable plugin

        self.markdown = self.config["markdown"]
        if self.markdown:
            self.file_ext = "md"

        # Configure logging after checking enabled status
        log = logging.getLogger(__name__)
        if self.config["verbose"]:
            log.setLevel(logging.DEBUG)
        else:
            log.setLevel(logging.ERROR)

        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        return config

    def on_nav(self, nav, config, files):
        if not self.enabled:
            return nav

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

    def on_post_page(self, output_content, page, config):
        if not self.enabled:
            return output_content

        start = timer()

        self.num_files += 1

        try:
            abs_dest_path = page.file.abs_dest_path
            src_path = page.file.src_path
        except AttributeError:
            # Support for mkdocs <1.0
            abs_dest_path = page.abs_output_path
            src_path = page.input_path

        path = os.path.dirname(abs_dest_path)
        os.makedirs(path, exist_ok=True)

        filename = os.path.splitext(os.path.basename(src_path))[0]

        from weasyprint import urls  # type: ignore

        base_url = urls.path2url(os.path.join(path, filename))
        txt_file = f"{filename}.{self.file_ext}"

        try:
            self.renderer.write_txt(
                output_content, base_url, os.path.join(path, txt_file)
            )
            output_content = self.renderer.add_link(output_content, txt_file)
        except Exception as e:
            logging.error(f"Error converting {src_path} to text: {e}")
            self.num_errors += 1

        end = timer()
        self.total_time += end - start

        return output_content

    def on_post_build(self, config):
        if not self.enabled:
            return

        logging.info(
            f"Converting {self.num_files} files to text took {self.total_time:.1f}s"
        )
        if self.num_errors > 0:
            logging.error(f"{self.num_errors} conversion errors occurred (see above)")
