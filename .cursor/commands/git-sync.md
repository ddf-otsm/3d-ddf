# /git-sync

This command is intentionally disabled. Do not automate git operations.

- Reason: Git operations can be destructive without manual review.
- Guidance: Execute git commands manually and verify output between steps.
- AI usage policy: The AI must not execute or propose any git commands or scripts. Present the steps below for human-operated, manual use only (no force-push, no `--no-verify`, no chaining).
- Commit messages must be meaningful; do not use generic defaults or placeholders (e.g., "chore: git sync").

Suggested manual flow (run each step yourself, review output after each):

1) Verify repository context
```bash
git rev-parse --show-toplevel
```

2) Sync remotes (and prune deleted refs)
```bash
git fetch --all --prune
```

3) Stage changes
```bash
git add -A
```

4) Run hooks (if configured)
```bash
pre-commit run --all-files
```

5) Commit (single-line, no emojis; describe what changed and why)
```bash
git commit -m "feat(plan): add TL;DR to merge mini prompt for manual flow"
```

6) Push (set upstream on first push if needed)
```bash
git push
# or, if upstream is missing
# git push --set-upstream origin $(git branch --show-current)
```
