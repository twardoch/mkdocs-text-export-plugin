# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed (html22text from PyPI)
- `html22text` is now a regular dependency (`html22text>=1.0.1`), published on PyPI
  from https://github.com/twardoch/html22text. The bundled copy in
  `mkdocs_text_export_plugin/_vendor/` is removed. Version 1.0.2, which carried
  the bundled copy, was tagged but never uploaded to PyPI.

## [1.0.2] - 2026-10-13

### Changed (PyPI readiness and docs site)
- `html22text` 1.0.0 is now vendored in `mkdocs_text_export_plugin/_vendor/html22text/`
  (MIT, license included). The `git+https` dependency and `allow-direct-references`
  are gone, so the package can be uploaded to PyPI. Runtime dependencies are now
  `mkdocs`, `html2text` and `beautifulsoup4`.
- Documentation moved from the Jekyll site in `docs/` to ProperDocs + MaterialX:
  source in `src_docs/md/`, config in `src_docs/mkdocs.yml`, built into `docs/` by
  `src_docs/build.sh` and the new `Docs` workflow. Published at
  https://vexy.dev/vexy-mkdocs-text-export/.
- Docs now describe actual behaviour: text files are named after the source file
  (`setup.md` → `setup.txt`), the whole HTML page (including theme navigation) is
  converted unless `kill_tags` removes it, `plain_tables` is ignored, and
  `hide_strikethrough` has no effect on MkDocs output.
- `build.sh` builds docs and/or the package (`./build.sh [all|docs|package]`);
  `publish.sh` tags with `gitnextver`, builds and uploads with `uv publish`.

### Added
- GitHub Actions CI (`ci.yml`): tests on Python 3.12/3.13 across Linux and Windows,
  a MkDocs-version compatibility matrix (1.5.x and 1.6.x), plus ruff and mypy lint jobs.
- Release workflow (`release.yml`): builds the package and publishes a GitHub Release
  on `v*` tags. PyPI publishing is left disabled (commented) until `html22text` ships to PyPI.
- Integration test that runs a real `mkdocs build` and asserts the `.txt`/`.md` twin
  and the injected alternate link are produced.
- Unit tests for every built-in theme handler and the Renderer's handler resolution.
- Jekyll (Just the Docs) documentation site under `docs/` with home, options, and
  theme-handler pages.
- `CLAUDE.md` with per-file `this_file:` map and architecture notes.

### Changed
- Full type hints and docstrings across `plugin.py`, `renderer.py`, and all theme
  handlers; every source file now carries a `this_file:` header.
- `Renderer.kill_tags` no longer uses a mutable default argument.
- README rewritten and trimmed to a quick-start-first format with current package
  name and install instructions.
- mypy config added to `pyproject.toml`; `mypy` added to the `dev` extra.

### Removed
- Stale `tests/test_version.py`, which imported the already-removed `version.py`
  module and broke test collection.
- Legacy MkDocs-based docs scaffolding (`docs/mkdocs.yml`, `docs/docs/`,
  `docs/theme-handler/`), replaced by the Jekyll site.

### Changed (packaging, earlier this cycle)
- Renamed PyPI distribution to `vexy-mkdocs-text-export` (was `mkdocs-text-export-plugin`).
- Migrated build to `hatchling` + `hatch-vcs` with VCS-derived version (`mkdocs_text_export_plugin/__version__.py`, gitignored).
- `requires-python` bumped to `>=3.12`; repo URLs moved to `vexyart` org.
- `__init__.py` now imports `__version__` from the generated module instead of shelling out to `version.py`.

### Removed
- `setup.py` shim, `version.py`, `requirements.txt`, `requirements-dev.txt`.

### Added
- `build.sh` / `publish.sh` convention scripts.

> Note: PyPI publish is blocked until `html22text` (currently a `git+https` dependency) is itself published to PyPI.

### Changed (earlier)
- Cleaned up code structure and removed redundant imports
- Simplified theme handler implementations

## [1.0.0] - 2025-06-23

### Added
- Complete modernization of the codebase for MVP release
- Comprehensive test suite using pytest with 90%+ coverage
- GitHub Actions CI/CD pipeline for automated testing and linting
- Type hints throughout the codebase for better IDE support
- Development dependencies (pytest, flake8, black, mypy)
- Detailed documentation site with MkDocs
- Custom theme handler documentation and examples
- Support for environment variable-based plugin enabling/disabling

### Changed
- Updated project structure to follow Python best practices
- Improved code quality with black formatting and flake8 linting
- Enhanced README with better usage examples and configuration options
- Refactored plugin architecture for better maintainability
- Updated dependencies to use html22text from GitHub

### Fixed
- Various bug fixes and improvements in the rendering pipeline
- Theme handler loading mechanism improvements
- Better error handling and logging

## [0.1.0] - Initial Release

### Added
- Basic MkDocs text export functionality
- Support for plain text and Markdown output formats
- Theme-specific HTML preprocessing
- Configurable options for text conversion
- Support for Material, Cinder, and generic themes