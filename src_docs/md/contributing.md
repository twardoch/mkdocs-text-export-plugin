# Contributing

## Set up a development environment

1. Clone the repository and enter it:

    ```bash
    git clone https://github.com/vexyart/vexy-mkdocs-text-export.git
    cd vexy-mkdocs-text-export
    ```

2. Create a virtual environment and install the package with its development
   tools (`pytest`, `pytest-cov`, `ruff`, `mypy`, `mkdocs-material`):

    ```bash
    uv venv --python 3.12
    source .venv/bin/activate
    uv pip install -e ".[dev]"
    ```

## Run the checks

```bash
pytest -q
ruff check .
mypy mkdocs_text_export_plugin
```

The tests live in `tests/`:

| File | What it covers |
|---|---|
| `tests/test_plugin.py` | The plugin's build events and options |
| `tests/test_themes.py` | Every built-in theme handler and handler selection |
| `tests/test_integration.py` | A real `mkdocs build` that checks the text file and the injected link |

CI (`.github/workflows/ci.yml`) runs the tests on Python 3.12 and 3.13 on Linux
and Windows, runs them again against MkDocs 1.5.x and 1.6.x, and runs `ruff` and
`mypy`.

## Conventions

- Every source file starts with a `this_file:` comment that gives its path.
- The version comes from git tags through `hatch-vcs`. Do not add a version
  string to the code. `mkdocs_text_export_plugin/__version__.py` is generated
  and ignored by git.
- Do not edit files in `mkdocs_text_export_plugin/_vendor/`. Copy a new
  `html22text` release over them instead (see [Architecture](architecture.md)).

## Build the package and the documentation

The root `build.sh` builds either part or both:

```bash
./build.sh            # documentation and package
./build.sh docs       # documentation only, into docs/
./build.sh package    # dist/*.whl and dist/*.tar.gz, then twine check
```

The documentation source is in `src_docs/md/`, and its configuration is
`src_docs/mkdocs.yml`. `src_docs/build.sh` builds it with ProperDocs and the
MaterialX theme in strict mode, so any warning fails the build. For a live
preview on `http://127.0.0.1:8000`:

```bash
src_docs/build.sh serve
```

Do not edit `docs/` by hand. It is generated, and the `Docs` workflow rebuilds
and commits it on every push to `main` that changes `src_docs/`.

## Release

`publish.sh` makes a release:

1. `uvx gitnextver` commits pending changes, creates the next `vX.Y.Z` tag and
   pushes both.
2. `./build.sh package` builds the wheel and the source distribution from that
   tag.
3. `uv publish dist/*` uploads them to PyPI. It needs `UV_PUBLISH_TOKEN` or
   another `uv publish` credential.

Pushing the tag also starts `.github/workflows/release.yml`, which builds the
package and creates a GitHub release with the matching `CHANGELOG.md` section.
That workflow does not upload to PyPI.
