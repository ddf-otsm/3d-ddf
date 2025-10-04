# Blender MCP Update Workflow

This guide explains how we maintain the `blender-mcp` tooling now that it lives directly inside the main repository (no longer as a git submodule).

## Why the Change?
- The upstream project moves quickly and we maintain local customizations.
- Keeping the code as a regular directory simplifies editing and makes it easier to apply project-wide changes.
- We only pull in upstream changes when we explicitly choose to compare and merge them.

## Repository Layout
- `blender-mcp/` is tracked like any other project directory.
- There is no `.gitmodules` entry or nested git repository inside this folder.
- Temporary build artifacts (`.venv`, `uv.lock`, `__pycache__`, `.DS_Store`, etc.) should not be committed.

## Keeping a Backup (Optional)
Before making large edits, create a safe copy:
```bash
cp -R blender-mcp blender-mcp-backup-$(date +%Y%m%d)
```

## Comparing with Upstream (Manual Update Process)
When you want to review the latest upstream changes:

1. **Prepare a temporary workspace**
   ```bash
   mkdir -p /tmp/blender-mcp-update
   cd /tmp/blender-mcp-update
   git clone https://github.com/ahujasid/blender-mcp upstream-blender-mcp
   ```

2. **Compare upstream with our tracked version**
   ```bash
   cd ${PROJECT_ROOT}
   git diff --no-index /tmp/blender-mcp-update/upstream-blender-mcp blender-mcp > /tmp/blender-mcp-update/diff.patch
   ```
   - Review `/tmp/blender-mcp-update/diff.patch` in your editor.
   - This highlights upstream additions, removals, and local changes.

3. **Cherry-pick desired changes**
   - Manually copy updated files from `/tmp/blender-mcp-update/upstream-blender-mcp` into our `blender-mcp/` directory.
   - Resolve conflicts or adapt the upstream code to match our customizations.

4. **Test locally**
   - Run your usual validation steps (e.g., MCP smoke tests, Blender integration tests) to confirm the update works.

5. **Commit the update**
   ```bash
   git add blender-mcp
   git status  # verify only the intended files changed
   git commit -m "Update blender-mcp to <upstream version>"
   ```

6. **Cleanup**
   ```bash
   rm -rf /tmp/blender-mcp-update
   ```

## Optional: Track Upstream as a Remote (Read-Only)
If you frequently update, add the upstream repository as a remote reference without turning it back into a submodule:
```bash
cd blender-mcp
git init  # only if git metadata is absent and you want a throwaway comparison repo
git remote add upstream https://github.com/ahujasid/blender-mcp
git fetch upstream
# Use git diff upstream/main -- <path> to inspect differences, then delete .git when finished
```
> Note: Only do this in a temporary copy—remove any `.git/` metadata before committing to avoid reintroducing nested repos.

## Best Practices
- Never commit `.git/`, `.venv/`, `uv.lock`, or other environment artifacts.
- Document meaningful upstream merges in commit messages.
- Keep this guide updated if the workflow changes.
