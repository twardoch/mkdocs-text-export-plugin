#!/bin/bash

# this_file: scripts/release.sh

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[RELEASE]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

print_status "Preparing release for mkdocs-text-export-plugin..."
print_status "Project root: $PROJECT_ROOT"

cd "$PROJECT_ROOT"

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    print_error "Not in a git repository!"
    exit 1
fi

# Check if working directory is clean
if [ -n "$(git status --porcelain)" ]; then
    print_error "Working directory is not clean. Please commit or stash changes."
    git status --short
    exit 1
fi

# Get version information
VERSION=$(python version.py)
print_status "Current version: $VERSION"

# Check if this is a release version
if python -c "from version import is_release_version; exit(0 if is_release_version() else 1)"; then
    print_success "This is a release version"
else
    print_error "This is not a release version. Please create a git tag first."
    print_status "Example: git tag v1.2.3"
    exit 1
fi

# Check if we're on the main branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" != "main" ] && [ "$CURRENT_BRANCH" != "master" ]; then
    print_warning "You are not on the main/master branch (current: $CURRENT_BRANCH)"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_status "Release cancelled"
        exit 0
    fi
fi

# Run tests
print_status "Running test suite..."
if ! ./scripts/test.sh; then
    print_error "Tests failed. Cannot proceed with release."
    exit 1
fi

# Build the package
print_status "Building package..."
if ! ./scripts/build.sh; then
    print_error "Build failed. Cannot proceed with release."
    exit 1
fi

# Check if PyPI credentials are available
if [ -z "${PYPI_USERNAME:-}" ] && [ -z "${PYPI_TOKEN:-}" ]; then
    print_warning "No PyPI credentials found in environment variables."
    print_status "To publish to PyPI, set PYPI_USERNAME and PYPI_PASSWORD or PYPI_TOKEN"
    print_status "For now, just building the package..."
else
    print_status "PyPI credentials found. Ready to publish."
    
    # Optional: Upload to PyPI
    read -p "Upload to PyPI? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Uploading to PyPI..."
        
        if [ -n "${PYPI_TOKEN:-}" ]; then
            # Use API token
            python -m twine upload dist/* --username __token__ --password "$PYPI_TOKEN"
        else
            # Use username/password
            python -m twine upload dist/* --username "$PYPI_USERNAME" --password "$PYPI_PASSWORD"
        fi
        
        if [ $? -eq 0 ]; then
            print_success "Package uploaded to PyPI successfully!"
        else
            print_error "Failed to upload to PyPI"
            exit 1
        fi
    fi
fi

print_success "Release preparation completed successfully!"
print_status "Version: $VERSION"
print_status "Built packages are in: dist/"

# Display next steps
print_status "Next steps:"
print_status "1. If not already done, push the tag: git push origin v$VERSION"
print_status "2. Create a GitHub release with the tag"
print_status "3. Upload the built packages as release assets"