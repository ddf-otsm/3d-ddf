#!/usr/bin/env python3
"""
Blender Installation Detector
Finds Blender installations on your system and provides configuration guidance
"""

import os
import sys
import platform
import subprocess
from pathlib import Path
from typing import List, Optional, Dict
from glob import glob


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
        for path in glob(str(path_pattern)):
            if os.path.exists(path):
                executable = get_blender_executable(path)
                if executable and not any(
                        inst['executable'] == executable for inst in installations):
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
        if platform.system() == 'Windows':
            result = subprocess.run(
                ['where', 'blender'],
                capture_output=True,
                text=True,
                timeout=5
            )
        else:
            result = subprocess.run(
                ['which', 'blender'],
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
        if platform.system() == 'Darwin':
            print("   • brew install --cask blender")
        elif platform.system() == 'Linux':
            print("   • sudo apt install blender       (Ubuntu/Debian)")
            print("   • sudo dnf install blender       (Fedora)")
            print("   • sudo pacman -S blender         (Arch)")
        elif platform.system() == 'Windows':
            print("   • choco install blender          (Chocolatey)")
        print("   • Visit: https://www.blender.org/download/")
        print()
        print("📖 See: docs/setup/blender-installation.md")
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

        if platform.system() == 'Darwin' and recommended['source'] != 'PATH':
            print("🔧 To add to PATH:")
            print(
                f'   echo \'export PATH="{
                    os.path.dirname(
                        recommended["executable"])}:$PATH"\' >> ~/.zshrc')
            print('   source ~/.zshrc')
            print()
        elif platform.system() == 'Linux' and recommended['source'] != 'PATH':
            print("🔧 To add to PATH:")
            print(
                f'   echo \'export PATH="{
                    os.path.dirname(
                        recommended["executable"])}:$PATH"\' >> ~/.bashrc')
            print('   source ~/.bashrc')
            print()

    print("=" * 60)
    print("📚 NEXT STEPS:")
    print("=" * 60)
    print()
    print("1. Install Blender MCP Addon:")
    print("   • Open Blender")
    print("   • Edit > Preferences > Add-ons > Install...")
    print("   • Select: blender-mcp/addon.py")
    print("   • Enable: 'Interface: Blender MCP'")
    print()
    print("2. Start MCP Server:")
    print("   • Press 'N' in Blender 3D View")
    print("   • Click 'BlenderMCP' tab")
    print("   • Click 'Connect to Claude'")
    print()
    print("3. Restart Cursor and look for 🔨 icon")
    print()
    print("=" * 60)
    print("📖 Documentation:")
    print("   • docs/setup/blender-installation.md  (Installation guide)")
    print("   • docs/setup/installation.md          (MCP setup)")
    print("   • docs/setup/troubleshooting.md       (Common issues)")
    print("   • QUICKSTART.md                       (Quick start)")
    print("=" * 60)

    return 0


if __name__ == '__main__':
    sys.exit(main())
