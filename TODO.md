# TODO List for mkdocs-text-export-plugin

## 🚨 Critical Fixes (Immediate)

- [ ] Fix syntax errors in `docs/theme-handler/cinder.py` (duplicate functions, malformed code)
- [ ] Remove unused `weasyprint` import from `mkdocs_text_export_plugin/plugin.py`
- [ ] Fix `weasyprint.urls` import error (should use `urllib.parse`)
- [ ] Resolve html22text GitHub dependency issue (vendor it or publish to PyPI)

## 📦 Packaging & Distribution

- [ ] Create `pyproject.toml` for modern Python packaging
- [ ] Create `MANIFEST.in` for proper package distribution
- [ ] Add `mkdocs_text_export_plugin/__init__.py` with version info
- [ ] Set up setuptools_scm for automatic versioning
- [ ] Create `.pre-commit-config.yaml` for code quality checks
- [ ] Add `py.typed` marker for type checking support

## 🧪 Testing Improvements

- [ ] Add tests for all theme handlers (material, cinder, generic, basictheme)
- [ ] Create integration tests with real MkDocs builds
- [ ] Add tests for custom theme handler loading
- [ ] Test error conditions and edge cases
- [ ] Add performance benchmarks
- [ ] Increase test coverage to >95%

## 📚 Documentation

- [ ] Create `docs/docs/quickstart.md` guide
- [ ] Create `docs/docs/troubleshooting.md` with common issues
- [ ] Create `docs/docs/examples.md` with practical examples  
- [ ] Create `docs/docs/api.md` with full API reference
- [ ] Create `docs/docs/contributing.md` with contribution guidelines
- [ ] Fix broken example in `docs/theme-handler/cinder.py`
- [ ] Add docstrings to all public methods
- [ ] Generate API docs with mkdocstrings

## ✨ Feature Enhancements

- [ ] Add `exclude_pages` configuration option
- [ ] Add `output_dir` configuration option
- [ ] Add configuration validation
- [ ] Create CLI tool for standalone HTML conversion
- [ ] Add parallel processing for large sites
- [ ] Add progress indicator for long builds
- [ ] Support custom CSS removal rules
- [ ] Add option to preserve HTML structure in markdown

## 🏗️ Code Quality

- [ ] Complete type hints for all functions
- [ ] Standardize error handling across modules
- [ ] Improve logging consistency
- [ ] Refactor plugin/renderer coupling
- [ ] Add proper error messages for common issues
- [ ] Remove code duplication

## 🐳 DevOps & CI/CD

- [ ] Create Dockerfile for containerized usage
- [ ] Create docker-compose.yml example
- [ ] Enhance GitHub Actions workflow
- [ ] Add automated PyPI publishing
- [ ] Add security scanning (Snyk/Dependabot)
- [ ] Set up code coverage reporting

## 🚀 Advanced Features (Future)

- [ ] Add JSON output format
- [ ] Add YAML output format  
- [ ] Support for extracting structured data
- [ ] Automatic table of contents generation
- [ ] Code block extraction with syntax highlighting
- [ ] Plugin hooks for extensibility
- [ ] Batch processing mode
- [ ] Watch mode for development

## 🐛 Known Issues to Fix

- [ ] Theme handler loading fails silently in some cases
- [ ] No proper cleanup if conversion fails mid-process
- [ ] Memory usage high for large documentation sites
- [ ] Unicode handling issues with certain characters
- [ ] Relative URLs not properly resolved in some themes

## 📈 Performance Optimizations

- [ ] Cache theme handler instances
- [ ] Optimize BeautifulSoup parsing
- [ ] Reduce memory footprint for large files
- [ ] Add streaming support for huge pages
- [ ] Profile and optimize hot paths

## 🔒 Security Improvements

- [ ] Sanitize file paths to prevent directory traversal
- [ ] Add input validation for all config options
- [ ] Secure handling of custom theme handler imports
- [ ] Add security policy (SECURITY.md)

## 📋 Project Management

- [ ] Create issue templates on GitHub
- [ ] Set up project board for tracking progress
- [ ] Define release schedule and versioning policy
- [ ] Create automated changelog generation
- [ ] Set up community guidelines

---

**Priority Legend:**
- 🚨 Critical - Must fix before next release
- 📦 High - Important for usability  
- 🧪 Medium - Quality improvements
- ✨ Low - Nice to have features

**Note**: Check off items as completed. Review and update this list regularly.