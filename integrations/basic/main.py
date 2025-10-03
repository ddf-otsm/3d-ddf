#!/usr/bin/env python3
"""
Basic Integration Main Entry Point
Free platforms that work without authentication
"""

import sys
import os
from pathlib import Path

# Add src directory to path
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

from basic_asset_scraper import BasicAssetScraper

def main():
    """Main entry point for basic integration"""
    if len(sys.argv) < 2:
        print("🌐 Basic Integration - Free Platforms (No Authentication Required)")
        print("=" * 70)
        print("Usage: python main.py <command> [options]")
        print("\nCommands:")
        print("  search     - Search for assets across all free platforms")
        print("  download   - Download assets from search results")
        print("  platforms  - Show available platforms")
        print("  demo       - Run complete demo")
        print("\nExamples:")
        print("  python main.py search character")
        print("  python main.py download")
        print("  python main.py platforms")
        print("  python main.py demo")
        return
    
    command = sys.argv[1].lower()
    
    if command == "search":
        search_term = sys.argv[2] if len(sys.argv) > 2 else "character"
        run_search(search_term)
    elif command == "download":
        run_download()
    elif command == "platforms":
        show_platforms()
    elif command == "demo":
        run_demo()
    else:
        print(f"Unknown command: {command}")
        print("Use 'python main.py' to see available commands")

def run_search(query: str):
    """Search for assets across all free platforms"""
    print(f"🔍 Searching for: {query}")
    print("=" * 40)
    
    scraper = BasicAssetScraper()
    results = scraper.search_all_platforms(query, limit_per_platform=3)
    
    total_assets = 0
    for platform, assets in results.items():
        platform_info = scraper.get_platform_info(platform)
        print(f"\n📦 {platform_info['name']}: {len(assets)} assets")
        
        for i, asset in enumerate(assets, 1):
            print(f"  {i}. {asset['title']}")
            print(f"     Format: {asset['format']}")
            print(f"     License: {asset['license']}")
            print(f"     Size: {asset.get('file_size', 'Unknown')}")
            print(f"     Rating: {asset.get('rating', 'Unknown')}")
        
        total_assets += len(assets)
    
    print(f"\n📊 Total assets found: {total_assets}")
    
    # Save results for download
    results_file = Path(__file__).parent / "assets" / "search_results.json"
    results_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(results_file, 'w') as f:
        import json
        json.dump(results, f, indent=2)
    
    print(f"💾 Search results saved to: {results_file}")

def run_download():
    """Download assets from previous search results"""
    print("⬇️ Downloading assets...")
    print("=" * 30)
    
    scraper = BasicAssetScraper()
    results_file = Path(__file__).parent / "assets" / "search_results.json"
    
    if not results_file.exists():
        print("❌ No search results found. Run 'python main.py search <query>' first.")
        return
    
    # Load search results
    with open(results_file, 'r') as f:
        import json
        results = json.load(f)
    
    # Download assets
    download_dir = Path(__file__).parent / "assets" / "downloads"
    download_results = scraper.download_all_assets(results, str(download_dir))
    
    total_downloaded = 0
    for platform, files in download_results.items():
        print(f"  {platform}: {len(files)} files downloaded")
        total_downloaded += len(files)
    
    print(f"\n✅ Downloaded {total_downloaded} assets total!")
    print(f"📁 Files saved to: {download_dir}")

def show_platforms():
    """Show available platforms"""
    print("🌐 Available Free Platforms")
    print("=" * 35)
    
    scraper = BasicAssetScraper()
    platforms = scraper.get_supported_platforms()
    
    for platform in platforms:
        auth_status = "🔐 Auth Required" if platform["requires_auth"] else "🆓 No Auth"
        print(f"  {platform['name']}: {auth_status}")
        print(f"    URL: {platform['base_url']}")
        print(f"    Rate Limit: {platform['rate_limit']}s")
        print()

def run_demo():
    """Run complete demo"""
    print("🚀 Basic Integration Demo")
    print("=" * 30)
    
    # Show platforms
    print("\n1️⃣ Available Platforms:")
    show_platforms()
    
    # Search for assets
    print("\n2️⃣ Searching for assets...")
    run_search("character")
    
    # Download assets
    print("\n3️⃣ Downloading assets...")
    run_download()
    
    print("\n✅ Demo completed!")
    print("\n💡 Next steps:")
    print("- Try different search terms: python main.py search weapon")
    print("- Download assets: python main.py download")
    print("- Explore other phases: cd ../phase1 && python main.py setup")

if __name__ == "__main__":
    main()
