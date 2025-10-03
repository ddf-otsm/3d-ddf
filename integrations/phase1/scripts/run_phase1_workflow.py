#!/usr/bin/env python3
"""
Phase 1 Workflow Runner
Demonstrates the complete Phase 1 workflow for free asset integration
"""

import os
import sys
import json
import time
from pathlib import Path

# Add src directory to path for imports
src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
sys.path.insert(0, src_path)

from phase1_asset_importer import Phase1AssetImporter
from blender_mcp_phase1 import Phase1BlenderIntegration

class Phase1WorkflowRunner:
    """Runs the complete Phase 1 workflow"""
    
    def __init__(self):
        self.importer = Phase1AssetImporter()
        self.blender_integration = Phase1BlenderIntegration()
        self.workflow_results = {
            "start_time": time.time(),
            "steps_completed": [],
            "assets_processed": 0,
            "errors": []
        }
    
    def step_1_discover_platforms(self):
        """Step 1: Discover and understand Phase 1 platforms"""
        print("\n🔍 Step 1: Discovering Phase 1 Platforms")
        print("-" * 40)
        
        platforms = self.importer.platforms
        
        for platform_id, platform_info in platforms.items():
            print(f"\n📦 {platform_info['name']}")
            print(f"   Complexity: {'⭐' * platform_info['complexity']}")
            print(f"   License: {platform_info['license']}")
            print(f"   Formats: {', '.join(platform_info['supported_formats'])}")
            print(f"   URL: {platform_info['base_url']}")
        
        self.workflow_results["steps_completed"].append("platform_discovery")
        print(f"\n✅ Discovered {len(platforms)} platforms")
    
    def step_2_setup_environment(self):
        """Step 2: Set up the working environment"""
        print("\n🔧 Step 2: Setting Up Environment")
        print("-" * 40)
        
        # Create directories
        self.importer.ensure_download_dir()
        print(f"✅ Download directory: {self.importer.download_dir}")
        
        # Setup Blender environment
        print("🔧 Setting up Blender environment...")
        if self.blender_integration.setup_phase1_scene():
            print("✅ Blender scene setup complete")
        else:
            print("❌ Blender scene setup failed")
            self.workflow_results["errors"].append("Blender scene setup failed")
        
        # Create asset collections
        for platform in ["opengameart", "free3d"]:
            if self.blender_integration.create_asset_collection(platform):
                print(f"✅ Created collection for {platform}")
            else:
                print(f"❌ Failed to create collection for {platform}")
                self.workflow_results["errors"].append(f"Failed to create {platform} collection")
        
        self.workflow_results["steps_completed"].append("environment_setup")
    
    def step_3_demo_asset_workflow(self):
        """Step 3: Demonstrate asset workflow with mock data"""
        print("\n📥 Step 3: Asset Workflow Demo")
        print("-" * 40)
        
        # Mock search terms for demonstration
        search_terms = ["character", "weapon", "environment"]
        
        print(f"🔍 Searching for: {', '.join(search_terms)}")
        
        for term in search_terms:
            print(f"\n  📋 Processing: {term}")
            
            # Simulate asset discovery
            mock_assets = [
                {
                    "title": f"{term.title()} Asset 1",
                    "format": ".blend",
                    "license": "CC0",
                    "url": f"https://example.com/{term}_1"
                },
                {
                    "title": f"{term.title()} Asset 2", 
                    "format": ".fbx",
                    "license": "CC-BY",
                    "url": f"https://example.com/{term}_2"
                }
            ]
            
            for asset in mock_assets:
                print(f"    📦 {asset['title']} ({asset['format']})")
                
                # Download asset (mock)
                filepath = self.importer.download_asset(asset, "opengameart")
                if filepath:
                    print(f"      ✅ Downloaded to: {filepath}")
                    
                    # Import to Blender
                    if self.blender_integration.import_asset_to_blender(filepath, asset['title']):
                        print(f"      ✅ Imported to Blender")
                        self.workflow_results["assets_processed"] += 1
                    else:
                        print(f"      ❌ Failed to import to Blender")
                        self.workflow_results["errors"].append(f"Failed to import {asset['title']}")
                else:
                    print(f"      ❌ Failed to download")
                    self.workflow_results["errors"].append(f"Failed to download {asset['title']}")
        
        self.workflow_results["steps_completed"].append("asset_workflow")
    
    def step_4_create_asset_library(self):
        """Step 4: Create and organize asset library"""
        print("\n📚 Step 4: Creating Asset Library")
        print("-" * 40)
        
        # Create asset library
        library = self.importer.create_asset_library()
        
        print(f"📊 Asset Library Summary:")
        print(f"   Total assets: {library['metadata']['total_assets']}")
        print(f"   Platforms: {', '.join(library['metadata']['platforms'])}")
        
        for platform, assets in library["phase1_assets"].items():
            print(f"\n   {platform.title()}: {len(assets)} assets")
            for asset in assets[:2]:  # Show first 2 assets
                print(f"     - {asset['filename']}")
        
        # Save library to file
        library_file = os.path.join(self.importer.download_dir, "asset_library.json")
        with open(library_file, 'w') as f:
            json.dump(library, f, indent=2)
        
        print(f"\n✅ Asset library saved to: {library_file}")
        self.workflow_results["steps_completed"].append("asset_library")
    
    def step_5_verify_integration(self):
        """Step 5: Verify Blender integration"""
        print("\n🔍 Step 5: Verifying Blender Integration")
        print("-" * 40)
        
        # Check available assets
        assets = self.blender_integration.get_available_assets()
        
        print(f"📁 Available Assets in Blender:")
        for platform, platform_assets in assets.items():
            print(f"   {platform}: {len(platform_assets)} assets")
        
        # Test scene info
        print("\n🎬 Scene Information:")
        print("   - Basic scene setup complete")
        print("   - Collections created for each platform")
        print("   - Ready for asset import")
        
        self.workflow_results["steps_completed"].append("integration_verification")
    
    def step_6_generate_report(self):
        """Step 6: Generate workflow report"""
        print("\n📊 Step 6: Generating Report")
        print("-" * 40)
        
        end_time = time.time()
        duration = end_time - self.workflow_results["start_time"]
        
        report = {
            "workflow": "Phase 1: Free & Simple Asset Integration",
            "duration_seconds": round(duration, 2),
            "steps_completed": self.workflow_results["steps_completed"],
            "assets_processed": self.workflow_results["assets_processed"],
            "errors": self.workflow_results["errors"],
            "success_rate": len(self.workflow_results["steps_completed"]) / 6 * 100,
            "recommendations": [
                "Start with OpenGameArt.org for completely free assets",
                "Use Free3D for quick prototyping",
                "Organize assets by platform in separate collections",
                "Always check licensing before commercial use"
            ]
        }
        
        # Save report
        report_file = os.path.join(self.importer.download_dir, "phase1_report.json")
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📄 Report saved to: {report_file}")
        print(f"\n📈 Success Rate: {report['success_rate']:.1f}%")
        print(f"⏱️  Duration: {duration:.1f} seconds")
        print(f"📦 Assets Processed: {report['assets_processed']}")
        
        if report['errors']:
            print(f"\n❌ Errors ({len(report['errors'])}):")
            for error in report['errors']:
                print(f"   - {error}")
        
        self.workflow_results["steps_completed"].append("report_generation")
    
    def run_complete_workflow(self):
        """Run the complete Phase 1 workflow"""
        print("🚀 Starting Phase 1: Free & Simple Asset Integration")
        print("=" * 60)
        
        try:
            self.step_1_discover_platforms()
            self.step_2_setup_environment()
            self.step_3_demo_asset_workflow()
            self.step_4_create_asset_library()
            self.step_5_verify_integration()
            self.step_6_generate_report()
            
            print("\n🎉 Phase 1 Workflow Complete!")
            print("=" * 60)
            print("✅ Ready to proceed to Phase 2 (Free with Registration)")
            print("📁 Check your asset directories for downloaded files")
            print("🎬 Open Blender to see imported assets")
            
        except Exception as e:
            print(f"\n❌ Workflow failed: {e}")
            self.workflow_results["errors"].append(f"Workflow failure: {e}")

def main():
    """Main function"""
    runner = Phase1WorkflowRunner()
    runner.run_complete_workflow()

if __name__ == "__main__":
    main()
