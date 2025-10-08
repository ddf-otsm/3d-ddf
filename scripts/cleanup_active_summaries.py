#!/usr/bin/env python3

import argparse
import re
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

SUMMARY_NAME_PATTERN = re.compile(r"^(?P<prefix>ACTIVE_PLANS_EXECUTION_SUMMARY_)(?P<date>[^/]+?)(?P<finals>(?:_FINAL)*)\.md$")


def extract(markdown_path: Path) -> Tuple[str, str, int]:
    match = SUMMARY_NAME_PATTERN.match(markdown_path.name)
    if not match:
        return "", "", 0
    prefix = match.group("prefix")
    date_slug = match.group("date")
    finals_segment = match.group("finals") or ""
    final_count = finals_segment.count("_FINAL")
    return prefix, date_slug, final_count


def to_finished_folder_name(date_slug: str) -> str:
    # Example: OCT_7_2025 -> oct-7-2025
    return date_slug.replace("_", "-").lower()


def choose_canonical(files: List[Path]) -> Path:
    # Prefer single-final variant, else base variant, else first file
    single_final = [p for p in files if extract(p)[2] == 1]
    if single_final:
        return sorted(single_final)[0]
    base = [p for p in files if extract(p)[2] == 0]
    if base:
        return sorted(base)[0]
    return sorted(files)[0]


def canonical_name(prefix: str, date_slug: str, final_count: int) -> str:
    if final_count >= 2:
        return f"{prefix}{date_slug}_FINAL.md"
    elif final_count == 1:
        return f"{prefix}{date_slug}_FINAL.md"
    else:
        return f"{prefix}{date_slug}.md"


def cleanup(active_dir: Path, finished_dir: Path, dry_run: bool) -> List[str]:
    actions: List[str] = []

    # Group files by base date slug
    groups: Dict[str, List[Path]] = {}
    for p in active_dir.glob("ACTIVE_PLANS_EXECUTION_SUMMARY_*.md"):
        prefix, date_slug, _ = extract(p)
        if not date_slug:
            continue
        groups.setdefault(date_slug, []).append(p)

    for date_slug, files in sorted(groups.items()):
        keep_path = choose_canonical(files)
        keep_prefix, keep_date, keep_final_count = extract(keep_path)
        desired_keep_name = canonical_name(keep_prefix, keep_date, keep_final_count)
        desired_keep_path = keep_path.with_name(desired_keep_name)

        if keep_path.name != desired_keep_name:
            if dry_run:
                actions.append(f"RENAME {keep_path} -> {desired_keep_path}")
            else:
                keep_path.rename(desired_keep_path)
                actions.append(f"Renamed {keep_path.name} -> {desired_keep_path.name}")
            keep_path = desired_keep_path

        # Move the rest to finished folder
        archive_root = finished_dir / f"execution-summaries-{to_finished_folder_name(date_slug)}"
        if not dry_run:
            archive_root.mkdir(parents=True, exist_ok=True)

        for extra in files:
            if extra.resolve() == keep_path.resolve():
                continue
            destination = archive_root / extra.name
            if dry_run:
                actions.append(f"MOVE  {extra} -> {destination}")
            else:
                shutil.move(str(extra), str(destination))
                actions.append(f"Moved {extra} -> {destination}")

    if not actions:
        actions.append("No changes needed. Active summaries already canonical.")

    return actions


def main() -> None:
    parser = argparse.ArgumentParser(description="Canonicalize active execution summaries and archive duplicates.")
    parser.add_argument("--fix", action="store_true", help="Apply fixes (default: dry-run)")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    active_dir = repo_root / "docs" / "plans" / "active"
    finished_dir = repo_root / "docs" / "plans" / "finished"

    if not active_dir.exists():
        print("✅ No active plans directory found; nothing to clean.")
        return

    dry_run = not args.fix
    actions = cleanup(active_dir, finished_dir, dry_run)

    print("\n" + "=" * 70)
    print("🧹 Active Summaries Cleanup" + (" (dry-run)" if dry_run else ""))
    print("=" * 70 + "\n")
    for a in actions:
        print(f"- {a}")
    print()
    if dry_run:
        print("💡 Run with --fix to apply the above changes.")
    else:
        print("✅ Cleanup applied.")


if __name__ == "__main__":
    main()


