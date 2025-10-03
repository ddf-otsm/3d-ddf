#!/usr/bin/env python3
"""
Phase 2 Main Entry Point
Provides a unified interface for Phase 2 asset integration
"""

import os
import sys
import argparse
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def run_tests():
    """Run Phase 2 tests"""
    print("🧪 Running Phase 2 tests...")
    
    test_script = Path(__file__).parent / "tests" / "test_phase2_simple.py"
    if test_script.exists():
        os.system(f"python {test_script}")
    else:
        print("❌ Test script not found")

def run_workflow():
    """Run Phase 2 workflow"""
    print("🚀 Running Phase 2 workflow...")
    
    workflow_script = Path(__file__).parent / "scripts" / "run_phase2_workflow.py"
    if workflow_script.exists():
        os.system(f"python {workflow_script}")
    else:
        print("❌ Workflow script not found")

def setup_environment():
    """Set up Phase 2 environment"""
    print("🔧 Setting up Phase 2 environment...")
    
    # Create directories
    integration_dir = Path(__file__).parent
    assets_dir = integration_dir / "assets"
    
    directories = [
        assets_dir,
        assets_dir / "sketchfab",
        assets_dir / "clara",
        assets_dir / "imported",
        assets_dir / "exports",
        integration_dir / "logs"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"  ✅ {directory}")
    
    print("✅ Phase 2 environment setup complete")

def show_status():
    """Show Phase 2 status"""
    print("📊 Phase 2 Status")
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
        for platform in ["sketchfab", "clara", "imported", "exports"]:
            platform_dir = assets_dir / platform
            if platform_dir.exists():
                count = len(list(platform_dir.glob("*")))
                print(f"  {platform}: {count} assets")
            else:
                print(f"  {platform}: 0 assets")
    
    # Check authentication status
    print(f"\n🔐 Authentication Status:")
    sketchfab_key = os.getenv("SKETCHFAB_API_KEY")
    clara_token = os.getenv("CLARA_IO_TOKEN")
    
    print(f"  Sketchfab: {'✅ Authenticated' if sketchfab_key else '❌ Not authenticated'}")
    print(f"  Clara.io: {'✅ Authenticated' if clara_token else '❌ Not authenticated'}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Phase 2: Free with Registration Asset Integration")
    parser.add_argument("command", choices=["test", "workflow", "setup", "status"], 
                       help="Command to run")
    
    args = parser.parse_args()
    
    print("🎯 Phase 2: Free with Registration Asset Integration")
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
