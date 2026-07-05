<!-- this_file: TODO.md -->
# TODO

## Done in the 2026 modernization pass
- [x] Add CI (`ci.yml`) and release (`release.yml`) workflows.
- [x] Full type hints + docstrings + `this_file:` headers across the package.
- [x] Delete stale `test_version.py`; add theme-handler and `mkdocs build` integration tests (88% coverage).
- [x] ruff + mypy clean.
- [x] Convert docs to Jekyll (Just the Docs).
- [x] Rewrite README (quick-start first, ≤200 lines); add `CLAUDE.md`.

## Blocked
- [ ] Publish to PyPI. Blocked: `html22text` is a `git+https` dependency and not on
      PyPI, so PyPI rejects the upload. Publish `html22text` first, then drop the git
      reference in `pyproject.toml` and re-enable the `publish-pypi` job in `release.yml`.

## Bigger ideas (not yet scheduled)
- [ ] Migrate the flat `mkdocs_text_export_plugin/` package to a `src/` layout
      (update `hatch` targets and the `version-file` path).
- [ ] Add `exclude_pages` / glob-based page filtering.
- [ ] Untrack the generated `llms.txt` snapshot (now gitignored) in a follow-up commit.
