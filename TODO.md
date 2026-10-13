<!-- this_file: TODO.md -->
# TODO

## Pending: PyPI release (2026-10-13)

- [ ] Release to PyPI with `./publish.sh` after `html22text` 1.0.1 is on PyPI. That upload
      is blocked by PyPI's `429 Too many new projects created` limit; see the html22text
      repository. Tag `v1.0.2` exists but was never uploaded; the next release (v1.0.3)
      is the first one that depends on `html22text` from PyPI.

## Done in the 2026 modernization pass
- [x] Add CI (`ci.yml`) and release (`release.yml`) workflows.
- [x] Full type hints + docstrings + `this_file:` headers across the package.
- [x] Delete stale `test_version.py`; add theme-handler and `mkdocs build` integration tests (88% coverage).
- [x] ruff + mypy clean.
- [x] Convert docs to Jekyll (Just the Docs).
- [x] Rewrite README (quick-start first, ≤200 lines); add `CLAUDE.md`.

## Ready
- [ ] Decide whether `plain_tables` should be wired through or removed (it is accepted
      but never passed to the converter).

## Bigger ideas (not yet scheduled)
- [ ] Migrate the flat `mkdocs_text_export_plugin/` package to a `src/` layout
      (update `hatch` targets and the `version-file` path).
- [ ] Add `exclude_pages` / glob-based page filtering.
- [ ] Untrack the generated `llms.txt` snapshot (now gitignored) in a follow-up commit.
