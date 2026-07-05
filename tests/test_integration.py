# this_file: tests/test_integration.py
"""End-to-end test: build a tiny MkDocs site with the plugin and check output."""

import subprocess
import sys
from pathlib import Path

import pytest

MKDOCS_YML = """\
site_name: Integration Test Site
theme:
  name: mkdocs
plugins:
  - text-export:
      markdown: {markdown}
"""

INDEX_MD = """\
# Hello

A paragraph with a [link](https://example.com) and some **bold** text.
"""


def _build_site(tmp_path: Path, markdown: bool) -> Path:
    """Write a minimal MkDocs project under ``tmp_path`` and build it."""
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "index.md").write_text(INDEX_MD)
    (tmp_path / "mkdocs.yml").write_text(
        MKDOCS_YML.format(markdown="true" if markdown else "false")
    )

    site = tmp_path / "site"
    result = subprocess.run(
        [sys.executable, "-m", "mkdocs", "build", "--site-dir", str(site)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"mkdocs build failed:\n{result.stderr}"
    return site


@pytest.mark.parametrize(
    ("markdown", "ext"),
    [(False, "txt"), (True, "md")],
)
def test_mkdocs_build_emits_text_twin(tmp_path: Path, markdown: bool, ext: str) -> None:
    """A full build produces a .txt/.md twin next to the page's index.html."""
    site = _build_site(tmp_path, markdown=markdown)

    exported = site / f"index.{ext}"
    assert exported.exists(), f"expected {exported} to be generated"

    text = exported.read_text()
    assert "Hello" in text
    assert "bold" in text
    # The HTML markup itself must be gone from the exported text.
    assert "<strong>" not in text

    # The plugin also injects an alternate-link into the built HTML page.
    html = (site / "index.html").read_text()
    assert f"index.{ext}" in html
