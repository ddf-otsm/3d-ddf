#!/usr/bin/env python3
"""
Phase 1 Main Entry Point
Provides a unified interface for Phase 1 asset integration
"""

import os
import sys
import argparse
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def run_tests():
    """Run Phase 1 tests"""
    print("🧪 Running Phase 1 tests...")
    
    test_script = Path(__file__).parent / "tests" / "test_phase1.py"
    if test_script.exists():
        os.system(f"python {test_script}")
    else:
        print("❌ Test script not found")

def run_workflow():
    """Run Phase 1 workflow"""
    print("🚀 Running Phase 1 workflow...")
    
    workflow_script = Path(__file__).parent / "scripts" / "run_phase1_workflow.py"
    if workflow_script.exists():
        os.system(f"python {workflow_script}")
    else:
        print("❌ Workflow script not found")

def setup_environment():
    """Set up Phase 1 environment"""
    print("🔧 Setting up Phase 1 environment...")
    
    setup_script = Path(__file__).parent / "scripts" / "setup_phase1.py"
    if setup_script.exists():
        os.system(f"python {setup_script}")
    else:
        print("❌ Setup script not found")

def show_status():
    """Show Phase 1 status"""
    print("📊 Phase 1 Status")
    print("=" * 40)
    
    integration_dir = Path(__file__).parent
    assets_dir = integration_dir / "assets"
    
    # Check directories
    directories = [
        ("Source", integration_dir / "src"),
        ("Tests", integration_dir / "tests"),
        ("Scripts", integration_dir / "scripts"),
        ("Docs", integration_dir / "docs"),
        ("Assets", assets_dir),
        ("Config", integration_dir / "config"),
        ("Logs", integration_dir / "logs")
    ]
    
    for name, path in directories:
        if path.exists():
            if path.is_dir():
                file_count = len(list(path.rglob("*")))
                print(f"  ✅ {name}: {file_count} items")
            else:
                print(f"  ✅ {name}: exists")
        else:
            print(f"  ❌ {name}: missing")
    
    # Check asset counts
    if assets_dir.exists():
        print(f"\n📦 Asset Summary:")
        for platform in ["opengameart", "free3d", "imported", "exports"]:
            platform_dir = assets_dir / platform
            if platform_dir.exists():
                count = len(list(platform_dir.glob("*")))
                print(f"  {platform}: {count} assets")
            else:
                print(f"  {platform}: 0 assets")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Phase 1: Free & Simple Asset Integration")
    parser.add_argument("command", choices=["test", "workflow", "setup", "status"], 
                       help="Command to run")
    
    args = parser.parse_args()
    
    print("🎯 Phase 1: Free & Simple Asset Integration")
    print("=" * 50)
    
    if args.command == "test":
        run_tests()
    elif args.command == "workflow":
        run_workflow()
    elif args.command == "setup":
        setup_environment()
    elif args.command == "status":
        show_status()
    else:
        print(f"❌ Unknown command: {args.command}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

