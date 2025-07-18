#!/usr/bin/env python3
"""
MkDocs Text Export Plugin

An MkDocs plugin to export content pages as plain-text or Markdown files.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path so we can import version
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from version import get_version

    __version__ = get_version()
except ImportError:
    # Fallback version if version.py is not available
    __version__ = "1.0.0"

__all__ = ["__version__"]
