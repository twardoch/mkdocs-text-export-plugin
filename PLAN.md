# MkDocs Text Export Plugin - Improvement Plan

## Executive Summary

This document outlines a comprehensive plan to improve the mkdocs-text-export-plugin, making it more stable, elegant, and easily deployable. The improvements are organized into phases, with immediate fixes taking priority, followed by enhancements and new features.

## Current State Analysis

### Strengths
- Core functionality works well for basic text/markdown export
- Good test coverage for the main plugin
- Clean plugin architecture following MkDocs conventions
- Support for multiple themes with extensible handlers
- Well-documented configuration options

### Weaknesses
1. **Code Quality Issues**
   - Syntax errors in docs/theme-handler/cinder.py (duplicate code, malformed functions)
   - Incomplete type hints in some modules
   - Inconsistent error handling and logging patterns
   - Import of weasyprint in plugin.py that's not used

2. **Deployment Challenges**
   - Dependency on GitHub-hosted html22text makes pip installation fragile
   - No pyproject.toml for modern Python packaging
   - Missing MANIFEST.in for proper package distribution
   - No Docker support for isolated environments

3. **Testing Gaps**
   - No tests for theme handlers
   - Missing integration tests with real MkDocs builds
   - No performance benchmarks
   - Limited error condition testing

4. **Documentation Limitations**
   - No API reference documentation
   - Missing practical examples for custom theme handlers
   - No troubleshooting guide
   - No contribution guidelines

## Phase 1: Immediate Fixes (1-2 days)

### 1.1 Fix Critical Code Issues

**Problem**: The docs/theme-handler/cinder.py file has syntax errors and duplicate code that could confuse users trying to create custom handlers.

**Solution**:
```python
# Fix the cinder.py example by:
1. Removing duplicate function definitions
2. Fixing the malformed fix_html function
3. Adding proper docstrings and comments
4. Making it a working example that users can copy
```

**Implementation**:
- Review and fix the example theme handler
- Ensure it follows the same pattern as built-in handlers
- Add inline comments explaining each section

### 1.2 Remove Unused Dependencies

**Problem**: The plugin imports weasyprint but never uses it, creating unnecessary dependencies.

**Solution**:
- Remove the weasyprint import from plugin.py
- Audit all imports across the codebase
- Update requirements.txt accordingly

### 1.3 Fix Installation Issues

**Problem**: The GitHub dependency for html22text makes installation unreliable.

**Solution**:
1. **Option A (Preferred)**: Vendor html22text into the project
   - Copy the html22text code into mkdocs_text_export_plugin/vendor/
   - Update imports to use the vendored version
   - Remove GitHub dependency from requirements.txt

2. **Option B**: Create a proper release of html22text on PyPI
   - Work with the html22text maintainer
   - Or fork and maintain our own PyPI package

## Phase 2: Packaging and Distribution (2-3 days)

### 2.1 Modernize Python Packaging

**Create pyproject.toml**:
```toml
[build-system]
requires = ["setuptools>=45", "wheel", "setuptools_scm[toml]>=6.2"]
build-backend = "setuptools.build_meta"

[project]
name = "mkdocs-text-export-plugin"
authors = [{name = "Adam Twardoch", email = "adam+github@twardoch.com"}]
description = "MkDocs plugin to export pages as text or markdown"
readme = "README.md"
requires-python = ">=3.10"
keywords = ["mkdocs", "plugin", "export", "text", "markdown"]
license = {text = "MIT"}
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]
dependencies = [
    "mkdocs>=1.3.0",
    "beautifulsoup4>=4.0.0",
    "html2text",
]
dynamic = ["version"]

[project.entry-points."mkdocs.plugins"]
text-export = "mkdocs_text_export_plugin.plugin:MdTxtExportPlugin"

[project.urls]
Homepage = "https://github.com/twardoch/mkdocs-text-export-plugin"
Documentation = "https://github.com/twardoch/mkdocs-text-export-plugin#readme"
Repository = "https://github.com/twardoch/mkdocs-text-export-plugin"
Issues = "https://github.com/twardoch/mkdocs-text-export-plugin/issues"

[tool.setuptools_scm]
write_to = "mkdocs_text_export_plugin/_version.py"
```

**Create MANIFEST.in**:
```
include README.md
include LICENSE
include CHANGELOG.md
include requirements*.txt
recursive-include mkdocs_text_export_plugin *.py
recursive-include docs *.md *.yml
recursive-include tests *.py
global-exclude __pycache__
global-exclude *.py[co]
global-exclude .DS_Store
```

### 2.2 Add Pre-commit Hooks

**Create .pre-commit-config.yaml**:
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict

  - repo: https://github.com/psf/black
    rev: 24.1.0
    hooks:
      - id: black
        language_version: python3.10

  - repo: https://github.com/PyCQA/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        args: ['--max-line-length=127', '--extend-ignore=E203']

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-setuptools, types-beautifulsoup4]
```

## Phase 3: Testing Improvements (3-4 days)

### 3.1 Add Theme Handler Tests

Create `tests/test_theme_handlers.py`:
```python
import pytest
from mkdocs_text_export_plugin.themes import material, cinder, generic

def test_material_theme_handler():
    """Test Material theme specific modifications"""
    # Test stylesheet generation
    # Test HTML modifications
    # Test with real Material theme HTML samples

def test_custom_theme_handler_loading():
    """Test loading custom theme handlers from file"""
    # Create temporary handler file
    # Test loading mechanism
    # Verify fallback to generic handler
```

### 3.2 Add Integration Tests

Create `tests/test_integration.py`:
```python
def test_full_mkdocs_build():
    """Test plugin with a real MkDocs build"""
    # Create temporary MkDocs project
    # Run mkdocs build with plugin
    # Verify output files are created
    # Check content conversion quality

def test_multiple_themes():
    """Test plugin with different MkDocs themes"""
    # Test with material, readthedocs, mkdocs themes
    # Verify appropriate handlers are loaded
```

### 3.3 Add Performance Benchmarks

Create `tests/test_performance.py`:
```python
def test_conversion_speed():
    """Benchmark conversion performance"""
    # Test with various file sizes
    # Measure memory usage
    # Compare markdown vs text output performance
```

## Phase 4: Feature Enhancements (1 week)

### 4.1 Improved Configuration System

**Add configuration validation**:
```python
class MdTxtExportPlugin(BasePlugin):
    config_scheme = (
        # ... existing config ...
        ("exclude_pages", config_options.Type(list, default=[])),
        ("output_dir", config_options.Type(str, default="")),
        ("custom_css_rules", config_options.Type(list, default=[])),
    )
    
    def validate_config(self):
        """Validate configuration options"""
        # Check theme_handler_path exists
        # Validate kill_tags format
        # Ensure output_dir is writable
```

### 4.2 CLI Tool for Standalone Usage

Create `mkdocs_text_export_plugin/cli.py`:
```python
import click

@click.command()
@click.option('--input', '-i', help='HTML file to convert')
@click.option('--output', '-o', help='Output file path')
@click.option('--format', type=click.Choice(['txt', 'md']), default='txt')
def convert(input, output, format):
    """Convert HTML to text/markdown without MkDocs"""
    # Standalone conversion functionality
    # Useful for testing and one-off conversions
```

### 4.3 Plugin Hooks for Extensibility

**Add extension points**:
```python
class MdTxtExportPlugin(BasePlugin):
    def on_pre_convert(self, html, page, config):
        """Hook called before conversion"""
        # Allow other plugins to modify HTML
        return html
    
    def on_post_convert(self, text, page, config):
        """Hook called after conversion"""
        # Allow post-processing of converted text
        return text
```

## Phase 5: Documentation Overhaul (3-4 days)

### 5.1 API Reference Documentation

Generate API docs using:
- mkdocstrings for automatic API documentation
- Proper docstrings for all public methods
- Type hints for better documentation

### 5.2 User Guide Improvements

Create new documentation pages:
- `docs/docs/quickstart.md` - Getting started quickly
- `docs/docs/troubleshooting.md` - Common issues and solutions
- `docs/docs/examples.md` - Real-world usage examples
- `docs/docs/api.md` - Complete API reference
- `docs/docs/contributing.md` - How to contribute

### 5.3 Example Projects

Create `examples/` directory with:
- Basic MkDocs site with text export
- Custom theme handler example
- Multi-language documentation example
- Large documentation site optimization

## Phase 6: Docker and CI/CD (2-3 days)

### 6.1 Docker Support

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install --no-cache-dir -e .

# Add example usage
```

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  mkdocs:
    build: .
    volumes:
      - ./docs:/docs
    command: mkdocs build
```

### 6.2 Enhanced CI/CD

Update `.github/workflows/ci.yml`:
- Add Docker build tests
- Add integration tests
- Add performance benchmarks
- Add documentation build checks
- Add PyPI publishing workflow

## Phase 7: Advanced Features (2 weeks)

### 7.1 Parallel Processing

Implement concurrent page processing:
```python
from concurrent.futures import ThreadPoolExecutor

class Renderer:
    def process_pages_parallel(self, pages, max_workers=4):
        """Process multiple pages concurrently"""
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for page in pages:
                future = executor.submit(self.process_page, page)
                futures.append(future)
```

### 7.2 Output Format Plugins

Create extensible output format system:
```python
class OutputFormat(ABC):
    @abstractmethod
    def convert(self, html: str, options: dict) -> str:
        pass

class MarkdownFormat(OutputFormat):
    def convert(self, html: str, options: dict) -> str:
        # Existing markdown conversion

class PlainTextFormat(OutputFormat):
    def convert(self, html: str, options: dict) -> str:
        # Existing text conversion

class JSONFormat(OutputFormat):
    def convert(self, html: str, options: dict) -> str:
        # New: Extract structured data to JSON
```

### 7.3 Smart Content Extraction

Add intelligent content extraction:
- Automatic table of contents generation
- Metadata extraction (author, date, tags)
- Code block extraction with language detection
- Image caption extraction

## Timeline and Priorities

### Week 1
- Phase 1: Immediate Fixes (High Priority)
- Phase 2: Packaging and Distribution (High Priority)

### Week 2
- Phase 3: Testing Improvements (Medium Priority)
- Phase 5: Documentation Overhaul (Medium Priority)

### Week 3
- Phase 4: Feature Enhancements (Medium Priority)
- Phase 6: Docker and CI/CD (Low Priority)

### Week 4+
- Phase 7: Advanced Features (Low Priority)

## Success Metrics

1. **Stability**
   - Zero installation failures
   - 95%+ test coverage
   - No critical bugs in production

2. **Elegance**
   - Clean, well-documented code
   - Consistent coding style
   - Intuitive API design

3. **Deployability**
   - One-command installation: `pip install mkdocs-text-export-plugin`
   - Docker support for complex environments
   - Clear upgrade path between versions

## Risks and Mitigation

1. **Breaking Changes**
   - Risk: Updates might break existing installations
   - Mitigation: Semantic versioning, deprecation warnings, migration guide

2. **Performance Impact**
   - Risk: New features might slow down builds
   - Mitigation: Performance benchmarks, optional features, parallel processing

3. **Maintenance Burden**
   - Risk: Too many features increase maintenance
   - Mitigation: Good test coverage, clear documentation, community contributions

## Conclusion

This improvement plan transforms mkdocs-text-export-plugin from a functional tool into a production-ready, enterprise-grade solution. By focusing on stability first, then elegance and deployability, we ensure that existing users benefit immediately while setting the foundation for future growth.