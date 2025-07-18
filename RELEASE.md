# Release Process

This document describes the release process for mkdocs-text-export-plugin using git-tag-based semversioning.

## Overview

The project uses git tags for versioning and automated CI/CD pipelines for releases. Version numbers follow semantic versioning (semver) format: `MAJOR.MINOR.PATCH`.

## Version Management

### How Versioning Works

1. **Git Tags**: Release versions are determined by git tags in the format `vX.Y.Z` (e.g., `v1.2.3`)
2. **Dynamic Versioning**: The `version.py` script automatically determines the current version based on git tags
3. **Development Versions**: Between releases, versions have `-dev.N+hash` suffix (e.g., `1.2.3-dev.5+abc123`)

### Version Detection Logic

- **On a tag**: `v1.2.3` → `1.2.3`
- **Ahead of tag**: `v1.2.3-5-gabc123` → `1.2.3-dev.5+abc123`
- **Dirty working directory**: `v1.2.3-dirty` → `1.2.3-dirty`
- **No tags**: `0.0.0-dev.0+abc123`

## Local Development

### Prerequisites

- Python 3.10+
- Git
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/twardoch/mkdocs-text-export-plugin.git
cd mkdocs-text-export-plugin

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install in development mode
pip install -e .
```

### Running Tests

```bash
# Run all tests
./scripts/test.sh

# Or run individual components
black --check .                    # Code formatting
flake8 .                           # Linting
mypy .                             # Type checking
pytest -v                          # Unit tests
```

### Building

```bash
# Build packages
./scripts/build.sh

# The built packages will be in dist/
```

## Release Process

### 1. Prepare for Release

1. Ensure all changes are committed and pushed
2. Update `CHANGELOG.md` with release notes
3. Run tests to ensure everything works:
   ```bash
   ./scripts/test.sh
   ```

### 2. Create Release Tag

Create and push a git tag:

```bash
# Create a new tag (replace X.Y.Z with actual version)
git tag v1.2.3

# Push the tag
git push origin v1.2.3
```

### 3. Automated Release Pipeline

When a tag is pushed, GitHub Actions automatically:

1. **Runs tests** on multiple platforms (Ubuntu, Windows, macOS) and Python versions (3.10, 3.11, 3.12)
2. **Builds packages** (source and wheel distributions)
3. **Creates GitHub release** with:
   - Release notes
   - Built packages as attachments
4. **Publishes to PyPI** (if configured)

### 4. Manual Release (Alternative)

If you prefer manual release:

```bash
# Run the release script
./scripts/release.sh

# This will:
# - Check if on a release tag
# - Run tests
# - Build packages
# - Optionally upload to PyPI
```

## GitHub Actions Configuration

### CI/CD Pipeline (`.github/workflows/ci.yml`)

Triggers on:
- Push to main/master branch
- Pull requests
- Release events

Features:
- Multi-platform testing (Ubuntu, Windows, macOS)
- Multi-Python version testing (3.10, 3.11, 3.12)
- Code quality checks (black, flake8, mypy)
- Package building and artifact upload

### Release Pipeline (`.github/workflows/release.yml`)

Triggers on:
- Git tag push (format: `v*`)

Features:
- Complete test suite
- Package building
- GitHub release creation
- PyPI publishing (if configured)

## PyPI Publishing

### Setup

1. Create a PyPI account and API token
2. Add the token as a GitHub secret named `PYPI_API_TOKEN`
3. Alternatively, configure trusted publishing (recommended)

### Trusted Publishing (Recommended)

1. Go to PyPI project settings
2. Configure GitHub Actions as a trusted publisher
3. Remove the `password` line from the release workflow
4. Uncomment the `attestations: true` line

## Scripts

### `scripts/test.sh`

Runs the complete test suite:
- Code formatting check (black)
- Linting (flake8)
- Type checking (mypy)
- Unit tests (pytest)

### `scripts/build.sh`

Builds the package:
- Installs dependencies
- Builds source and wheel distributions
- Places results in `dist/`

### `scripts/release.sh`

Prepares and executes a release:
- Checks for clean working directory
- Verifies this is a release version
- Runs tests
- Builds packages
- Optionally uploads to PyPI

## Troubleshooting

### Version Detection Issues

Check version detection:
```bash
python version.py
```

Common issues:
- Not in a git repository
- No git tags exist
- Git not available in PATH

### Build Issues

1. Ensure all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

2. Check for Python version compatibility (3.10+)

3. Verify git repository status:
   ```bash
   git status
   git describe --tags --long --dirty
   ```

### Release Issues

1. **"Not a release version"**: You're not on a git tag. Create and checkout a tag first.
2. **"Working directory not clean"**: Commit or stash changes before releasing.
3. **Tests failing**: Fix test failures before proceeding with release.

## Best Practices

1. **Always run tests** before creating a release tag
2. **Update CHANGELOG.md** with each release
3. **Use semantic versioning** for tags
4. **Test on multiple platforms** before releasing
5. **Keep dependencies up to date** in requirements files

## Example Release Workflow

```bash
# 1. Development work
git add .
git commit -m "feat: add new feature"
git push origin main

# 2. Prepare for release
./scripts/test.sh                    # Run tests
# Update CHANGELOG.md
git add CHANGELOG.md
git commit -m "docs: update changelog for v1.2.3"
git push origin main

# 3. Create release
git tag v1.2.3
git push origin v1.2.3

# 4. GitHub Actions automatically handles the rest!
```

The tag push triggers the release pipeline, which will:
- Run tests on all platforms
- Build packages
- Create GitHub release
- Publish to PyPI
- All automatically!