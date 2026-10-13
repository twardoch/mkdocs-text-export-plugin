<!-- this_file: TODO.md -->
# TODO

## Done in the 2026 modernization pass
- [x] Add CI (`ci.yml`) and release (`release.yml`) workflows.
- [x] Full type hints + docstrings + `this_file:` headers across the package.
- [x] Delete stale `test_version.py`; add theme-handler and `mkdocs build` integration tests (88% coverage).
- [x] ruff + mypy clean.
- [x] Convert docs to Jekyll (Just the Docs).
- [x] Rewrite README (quick-start first, ≤200 lines); add `CLAUDE.md`.

## Ready
- [ ] Publish to PyPI with `./publish.sh`. Unblocked: `html22text` is now vendored in
      `mkdocs_text_export_plugin/_vendor/html22text/`, so there is no `git+https` dependency.
- [ ] Decide whether `plain_tables` should be wired through or removed (it is accepted
      but never passed to the converter).

## Bigger ideas (not yet scheduled)
- [ ] Migrate the flat `mkdocs_text_export_plugin/` package to a `src/` layout
      (update `hatch` targets and the `version-file` path).
- [ ] Add `exclude_pages` / glob-based page filtering.
- [ ] Untrack the generated `llms.txt` snapshot (now gitignored) in a follow-up commit.
