#!/usr/bin/env python3
"""
Broken Link Validator

Validates internal links in markdown files and checks file references.
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple, Set
from urllib.parse import urlparse, unquote


class LinkError:
    def __init__(self, file: str, line: int, link: str, issue: str):
        self.file = file
        self.line = line
        self.link = link
        self.issue = issue

    def __str__(self):
        return f"❌ {
            self.file}:{
            self.line}\n   Link: {
            self.link}\n   Issue: {
                self.issue}"


def find_markdown_files(repo_root: Path) -> List[Path]:
    """Find all markdown files in the repository."""
    md_files: List[Path] = []

    # Search in standard locations
    for pattern in ["**/*.md"]:
        md_files.extend(repo_root.glob(pattern))

    # Exclude certain directories
    exclude_dirs = {".git", "node_modules", "__pycache__", ".venv", "venv"}

    filtered = []
    for f in md_files:
        if not any(ex in f.parts for ex in exclude_dirs):
            filtered.append(f)

    return sorted(filtered)


def extract_links(content: str, file_path: Path) -> List[Tuple[int, str, str]]:
    """Extract all markdown links from content.

    Returns: List of (line_number, link_text, link_url)
    """
    links = []

    # Pattern for markdown links: [text](url)
    pattern = r'\[([^\]]+)\]\(([^\)]+)\)'

    for line_num, line in enumerate(content.split('\n'), 1):
        for match in re.finditer(pattern, line):
            text = match.group(1)
            url = match.group(2)
            links.append((line_num, text, url))

    return links


def is_external_link(url: str) -> bool:
    """Check if URL is external (http/https)."""
    parsed = urlparse(url)
    return parsed.scheme in ('http', 'https')


def resolve_relative_path(base_file: Path, link_url: str, repo_root: Path) -> Path:
    """Resolve a relative link URL to absolute path."""
    # Remove anchor
    if '#' in link_url:
        link_url = link_url.split('#')[0]

    if not link_url:  # Just an anchor
        return base_file

    # Decode URL encoding
    link_url = unquote(link_url)

    # Handle absolute paths from repo root
    if link_url.startswith('/'):
        return repo_root / link_url.lstrip('/')

    # Handle relative paths
    base_dir = base_file.parent
    target = (base_dir / link_url).resolve()

    return target


def validate_links(repo_root: Path) -> List[LinkError]:
    """Validate all markdown links."""
    errors = []
    md_files = find_markdown_files(repo_root)

    print(f"📝 Checking {len(md_files)} markdown files...\n")

    for md_file in md_files:
        rel_path = md_file.relative_to(repo_root)

        try:
            content = md_file.read_text(encoding='utf-8')
        except Exception as e:
            errors.append(LinkError(
                str(rel_path), 0, "", f"Failed to read file: {e}"
            ))
            continue

        links = extract_links(content, md_file)

        for line_num, text, url in links:
            # Skip external links (we only validate internal links)
            if is_external_link(url):
                continue

            # Skip anchors only (same page)
            if url.startswith('#'):
                continue

            # Skip mailto links
            if url.startswith('mailto:'):
                continue

            # Resolve and check if file exists
            try:
                target = resolve_relative_path(md_file, url, repo_root)

                # Check if target exists
                if not target.exists():
                    errors.append(
                        LinkError(
                            str(rel_path),
                            line_num,
                            url,
                            "Target does not exist: "
                            f"{(target.relative_to(repo_root) if target.is_relative_to(repo_root) else target)}"))
                # Check if target is a directory without index
                elif target.is_dir():
                    index_file = target / "README.md"
                    if not index_file.exists():
                        errors.append(
                            LinkError(
                                str(rel_path),
                                line_num,
                                url,
                                f"Link to directory without README.md: {
                                    target.relative_to(repo_root)}"))

            except Exception as e:
                errors.append(LinkError(
                    str(rel_path),
                    line_num,
                    url,
                    f"Error resolving link: {e}"
                ))

    return errors


def find_orphaned_files(repo_root: Path) -> List[str]:
    """Find markdown files that aren't linked from anywhere."""
    # This is a simplified check - just reports files not in standard locations
    orphaned = []

    # Files that should always be in root
    expected_root = {"README.md", "QUICKSTART.md", "LICENSE.md", "CONTRIBUTING.md",
                     "CHANGELOG.md"}

    for md_file in repo_root.glob("*.md"):
        if md_file.name not in expected_root:
            orphaned.append(str(md_file.relative_to(repo_root)))

    return orphaned


def print_results(errors: List[LinkError], orphaned: List[str]) -> bool:
    """Print validation results."""
    print("\n" + "=" * 70)
    print("🔗 Link Validation Results")
    print("=" * 70 + "\n")

    if not errors and not orphaned:
        print("✅ All links are valid!")
        print("=" * 70)
        return True

    if errors:
        print(f"Found {len(errors)} broken link(s):\n")
        for error in errors:
            print(error)
            print()

    if orphaned:
        print(f"Found {len(orphaned)} potential orphaned file(s):\n")
        for file in orphaned:
            print(f"⚠️  {file}")
            print("   May not follow taxonomy rules (should be in docs/)")
        print()

    print("=" * 70)
    print("❌ Validation FAILED")
    print("=" * 70)
    return False


def main():
    """Main validation function."""
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent.parent

    errors = validate_links(repo_root)
    orphaned = find_orphaned_files(repo_root)

    success = print_results(errors, orphaned)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
