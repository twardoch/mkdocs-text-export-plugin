# this_file: tests/test_themes.py
"""Unit tests for the built-in theme handlers and the Renderer's theme loading."""

import pytest

from mkdocs_text_export_plugin.renderer import Renderer
from mkdocs_text_export_plugin.themes import (
    basictheme,
    cinder,
    generic,
    material,
    mkdocs,
)

HEAD_LINK_HANDLERS = [generic, mkdocs, basictheme]


@pytest.mark.parametrize("handler", HEAD_LINK_HANDLERS)
def test_head_link_handlers_add_alternate_link(handler):
    """generic/mkdocs/basic handlers inject a <head> alternate link."""
    html = "<html><head></head><body><p>Hi</p></body></html>"
    out = handler.modify_html(html, "page.txt")
    assert 'rel="alternate"' in out
    assert 'href="page.txt"' in out
    assert handler.get_stylesheet() == ""


def test_material_handler_inserts_download_button():
    """The material handler injects a visible button into the article header."""
    html = '<article class="md-content__inner md-typeset"><h1>Doc</h1></article>'
    out = material.modify_html(html, "doc.txt")
    assert 'href="doc.txt"' in out
    assert "md-content__button" in out
    assert "<svg" in out
    # Original insert point is preserved (button is appended after it).
    assert '<article class="md-content__inner md-typeset">' in out
    assert material.get_stylesheet() != ""


def test_cinder_handler_adds_footer_link():
    """The cinder handler prepends a visible link into the page footer."""
    html = "<html><body><footer><span>foot</span></footer></body></html>"
    out = cinder.modify_html(html, "page.txt")
    assert 'href="page.txt"' in out
    assert "Open text" in out


def test_renderer_falls_back_to_generic_for_unknown_theme():
    """An unknown theme name resolves to the generic handler."""
    renderer = Renderer(theme="no-such-theme")
    assert renderer.theme is generic


def test_renderer_loads_named_theme_handler():
    """A known theme name resolves to its dedicated handler module."""
    renderer = Renderer(theme="material")
    assert renderer.theme is material
