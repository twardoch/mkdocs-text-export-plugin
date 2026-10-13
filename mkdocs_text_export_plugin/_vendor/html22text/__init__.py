# this_file: mkdocs_text_export_plugin/_vendor/html22text/__init__.py
"""Vendored copy of html22text (MIT, (c) 2022 Adam Twardoch).

Source: https://github.com/twardoch/html22text, tag v1.0.0 (commit d365054),
files ``src/html22text/html22text.py`` and ``src/html22text/url_utils.py``.
Bundled because html22text is not published on PyPI, and PyPI rejects packages
that depend on a ``git+https`` URL. The command-line entry point (which needs
``fire``) is not included. See ``LICENSE`` in this directory.
"""

from .html22text import html22text

__all__ = ["html22text"]
