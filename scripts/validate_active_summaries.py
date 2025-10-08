#!/usr/bin/env python3

import sys
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple

SUMMARY_NAME_PATTERN = re.compile(r"^ACTIVE_PLANS_EXECUTION_SUMMARY_(?P<date>[^/]+?)(?P<finals>(?:_FINAL)*)\.md$")


def extract_summary_info(markdown_path: Path) -> Tuple[str, int]:
    """Return (base_key, final_count) for a summary filename.

    base_key is the filename without any _FINAL suffixes and without extension.
    final_count is how many times "_FINAL" occurs at the end before ".md".
    """
    match = SUMMARY_NAME_PATTERN.match(markdown_path.name)
    if not match:
        return "", 0

    date_slug = match.group("date")
    finals_segment = match.group("finals") or ""
    final_count = finals_segment.count("_FINAL")

    base_key = f"ACTIVE_PLANS_EXECUTION_SUMMARY_{date_slug}"
    return base_key, final_count


def find_invalid_files(active_dir: Path) -> Tuple[List[str], Dict[str, List[Path]]]:
    """Identify invalid summary filenames and group files by base_key.

    Invalid cases:
    - Any filename with repeated _FINAL (>= 2 occurrences)
    - More than one base or more than one single-final variant for the same date
    - More than two variants total (base + single _FINAL) for the same date
    """
    invalid_messages: List[str] = []
    grouped_by_base: Dict[str, List[Path]] = defaultdict(list)

    for markdown_path in active_dir.glob("*.md"):
        if not markdown_path.name.startswith("ACTIVE_PLANS_EXECUTION_SUMMARY_"):
            continue

        base_key, final_count = extract_summary_info(markdown_path)
        if not base_key:
            # Non-matching files are ignored here
            continue

        grouped_by_base[base_key].append(markdown_path)

        if final_count >= 2:
            invalid_messages.append(
                f"{markdown_path} (invalid: repeated '_FINAL' segments)"
            )

    # Detect duplicates and excessive variants per base_key
    for base_key, files in grouped_by_base.items():
        base_variants = [f for f in files if extract_summary_info(f)[1] == 0]
        single_final_variants = [f for f in files if extract_summary_info(f)[1] == 1]
        repeated_final_variants = [f for f in files if extract_summary_info(f)[1] >= 2]

        # More than one base or more than one single-final is invalid
        if len(base_variants) > 1:
            invalid_messages.append(
                f"{base_key}: multiple base variants found: {[p.name for p in base_variants]}"
            )
        if len(single_final_variants) > 1:
            invalid_messages.append(
                f"{base_key}: multiple single-final variants found: {[p.name for p in single_final_variants]}"
            )

        # Any extra variants beyond base + single final are invalid
        total_expected = min(1, len(base_variants)) + min(1, len(single_final_variants))
        if len(files) > total_expected + len(repeated_final_variants):
            invalid_messages.append(
                f"{base_key}: too many variants present: {[p.name for p in files]}"
            )

    return invalid_messages, grouped_by_base


def main() -> None:
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent.parent
    active_dir = repo_root / "docs" / "plans" / "active"

    if not active_dir.exists():
        print("✅ No active plans directory found; skipping validation.")
        sys.exit(0)

    invalid_messages, grouped = find_invalid_files(active_dir)

    if invalid_messages:
        print("\n" + "=" * 70)
        print("❌ Invalid Active Plan Summary Filenames Detected")
        print("=" * 70 + "\n")
        for message in invalid_messages:
            print(f"- {message}")
        print("\n💡 Allowed patterns (per date):")
        print("   - ACTIVE_PLANS_EXECUTION_SUMMARY_<DATE>.md")
        print("   - ACTIVE_PLANS_EXECUTION_SUMMARY_<DATE>_FINAL.md")
        print("\nTo auto-fix issues, run: python3 scripts/cleanup_active_summaries.py --fix")
        sys.exit(1)

    total = sum(1 for _ in active_dir.glob("ACTIVE_PLANS_EXECUTION_SUMMARY_*.md"))
    print(f"✅ Active plan summaries look good. Found {total} valid file(s).")
    sys.exit(0)


if __name__ == "__main__":
    main()


