# this_file: mkdocs_text_export_plugin/__init__.py
"""MkDocs Text Export Plugin — export content pages as plain-text or Markdown files."""

try:
    from mkdocs_text_export_plugin.__version__ import __version__
except ImportError:  # editable install before hatch-vcs has run
    __version__ = "0.0.0+local"

__all__ = ["__version__"]
