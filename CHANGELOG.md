# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Cleaned up code structure and removed redundant imports
- Simplified theme handler implementations
- Streamlined setup.py dependencies and configuration

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