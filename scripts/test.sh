#!/bin/bash

# this_file: scripts/test.sh

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[TEST]${NC} $1"
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

print_status "Running test suite for mkdocs-text-export-plugin..."
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

# Install dependencies
print_status "Installing dependencies..."
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install the package in development mode
print_status "Installing package in development mode..."
pip install -e .

# Run code formatting check
print_status "Checking code formatting with black..."
if black --check .; then
    print_success "Code formatting is correct"
else
    print_error "Code formatting issues found. Run 'black .' to fix."
    exit 1
fi

# Run linting
print_status "Running linting with flake8..."
if flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics; then
    print_success "No critical linting issues found"
else
    print_error "Critical linting issues found"
    exit 1
fi

# Run extended linting (warnings)
print_status "Running extended linting checks..."
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

# Run type checking
print_status "Running static type checking with mypy..."
if mypy . --exclude venv --exclude docs/theme-handler/cinder.py --ignore-missing-imports; then
    print_success "No type checking issues found"
else
    print_error "Type checking issues found"
    exit 1
fi

# Run tests
print_status "Running tests with pytest..."
if pytest -v; then
    print_success "All tests passed"
else
    print_error "Some tests failed"
    exit 1
fi

print_success "All tests completed successfully!"