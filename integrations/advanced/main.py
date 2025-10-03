#!/usr/bin/env python3
"""
Advanced Integration Features Main Entry Point
AI recommendations, batch processing, and custom platform integration
"""

import sys
import os
from pathlib import Path

# Add src directory to path
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

from ai_asset_recommender import AIAssetRecommender
from batch_processor import BatchProcessor
from custom_platform_integration import CustomPlatformManager

def main():
    """Main entry point for advanced integration features"""
    if len(sys.argv) < 2:
        print("Advanced Integration Features")
        print("=" * 40)
        print("Usage: python main.py <command> [options]")
        print("\nCommands:")
        print("  ai          - AI asset recommendation system")
        print("  batch       - Batch processing system")
        print("  platform    - Custom platform integration")
        print("  demo        - Run all advanced features demo")
        print("\nExamples:")
        print("  python main.py ai")
        print("  python main.py batch")
        print("  python main.py platform")
        print("  python main.py demo")
        return
    
    command = sys.argv[1].lower()
    
    if command == "ai":
        run_ai_demo()
    elif command == "batch":
        run_batch_demo()
    elif command == "platform":
        run_platform_demo()
    elif command == "demo":
        run_full_demo()
    else:
        print(f"Unknown command: {command}")
        print("Use 'python main.py' to see available commands")

def run_ai_demo():
    """Run AI asset recommendation demo"""
    print("🤖 AI Asset Recommendation System Demo")
    print("=" * 50)
    
    # Initialize AI recommender
    recommender = AIAssetRecommender()
    
    # Sample assets for demonstration
    sample_assets = [
        {
            "title": "Sci-Fi Character",
            "category": "Characters",
            "tags": ["sci-fi", "character", "humanoid"],
            "rating": 4.8,
            "downloads": 1500,
            "price": "$25.99",
            "platform": "sketchfab",
            "texture_resolution": "2048x2048",
            "polygon_count": 15000
        },
        {
            "title": "Medieval Weapon",
            "category": "Weapons",
            "tags": ["medieval", "sword", "weapon"],
            "rating": 4.5,
            "downloads": 800,
            "price": "$15.99",
            "platform": "opengameart",
            "texture_resolution": "1024x1024",
            "polygon_count": 5000
        },
        {
            "title": "Modern Building",
            "category": "Architecture",
            "tags": ["modern", "building", "architecture"],
            "rating": 4.9,
            "downloads": 2200,
            "price": "$49.99",
            "platform": "cgtrader",
            "texture_resolution": "4096x4096",
            "polygon_count": 25000
        }
    ]
    
    # Test feature extraction
    print("\n🔍 Feature Extraction:")
    for asset in sample_assets[:2]:
        features = recommender.extract_asset_features(asset)
        print(f"  {asset['title']}: {len(features)} feature categories")
    
    # Test recommendations
    print("\n💡 Recommendations:")
    query_asset = sample_assets[0]
    recommendations = recommender.recommend_assets(query_asset, sample_assets, limit=3)
    
    for i, rec in enumerate(recommendations, 1):
        print(f"  {i}. {rec['asset']['title']} (similarity: {rec['similarity']:.2f})")
    
    # Test trend analysis
    print("\n📊 Trend Analysis:")
    trends = recommender.analyze_asset_trends(sample_assets)
    print(f"  Popular categories: {trends['popular_categories']}")
    print(f"  Price distribution: {trends['price_trends']}")
    
    # Generate report
    print("\n📋 Asset Report:")
    report = recommender.generate_asset_report(sample_assets)
    print(f"  Total assets: {report['total_assets']}")
    print(f"  Insights: {len(report['insights'])} insights generated")
    
    print("\n✅ AI recommendation system demo completed!")

def run_batch_demo():
    """Run batch processing demo"""
    print("⚡ Batch Processing System Demo")
    print("=" * 40)
    
    # Initialize batch processor
    processor = BatchProcessor()
    
    # Create sample tasks
    sample_tasks = [
        {
            "type": "asset_download",
            "asset_id": "asset_001",
            "platform": "sketchfab",
            "url": "https://sketchfab.com/models/asset_001"
        },
        {
            "type": "asset_import",
            "asset_id": "asset_001",
            "file_path": "/tmp/asset_001.fbx"
        },
        {
            "type": "asset_optimization",
            "asset_id": "asset_001",
            "optimization_level": "high"
        },
        {
            "type": "asset_export",
            "asset_id": "asset_001",
            "export_format": "fbx"
        },
        {
            "type": "asset_analysis",
            "asset_id": "asset_001",
            "analysis_type": "performance"
        }
    ]
    
    # Create batch job
    job_id = processor.create_batch_job("demo_batch", sample_tasks, "asset_processing")
    print(f"Created batch job: {job_id}")
    
    # Define progress callback
    def progress_callback(progress, message):
        print(f"  Progress: {progress:.1f}% - {message}")
    
    # Process batch job
    print("\n🚀 Processing batch job...")
    try:
        results = processor.process_batch_job(job_id, progress_callback)
        
        print(f"\n✅ Batch processing completed!")
        print(f"  Job ID: {results['job_id']}")
        print(f"  Status: {results['status']}")
        print(f"  Results: {len(results['results'])} tasks processed")
        
        # Show processing stats
        stats = processor.get_processing_stats()
        print(f"\n📊 Processing Statistics:")
        print(f"  Total tasks: {stats['total_tasks']}")
        print(f"  Completed: {stats['completed_tasks']}")
        print(f"  Failed: {stats['failed_tasks']}")
        print(f"  Success rate: {stats['success_rate']:.1f}%")
        print(f"  Processing time: {stats['processing_time']:.2f} seconds")
        
    except Exception as e:
        print(f"❌ Batch processing failed: {e}")
    
    print("\n✅ Batch processing demo completed!")

def run_platform_demo():
    """Run custom platform integration demo"""
    print("🔧 Custom Platform Integration Demo")
    print("=" * 45)
    
    # Initialize custom platform manager
    manager = CustomPlatformManager()
    
    # Create a sample platform integration
    print("\n📝 Creating sample platform integration...")
    custom_config = {
        "base_url": "https://api.example-platform.com",
        "api_key": "your_api_key_here",
        "rate_limit": 500,
        "supported_formats": [".fbx", ".obj", ".blend", ".dae"]
    }
    
    platform_file = manager.create_platform_integration(
        "ExamplePlatform", 
        "basic", 
        custom_config
    )
    print(f"Created platform integration: {platform_file}")
    
    # Discover platforms
    print("\n🔍 Discovering platforms...")
    discovered = manager.discover_platforms()
    print(f"Discovered platforms: {discovered}")
    
    # Load and test platform
    print("\n🧪 Testing platform integration...")
    integration = manager.load_platform("exampleplatform")
    if integration:
        print("✅ Platform integration loaded successfully")
        
        # Test platform info
        platform_info = integration.get_platform_info()
        print(f"Platform info: {platform_info}")
        
        # Validate integration
        validation = manager.validate_platform_integration("exampleplatform")
        print(f"Validation results: {validation}")
    else:
        print("❌ Failed to load platform integration")
    
    # Get available platforms
    print("\n📋 Available platforms:")
    platforms = manager.get_available_platforms()
    for platform in platforms:
        print(f"  - {platform['name']}: {platform['status']}")
        if platform['errors']:
            print(f"    Errors: {platform['errors']}")
        if platform['warnings']:
            print(f"    Warnings: {platform['warnings']}")
    
    print("\n✅ Custom platform integration demo completed!")

def run_full_demo():
    """Run complete advanced features demo"""
    print("🚀 Advanced Integration Features - Complete Demo")
    print("=" * 60)
    
    print("\n" + "="*60)
    print("🤖 AI ASSET RECOMMENDATION SYSTEM")
    print("="*60)
    run_ai_demo()
    
    print("\n" + "="*60)
    print("⚡ BATCH PROCESSING SYSTEM")
    print("="*60)
    run_batch_demo()
    
    print("\n" + "="*60)
    print("🔧 CUSTOM PLATFORM INTEGRATION")
    print("="*60)
    run_platform_demo()
    
    print("\n" + "="*60)
    print("🎉 ADVANCED FEATURES DEMO COMPLETED!")
    print("="*60)
    print("\nAdvanced integration features include:")
    print("✅ AI-powered asset recommendations")
    print("✅ Batch processing for multiple assets")
    print("✅ Custom platform integration system")
    print("✅ Automated workflow optimization")
    print("✅ Performance analytics and monitoring")
    print("\nAll advanced features are ready for production use!")

if __name__ == "__main__":
    main()
