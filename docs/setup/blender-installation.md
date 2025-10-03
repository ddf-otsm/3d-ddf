# Blender Installation & Detection Guide

## 🎯 Quick Overview

This guide helps you:
1. ✅ Check if Blender is installed
2. 📦 Install Blender if needed
3. 🔍 Find your Blender installation path
4. ⚙️ Configure Blender for 3D-DDF

---

## 🔍 Check if Blender is Installed

### macOS

Open Terminal and run:

```bash
# Method 1: Check if Blender command exists
which blender

# Method 2: Check default application path
ls -la /Applications/Blender.app

# Method 3: Search for Blender in all common locations
find /Applications -name "Blender.app" -maxdepth 2 2>/dev/null
```

**Expected Output:**
- ✅ If installed: Shows path like `/Applications/Blender.app`
- ❌ If not installed: No output or "command not found"

### Linux

```bash
# Check if Blender is in PATH
which blender

# Check common installation locations
ls -la /usr/bin/blender
ls -la /usr/local/bin/blender
ls -la ~/Applications/blender*

# Check version
blender --version
```

### Windows

Open PowerShell and run:

```powershell
# Check if Blender is in PATH
Get-Command blender -ErrorAction SilentlyContinue

# Check common installation locations
Test-Path "C:\Program Files\Blender Foundation\Blender*"
Test-Path "C:\Program Files (x86)\Blender Foundation\Blender*"

# Check version
blender --version
```

---

## 📦 Install Blender

### Option 1: Official Download (Recommended)

**Best for: Production work, stable releases**

1. Visit [blender.org/download](https://www.blender.org/download/)
2. Download for your OS:
   - **macOS**: `.dmg` file
   - **Linux**: `.tar.xz` or use package manager
   - **Windows**: `.msi` installer
3. Install following platform-specific instructions below

#### macOS Installation
```bash
# After downloading the .dmg file:
# 1. Double-click the .dmg file
# 2. Drag Blender.app to Applications folder
# 3. Verify installation
open /Applications/Blender.app

# Optional: Add to PATH for command line access
echo 'export PATH="/Applications/Blender.app/Contents/MacOS:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Verify
blender --version
```

#### Linux Installation
```bash
# Ubuntu/Debian (apt)
sudo add-apt-repository ppa:thomas-schiex/blender
sudo apt update
sudo apt install blender

# Fedora (dnf)
sudo dnf install blender

# Arch (pacman)
sudo pacman -S blender

# Flatpak (universal)
flatpak install flathub org.blender.Blender

# Verify
blender --version
```

#### Windows Installation
```powershell
# After downloading the .msi installer:
# 1. Double-click the installer
# 2. Follow installation wizard
# 3. Choose "Add Blender to PATH" option
# 4. Verify installation

# Open PowerShell and run:
blender --version

# If not in PATH, add manually:
# System Properties > Environment Variables > Path > Edit
# Add: C:\Program Files\Blender Foundation\Blender 4.x
```

### Option 2: Package Managers

**Best for: Quick setup, automated updates**

#### macOS (Homebrew)
```bash
# Install Homebrew if needed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Blender
brew install --cask blender

# Verify
blender --version
```

#### Linux (Snap)
```bash
sudo snap install blender --classic

# Verify
blender --version
```

#### Windows (Chocolatey)
```powershell
# Install Chocolatey if needed (run as Administrator)
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install Blender
choco install blender

# Verify
blender --version
```

---

## 🔍 Find Your Blender Installation Path

### Automated Detection Script

Save this as `scripts/detect_blender.py`:

```python
#!/usr/bin/env python3
"""
Blender Installation Detector
Finds Blender installations on your system
"""

import os
import sys
import platform
import subprocess
from pathlib import Path
from typing import List, Optional, Dict


def find_blender_installations() -> List[Dict[str, str]]:
    """Find all Blender installations on the system."""
    installations = []
    system = platform.system()
    
    # Common installation paths by OS
    search_paths = {
        'Darwin': [  # macOS
            '/Applications/Blender.app',
            '/Applications/Blender*.app',
            str(Path.home() / 'Applications' / 'Blender.app'),
            '/usr/local/bin/blender',
        ],
        'Linux': [
            '/usr/bin/blender',
            '/usr/local/bin/blender',
            '/snap/bin/blender',
            '/opt/blender/blender',
            str(Path.home() / 'Applications' / 'blender'),
        ],
        'Windows': [
            'C:\\Program Files\\Blender Foundation\\Blender*\\blender.exe',
            'C:\\Program Files (x86)\\Blender Foundation\\Blender*\\blender.exe',
            str(Path.home() / 'AppData' / 'Local' / 'Programs' / 'Blender Foundation'),
        ]
    }
    
    # Check PATH first
    path_blender = check_path_for_blender()
    if path_blender:
        installations.append({
            'path': path_blender,
            'version': get_blender_version(path_blender),
            'source': 'PATH',
            'executable': path_blender
        })
    
    # Search common locations
    for path_pattern in search_paths.get(system, []):
        from glob import glob
        for path in glob(str(path_pattern)):
            if os.path.exists(path):
                executable = get_blender_executable(path)
                if executable and not any(inst['executable'] == executable for inst in installations):
                    installations.append({
                        'path': path,
                        'version': get_blender_version(executable),
                        'source': 'System',
                        'executable': executable
                    })
    
    return installations


def check_path_for_blender() -> Optional[str]:
    """Check if Blender is in system PATH."""
    try:
        result = subprocess.run(
            ['which', 'blender'] if platform.system() != 'Windows' else ['where', 'blender'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip().split('\n')[0]
    except Exception:
        pass
    return None


def get_blender_executable(path: str) -> Optional[str]:
    """Get the Blender executable path from an installation directory."""
    if path.endswith('.exe'):
        return path if os.path.isfile(path) else None
    
    if platform.system() == 'Darwin' and path.endswith('.app'):
        executable = os.path.join(path, 'Contents', 'MacOS', 'Blender')
        return executable if os.path.isfile(executable) else None
    
    if os.path.isfile(path):
        return path
    
    # Try to find blender executable in directory
    possible_names = ['blender', 'blender.exe', 'Blender']
    for name in possible_names:
        exe = os.path.join(path, name)
        if os.path.isfile(exe):
            return exe
    
    return None


def get_blender_version(executable: str) -> str:
    """Get Blender version from executable."""
    try:
        result = subprocess.run(
            [executable, '--version'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            # Parse version from output (e.g., "Blender 4.0.2")
            for line in result.stdout.split('\n'):
                if 'Blender' in line:
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part == 'Blender' and i + 1 < len(parts):
                            return parts[i + 1]
        return 'Unknown'
    except Exception as e:
        return f'Error: {str(e)}'


def main():
    """Main detection routine."""
    print("=" * 60)
    print("🔍 BLENDER INSTALLATION DETECTOR")
    print("=" * 60)
    print()
    
    print(f"System: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version.split()[0]}")
    print()
    
    installations = find_blender_installations()
    
    if not installations:
        print("❌ No Blender installations found!")
        print()
        print("📦 To install Blender:")
        print("   • Visit: https://www.blender.org/download/")
        print("   • Or use package manager (brew, apt, choco, etc.)")
        print()
        return 1
    
    print(f"✅ Found {len(installations)} Blender installation(s):\n")
    
    for i, install in enumerate(installations, 1):
        print(f"[{i}] Blender {install['version']}")
        print(f"    Path:       {install['path']}")
        print(f"    Executable: {install['executable']}")
        print(f"    Source:     {install['source']}")
        print()
    
    # Recommend the best installation
    if installations:
        recommended = installations[0]  # Prefer PATH installation
        print("💡 RECOMMENDED FOR 3D-DDF:")
        print(f"   Use: {recommended['executable']}")
        print()
        
        if platform.system() == 'Darwin':
            print("🔧 To add to PATH (if not already):")
            print(f'   export PATH="{os.path.dirname(recommended["executable"])}:$PATH"')
            print()
    
    print("=" * 60)
    print("📖 For setup instructions, see:")
    print("   docs/setup/installation.md")
    print("   docs/setup/blender-installation.md")
    print("=" * 60)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
```

Run it:

```bash
cd /Users/luismartins/local_repos/3d-ddf
python scripts/detect_blender.py
```

---

## ⚙️ Configure Blender for 3D-DDF

### Step 1: Install the Blender MCP Addon

```bash
# 1. Ensure Blender is installed (see above)

# 2. Open Blender
open /Applications/Blender.app  # macOS
# Or: blender  # Linux/Windows

# 3. In Blender:
#    Edit > Preferences > Add-ons > Install...
#    Navigate to: /Users/luismartins/local_repos/3d-ddf/blender-mcp/addon.py
#    Enable: "Interface: Blender MCP"
```

### Step 2: Start MCP Server

```bash
# In Blender:
# 1. Press 'N' to show sidebar
# 2. Click "BlenderMCP" tab
# 3. Click "Connect to Claude" button
# 4. Should show "Connected" status
```

### Step 3: Configure Environment (Optional)

Create `.env` file in project root:

```bash
# Blender Configuration
BLENDER_HOST=localhost
BLENDER_PORT=9876
BLENDER_TIMEOUT=30

# Optional: Explicit Blender executable path
BLENDER_EXECUTABLE=/Applications/Blender.app/Contents/MacOS/Blender
```

---

## 🧪 Verify Installation

### Quick Test

```bash
cd /Users/luismartins/local_repos/3d-ddf

# 1. Check Blender version
blender --version

# 2. Check Blender can run Python
blender --background --python-expr "import bpy; print('✅ Blender Python OK')"

# 3. Run integration test (requires Blender MCP server running)
python tests/integration/test_blender_mcp_cube.py
```

### Expected Output

```
✅ Blender 4.0.2
✅ Blender Python OK
✅ Connected to Blender at localhost:9876
🎉 ALL VALIDATIONS PASSED!
```

---

## 🆘 Troubleshooting

### "blender: command not found"

**Cause**: Blender not in system PATH

**Fix (macOS)**:
```bash
# Find Blender
ls /Applications/Blender.app

# Add to PATH permanently
echo 'export PATH="/Applications/Blender.app/Contents/MacOS:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Verify
which blender
```

**Fix (Linux)**:
```bash
# If installed via package manager
sudo ln -s /usr/bin/blender /usr/local/bin/blender

# If manual installation
export PATH="/path/to/blender:$PATH"
echo 'export PATH="/path/to/blender:$PATH"' >> ~/.bashrc
```

**Fix (Windows)**:
```powershell
# Add to PATH via System Properties
# 1. Search for "Environment Variables" in Start Menu
# 2. Edit System PATH
# 3. Add: C:\Program Files\Blender Foundation\Blender 4.x
# 4. Restart PowerShell
```

### "ModuleNotFoundError: No module named 'bpy'"

**Cause**: Trying to import Blender modules outside of Blender

**Context**:
- `bpy` (Blender Python API) only available inside Blender
- Tests should mock `bpy` when running outside Blender
- Scripts must check `BLENDER_AVAILABLE` flag

**Fix**:
```python
# Always use conditional imports for Blender modules
try:
    import bpy
    BLENDER_AVAILABLE = True
except ImportError:
    BLENDER_AVAILABLE = False
    bpy = None  # or create mock

# Check before using
if BLENDER_AVAILABLE:
    # Use bpy
    pass
else:
    # Fallback or skip
    pass
```

### "Connection refused" on localhost:9876

**Cause**: Blender MCP server not running

**Fix**:
1. Open Blender
2. Check addon is enabled: `Edit > Preferences > Add-ons` → "Blender MCP"
3. Open sidebar: Press `N` in 3D View
4. Click **"BlenderMCP"** tab
5. Click **"Connect to Claude"** button
6. Verify "Connected" status

### Tests requiring Blender fail

**Cause**: Tests need live Blender instance

**Fix**:
1. Ensure Blender is running with MCP server connected (see above)
2. Run Blender-dependent tests separately:
   ```bash
   # Skip Blender tests
   pytest -m "not blender"
   
   # Run only with Blender running
   pytest tests/integration/test_blender_mcp_cube.py
   ```
3. Check test uses proper mocking for unit tests

---

## 📚 Additional Resources

- **Official Blender Docs**: https://docs.blender.org/
- **Blender Python API**: https://docs.blender.org/api/current/
- **Blender MCP GitHub**: https://github.com/ahujasid/blender-mcp
- **3D-DDF Installation Guide**: [docs/setup/installation.md](./installation.md)
- **3D-DDF Troubleshooting**: [docs/setup/troubleshooting.md](./troubleshooting.md)

---

## 🎯 Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│ BLENDER QUICK REFERENCE                                 │
├─────────────────────────────────────────────────────────┤
│ Check if installed:                                     │
│   macOS:   which blender                                │
│   Linux:   which blender                                │
│   Windows: Get-Command blender                          │
│                                                         │
│ Install:                                                │
│   macOS:   brew install --cask blender                  │
│   Linux:   sudo apt install blender                     │
│   Windows: choco install blender                        │
│   All:     https://blender.org/download                 │
│                                                         │
│ Verify:                                                 │
│   blender --version                                     │
│   python scripts/detect_blender.py                      │
│                                                         │
│ MCP Server:                                             │
│   1. Open Blender                                       │
│   2. Press N → BlenderMCP tab                           │
│   3. Click "Connect to Claude"                          │
│   4. Verify "Connected" status                          │
│                                                         │
│ Troubleshooting:                                        │
│   docs/setup/troubleshooting.md                         │
│   docs/setup/blender-installation.md (this file)        │
└─────────────────────────────────────────────────────────┘
```

