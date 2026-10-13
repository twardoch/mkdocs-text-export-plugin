# Installation

## Requirements

- Python 3.12 or later (`requires-python = ">=3.12"`).
- MkDocs 1.5.0 or later.

The plugin also installs [`html22text`](https://pypi.org/project/html22text/)
1.0.1 or later, which brings in `html2text`, `beautifulsoup4` and `fire`.

## Install from PyPI

```bash
pip install vexy-mkdocs-text-export
```

With `uv`:

```bash
uv pip install vexy-mkdocs-text-export
```

!!! note
    If PyPI does not list the package yet, install it from GitHub instead:
    `pip install "git+https://github.com/vexyart/vexy-mkdocs-text-export"`.

To run a one-off build without installing anything into your environment:

```bash
uvx --with vexy-mkdocs-text-export mkdocs build
```

## Install from source

1. Clone the repository:

    ```bash
    git clone https://github.com/vexyart/vexy-mkdocs-text-export.git
    cd vexy-mkdocs-text-export
    ```

2. Install the package in editable mode, with the development tools:

    ```bash
    uv venv --python 3.12
    source .venv/bin/activate
    uv pip install -e ".[dev]"
    ```

The package version comes from the latest `vX.Y.Z` git tag (through
`hatch-vcs`). A clone without tags gets a development version string.

## Check the installation

MkDocs finds the plugin through the `mkdocs.plugins` entry point named
`text-export`. To confirm that the entry point is registered:

```bash
python -c "from importlib.metadata import entry_points; print(entry_points(group='mkdocs.plugins')['text-export'])"
```

The command prints:

```text
EntryPoint(name='text-export', value='mkdocs_text_export_plugin.plugin:MdTxtExportPlugin', group='mkdocs.plugins')
```

To print the installed version:

```bash
python -c "import mkdocs_text_export_plugin as m; print(m.__version__)"
```

Next: [Quick start](quickstart.md).
