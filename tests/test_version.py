#!/usr/bin/env python3
"""
Tests for version management utilities.
"""

import pytest
from unittest.mock import patch, MagicMock
from version import get_version, parse_git_describe, is_release_version


class TestParseGitDescribe:
    """Test the parse_git_describe function."""

    def test_exact_tag(self):
        """Test parsing when exactly on a tag."""
        result = parse_git_describe("v1.2.3-0-g1234567")
        assert result == "1.2.3"

    def test_exact_tag_without_v_prefix(self):
        """Test parsing when exactly on a tag without v prefix."""
        result = parse_git_describe("1.2.3-0-g1234567")
        assert result == "1.2.3"

    def test_commits_ahead_of_tag(self):
        """Test parsing when commits ahead of tag."""
        result = parse_git_describe("v1.2.3-5-g1234567")
        assert result == "1.2.3.dev5+1234567"

    def test_commits_ahead_of_tag_without_v_prefix(self):
        """Test parsing when commits ahead of tag without v prefix."""
        result = parse_git_describe("1.2.3-5-g1234567")
        assert result == "1.2.3.dev5+1234567"

    def test_dirty_working_directory(self):
        """Test parsing with dirty working directory."""
        result = parse_git_describe("v1.2.3-0-g1234567-dirty")
        assert result == "1.2.3.dev0+dirty"

    def test_dirty_working_directory_with_commits(self):
        """Test parsing with dirty working directory and commits ahead."""
        result = parse_git_describe("v1.2.3-5-g1234567-dirty")
        assert result == "1.2.3.dev5+1234567.dirty"

    def test_invalid_format(self):
        """Test parsing with invalid format."""
        result = parse_git_describe("invalid-format")
        assert result == "0.0.0.dev0+unknown.invalid-format"


class TestGetVersion:
    """Test the get_version function."""

    @patch("subprocess.run")
    def test_successful_git_describe(self, mock_run):
        """Test successful git describe."""
        mock_run.return_value = MagicMock(returncode=0, stdout="v1.2.3-5-g1234567\n")

        result = get_version()
        assert result == "1.2.3.dev5+1234567"

    @patch("subprocess.run")
    def test_no_tags_available(self, mock_run):
        """Test when no tags are available."""

        def side_effect(*args, **kwargs):
            if "describe" in args[0]:
                return MagicMock(returncode=1, stdout="")
            else:  # rev-parse
                return MagicMock(returncode=0, stdout="abc123\n")

        mock_run.side_effect = side_effect

        result = get_version()
        assert result == "0.0.0.dev0+abc123"

    @patch("subprocess.run")
    def test_git_not_available(self, mock_run):
        """Test when git is not available."""
        mock_run.side_effect = Exception("Git not found")

        result = get_version()
        assert result == "0.0.0.dev0+unknown"

    @patch("subprocess.run")
    def test_no_git_repository(self, mock_run):
        """Test when not in a git repository."""
        mock_run.return_value = MagicMock(returncode=128, stdout="")

        result = get_version()
        assert result == "0.0.0.dev0+unknown"


class TestIsReleaseVersion:
    """Test the is_release_version function."""

    @patch("version.get_version")
    def test_release_version(self, mock_get_version):
        """Test with a release version."""
        mock_get_version.return_value = "1.2.3"
        assert is_release_version() is True

    @patch("version.get_version")
    def test_dev_version(self, mock_get_version):
        """Test with a dev version."""
        mock_get_version.return_value = "1.2.3.dev5+abc123"
        assert is_release_version() is False

    @patch("version.get_version")
    def test_dirty_version(self, mock_get_version):
        """Test with a dirty version."""
        mock_get_version.return_value = "1.2.3.dev0+dirty"
        assert is_release_version() is False

    @patch("version.get_version")
    def test_unknown_version(self, mock_get_version):
        """Test with an unknown version."""
        mock_get_version.return_value = "0.0.0.dev0+unknown"
        assert is_release_version() is False
