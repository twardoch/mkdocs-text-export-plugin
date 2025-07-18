#!/bin/bash

# this_file: scripts/build.sh

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[BUILD]${NC} $1"
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

print_status "Building mkdocs-text-export-plugin..."
print_status "Project root: $PROJECT_ROOT"

cd "$PROJECT_ROOT"

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    print_error "Not in a git repository!"
    exit 1
fi

# Get version information
VERSION=$(python version.py)
print_status "Version: $VERSION"

# Clean previous builds
print_status "Cleaning previous builds..."
rm -rf build/
rm -rf dist/
rm -rf *.egg-info/

# Install dependencies
print_status "Installing dependencies..."
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install the package in development mode
print_status "Installing package in development mode..."
pip install -e .

# Build the package
print_status "Building source and wheel distributions..."
python -m build

# Check if build was successful
if [ -d "dist" ] && [ "$(ls -A dist)" ]; then
    print_success "Build completed successfully!"
    print_status "Built packages:"
    ls -la dist/
else
    print_error "Build failed - no packages created"
    exit 1
fi

print_success "Build script completed successfully!"