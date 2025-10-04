#!/usr/bin/env python3
"""
Validate that documentation and scripts don't contain hardcoded paths.

This script checks for common hardcoded path patterns that should use
environment variables instead:
- /Users/... (macOS user paths)
- /Applications/... (macOS app paths)
- C:\\... (Windows paths)
- /home/... (Linux user paths)
- /local_repos/... (specific directory names)

Allowed exceptions:
- Example paths in comments or markdown code blocks labeled as examples
- .env.example file (contains example paths by design)
- This validation script itself
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple

# Patterns to detect hardcoded paths
HARDCODED_PATH_PATTERNS = [
    (r'/Users/[a-zA-Z0-9_-]+', 'macOS user path'),
    (r'/Applications/[a-zA-Z]', 'macOS application path'),
    (r'C:\\\\[a-zA-Z]', 'Windows drive path'),
    (r'/home/[a-zA-Z0-9_-]+', 'Linux user path'),
    (r'/local_repos/', 'Specific directory name'),
]

# Files and directories to skip
SKIP_PATTERNS = [
    '.git/',
    '__pycache__/',
    '.mypy_cache/',  # Type checking cache
    '.pytest_cache/',  # Pytest cache
    'venv/',
    '.venv/',
    'node_modules/',
    '.DS_Store',
    '*.pyc',
    '*.pyo',
    'htmlcov/',
    '.coverage',
    '*.egg-info/',
    'logs/',
    'renders/',  # Render output directories
    'exports/',  # Export directories
    '.env.example',  # Allowed to have example paths
    'scripts/validate_paths.py',  # This script itself
    'data/logos/AGENTS.md',  # Example commands for agents
]

# File extensions to check
CHECK_EXTENSIONS = [
    '.md',    # Markdown docs
    '.py',    # Python scripts
    '.sh',    # Shell scripts
    '.bash',  # Bash scripts
    '.json',  # Config files (may have paths)
    '.yaml',  # Config files
    '.yml',   # Config files
]

def should_skip(path: Path) -> bool:
    """Check if a path should be skipped."""
    path_str = str(path)
    for pattern in SKIP_PATTERNS:
        if pattern.endswith('/') and f'/{pattern}' in f'/{path_str}/':
            return True
        if pattern.startswith('*') and path_str.endswith(pattern[1:]):
            return True
        if pattern in path_str:
            return True
    return False

def is_exception_context(line: str, line_num: int, lines: List[str]) -> bool:
    """
    Check if the line is in an allowed exception context:
    - Inside a code block marked as example
    - In a comment explicitly marked as example
    - Part of environment variable documentation
    """
    # Check for example/sample markers in the line or nearby lines
    example_keywords = ['example', 'sample', 'e.g.', 'for instance', 'placeholder']
    
    # Check current line
    lower_line = line.lower()
    if any(keyword in lower_line for keyword in example_keywords):
        return True
    
    # Check if we're in a markdown code block with example context
    if line_num > 0:
        context_start = max(0, line_num - 3)
        context = ' '.join(lines[context_start:line_num]).lower()
        if any(keyword in context for keyword in example_keywords):
            return True
    
    # Check for environment variable patterns (these are documenting vars)
    if '${' in line or '$(' in line or 'PROJECT_ROOT' in line or 'BLENDER' in line:
        return True
    
    # Check for .env file references (these are good)
    if '.env' in line:
        return True
    
    return False

def check_file(file_path: Path, project_root: Path) -> List[Tuple[int, str, str]]:
    """
    Check a file for hardcoded paths.
    Returns list of (line_number, line_content, pattern_name) tuples.
    """
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            
        for line_num, line in enumerate(lines, 1):
            # Skip if in exception context
            if is_exception_context(line, line_num - 1, [l.rstrip() for l in lines]):
                continue
            
            # Check each pattern
            for pattern, pattern_name in HARDCODED_PATH_PATTERNS:
                if re.search(pattern, line):
                    issues.append((line_num, line.strip(), pattern_name))
                    break  # Only report first match per line
    
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}", file=sys.stderr)
    
    return issues

def validate_paths(project_root: Path) -> int:
    """
    Validate all files in the project for hardcoded paths.
    Returns exit code (0 = success, 1 = errors found).
    """
    print("🔍 Checking for hardcoded paths in documentation and scripts...\n")
    
    all_issues = {}
    total_files_checked = 0
    
    # Walk through project directory
    for root, dirs, files in os.walk(project_root):
        # Filter out directories to skip
        dirs[:] = [d for d in dirs if not should_skip(Path(root) / d)]
        
        for file in files:
            file_path = Path(root) / file
            
            # Skip files that don't match our extensions
            if not any(file.endswith(ext) for ext in CHECK_EXTENSIONS):
                continue
            
            # Skip files in skip patterns
            if should_skip(file_path):
                continue
            
            total_files_checked += 1
            issues = check_file(file_path, project_root)
            
            if issues:
                rel_path = file_path.relative_to(project_root)
                all_issues[rel_path] = issues
    
    # Report results
    print(f"📊 Checked {total_files_checked} files\n")
    
    if not all_issues:
        print("✅ No hardcoded paths found!")
        return 0
    
    print(f"❌ Found hardcoded paths in {len(all_issues)} file(s):\n")
    
    for file_path, issues in sorted(all_issues.items()):
        print(f"  {file_path}:")
        for line_num, line_content, pattern_name in issues:
            print(f"    Line {line_num} ({pattern_name}):")
            print(f"      {line_content[:100]}{'...' if len(line_content) > 100 else ''}")
        print()
    
    print("💡 Recommendations:")
    print("  - Use ${PROJECT_ROOT} for project paths")
    print("  - Use $BLENDER for Blender executable paths")
    print("  - Use os.environ.get('VAR') in Python scripts")
    print("  - Document platform-specific paths with examples")
    print("  - See .env.example for portable path patterns\n")
    
    return 1

def main():
    """Main entry point."""
    # Determine project root
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    
    print(f"Project root: {project_root}\n")
    
    exit_code = validate_paths(project_root)
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
