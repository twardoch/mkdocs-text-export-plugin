#!/usr/bin/env python3
"""
Version management utilities for git-tag-based semversioning.
"""

import subprocess
import re
from pathlib import Path


def get_version():
    """
    Get version from git tags, falling back to a default if not available.

    Returns:
        str: Version string in semver format (e.g., "1.2.3" or "1.2.3-dev.4+abc123")
    """
    try:
        # Get the current git describe output
        result = subprocess.run(
            ["git", "describe", "--tags", "--long", "--dirty"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent,
            check=False,
        )

        if result.returncode == 0:
            git_describe = result.stdout.strip()
            return parse_git_describe(git_describe)
        else:
            # If no tags exist, try to get commit hash
            result = subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent,
                check=False,
            )
            if result.returncode == 0:
                commit_hash = result.stdout.strip()
                return f"0.0.0.dev0+{commit_hash}"
            else:
                return "0.0.0.dev0+unknown"
    except Exception:
        return "0.0.0.dev0+unknown"


def parse_git_describe(git_describe):
    """
    Parse git describe output into a semver-compatible version string.

    Args:
        git_describe (str): Output from 'git describe --tags --long --dirty'

    Returns:
        str: Semver-compatible version string
    """
    # Handle dirty working directory
    dirty = ""
    if git_describe.endswith("-dirty"):
        dirty = ".dirty"
        git_describe = git_describe[:-6]

    # Parse the git describe format: tag-commits_since_tag-commit_hash
    # Example: v1.2.3-5-g1234567 or 1.2.3-5-g1234567
    pattern = r"^v?(\d+\.\d+\.\d+)(?:-(\d+)-g([a-f0-9]+))?$"
    match = re.match(pattern, git_describe)

    if match:
        version, commits_since_tag, commit_hash = match.groups()

        if commits_since_tag and int(commits_since_tag) > 0:
            # We're ahead of the tag, create a pre-release version
            return f"{version}.dev{commits_since_tag}+{commit_hash}{dirty}"
        else:
            # We're exactly on a tag
            if dirty:
                # PEP 440 compliant dirty version
                return f"{version}.dev0+dirty"
            else:
                return version
    else:
        # Fallback for unexpected format
        return f"0.0.0.dev0+unknown.{git_describe}"


def is_release_version():
    """
    Check if the current version is a release version (no .dev suffix).

    Returns:
        bool: True if this is a release version, False otherwise
    """
    version = get_version()
    return ".dev" not in version and "+dirty" not in version


if __name__ == "__main__":
    print(get_version())
