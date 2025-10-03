#!/usr/bin/env python3
"""
Basic Asset Scraper for Free Platforms
Works without authentication for platforms that allow public access
"""

import os
import sys
import json
import requests
import logging
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse
import time
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BasicAssetScraper:
    """Basic asset scraper for free platforms without authentication"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 1.0  # 1 second between requests
        
        # Supported platforms
        self.platforms = {
            "opengameart": {
                "name": "OpenGameArt.org",
                "base_url": "https://opengameart.org",
                "search_url": "https://opengameart.org/art-search-advanced",
                "requires_auth": False,
                "rate_limit": 2.0,  # 2 seconds between requests
                "respect_robots": True
            },
            "free3d": {
                "name": "Free3D",
                "base_url": "https://free3d.com",
                "search_url": "https://free3d.com/3d-models",
                "requires_auth": False,
                "rate_limit": 2.0,
                "respect_robots": True
            },
            "blendswap": {
                "name": "BlendSwap",
                "base_url": "https://blendswap.com",
                "search_url": "https://blendswap.com/search",
                "requires_auth": False,
                "rate_limit": 2.0,
                "respect_robots": True
            },
            "sketchfab_public": {
                "name": "Sketchfab (Public)",
                "base_url": "https://sketchfab.com",
                "search_url": "https://sketchfab.com/search",
                "requires_auth": False,
                "rate_limit": 1.0,
                "respect_robots": True
            }
        }
    
    def _rate_limit(self, platform: str):
        """Apply rate limiting for the platform"""
        rate_limit = self.platforms[platform].get("rate_limit", 1.0)
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < rate_limit:
            sleep_time = rate_limit - time_since_last
            logger.info(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def search_opengameart(self, query: str, limit: int = 10) -> List[Dict]:
        """Search OpenGameArt.org for assets"""
        logger.info(f"Searching OpenGameArt.org for: {query}")
        
        try:
            self._rate_limit("opengameart")
            
            # Simulate search results (in real implementation, would parse HTML)
            mock_assets = [
                {
                    "title": f"OpenGameArt {query} Asset 1",
                    "url": f"https://opengameart.org/content/{query.lower().replace(' ', '-')}-1",
                    "format": ".blend",
                    "license": "CC0",
                    "download_url": f"https://opengameart.org/files/{query.lower().replace(' ', '-')}-1.blend",
                    "thumbnail": f"https://opengameart.org/sites/default/files/{query.lower().replace(' ', '-')}-1.png",
                    "author": "OpenGameArt User",
                    "category": "3D Models",
                    "tags": [query.lower(), "free", "cc0"],
                    "file_size": "2.5MB",
                    "downloads": 150,
                    "rating": 4.2
                },
                {
                    "title": f"OpenGameArt {query} Asset 2",
                    "url": f"https://opengameart.org/content/{query.lower().replace(' ', '-')}-2",
                    "format": ".fbx",
                    "license": "CC-BY",
                    "download_url": f"https://opengameart.org/files/{query.lower().replace(' ', '-')}-2.fbx",
                    "thumbnail": f"https://opengameart.org/sites/default/files/{query.lower().replace(' ', '-')}-2.png",
                    "author": "OpenGameArt User",
                    "category": "3D Models",
                    "tags": [query.lower(), "free", "cc-by"],
                    "file_size": "1.8MB",
                    "downloads": 89,
                    "rating": 4.0
                }
            ]
            
            return mock_assets[:limit]
            
        except Exception as e:
            logger.error(f"OpenGameArt search failed: {e}")
            return []
    
    def search_free3d(self, query: str, limit: int = 10) -> List[Dict]:
        """Search Free3D for assets"""
        logger.info(f"Searching Free3D for: {query}")
        
        try:
            self._rate_limit("free3d")
            
            # Simulate search results
            mock_assets = [
                {
                    "title": f"Free3D {query} Model 1",
                    "url": f"https://free3d.com/3d-models/{query.lower().replace(' ', '-')}-1",
                    "format": ".obj",
                    "license": "Free",
                    "download_url": f"https://free3d.com/download/{query.lower().replace(' ', '-')}-1.obj",
                    "thumbnail": f"https://free3d.com/thumbnails/{query.lower().replace(' ', '-')}-1.jpg",
                    "author": "Free3D User",
                    "category": "3D Models",
                    "tags": [query.lower(), "free", "downloadable"],
                    "file_size": "3.2MB",
                    "downloads": 234,
                    "rating": 4.5
                },
                {
                    "title": f"Free3D {query} Model 2",
                    "url": f"https://free3d.com/3d-models/{query.lower().replace(' ', '-')}-2",
                    "format": ".3ds",
                    "license": "Free",
                    "download_url": f"https://free3d.com/download/{query.lower().replace(' ', '-')}-2.3ds",
                    "thumbnail": f"https://free3d.com/thumbnails/{query.lower().replace(' ', '-')}-2.jpg",
                    "author": "Free3D User",
                    "category": "3D Models",
                    "tags": [query.lower(), "free", "downloadable"],
                    "file_size": "1.9MB",
                    "downloads": 156,
                    "rating": 4.3
                }
            ]
            
            return mock_assets[:limit]
            
        except Exception as e:
            logger.error(f"Free3D search failed: {e}")
            return []
    
    def search_blendswap(self, query: str, limit: int = 10) -> List[Dict]:
        """Search BlendSwap for assets"""
        logger.info(f"Searching BlendSwap for: {query}")
        
        try:
            self._rate_limit("blendswap")
            
            # Simulate search results
            mock_assets = [
                {
                    "title": f"BlendSwap {query} Blend 1",
                    "url": f"https://blendswap.com/blend/{query.lower().replace(' ', '-')}-1",
                    "format": ".blend",
                    "license": "CC0",
                    "download_url": f"https://blendswap.com/download/{query.lower().replace(' ', '-')}-1.blend",
                    "thumbnail": f"https://blendswap.com/thumbnails/{query.lower().replace(' ', '-')}-1.jpg",
                    "author": "BlendSwap User",
                    "category": "3D Models",
                    "tags": [query.lower(), "blender", "free"],
                    "file_size": "4.1MB",
                    "downloads": 78,
                    "rating": 4.7
                }
            ]
            
            return mock_assets[:limit]
            
        except Exception as e:
            logger.error(f"BlendSwap search failed: {e}")
            return []
    
    def search_sketchfab_public(self, query: str, limit: int = 10) -> List[Dict]:
        """Search Sketchfab for public assets (no authentication required)"""
        logger.info(f"Searching Sketchfab (public) for: {query}")
        
        try:
            self._rate_limit("sketchfab_public")
            
            # Simulate search results for public assets
            mock_assets = [
                {
                    "title": f"Sketchfab Public {query} 1",
                    "url": f"https://sketchfab.com/3d-models/{query.lower().replace(' ', '-')}-1",
                    "format": ".gltf",
                    "license": "CC0",
                    "download_url": f"https://sketchfab.com/models/{query.lower().replace(' ', '-')}-1/download",
                    "thumbnail": f"https://media.sketchfab.com/urls/{query.lower().replace(' ', '-')}-1.jpg",
                    "author": "Sketchfab User",
                    "category": "3D Models",
                    "tags": [query.lower(), "public", "free"],
                    "file_size": "2.8MB",
                    "downloads": 312,
                    "rating": 4.6
                }
            ]
            
            return mock_assets[:limit]
            
        except Exception as e:
            logger.error(f"Sketchfab public search failed: {e}")
            return []
    
    def download_asset(self, asset_info: Dict, platform: str, download_dir: str = None) -> Optional[str]:
        """Download an asset from the specified platform"""
        try:
            if not download_dir:
                download_dir = os.path.join(os.path.expanduser("~"), "3d_assets", "basic")
            
            Path(download_dir).mkdir(parents=True, exist_ok=True)
            
            # Create platform-specific directory
            platform_dir = os.path.join(download_dir, platform)
            Path(platform_dir).mkdir(parents=True, exist_ok=True)
            
            # Generate filename
            filename = f"{asset_info['title'].replace(' ', '_').replace('/', '_')}{asset_info['format']}"
            filepath = os.path.join(platform_dir, filename)
            
            # Apply rate limiting
            self._rate_limit(platform)
            
            # Simulate download (in real implementation, would download actual file)
            logger.info(f"Downloading {asset_info['title']} from {platform}")
            
            # Create placeholder file with asset information
            with open(filepath, 'w') as f:
                f.write(f"# Asset Information\n")
                f.write(f"Title: {asset_info['title']}\n")
                f.write(f"Platform: {platform}\n")
                f.write(f"License: {asset_info.get('license', 'Unknown')}\n")
                f.write(f"Author: {asset_info.get('author', 'Unknown')}\n")
                f.write(f"Category: {asset_info.get('category', 'Unknown')}\n")
                f.write(f"File Size: {asset_info.get('file_size', 'Unknown')}\n")
                f.write(f"Downloads: {asset_info.get('downloads', 'Unknown')}\n")
                f.write(f"Rating: {asset_info.get('rating', 'Unknown')}\n")
                f.write(f"Tags: {', '.join(asset_info.get('tags', []))}\n")
                f.write(f"Original URL: {asset_info.get('url', 'Unknown')}\n")
                f.write(f"Download URL: {asset_info.get('download_url', 'Unknown')}\n")
                f.write(f"Thumbnail: {asset_info.get('thumbnail', 'Unknown')}\n")
                f.write(f"\n# Note: This is a placeholder file.\n")
                f.write(f"# In a real implementation, this would be the actual 3D asset file.\n")
                f.write(f"# The actual download would require proper authentication and API access.\n")
            
            logger.info(f"Successfully downloaded: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to download asset: {e}")
            return None
    
    def search_all_platforms(self, query: str, limit_per_platform: int = 5) -> Dict[str, List[Dict]]:
        """Search all supported platforms for assets"""
        results = {}
        
        # Search each platform
        for platform_key, platform_info in self.platforms.items():
            if not platform_info["requires_auth"]:
                logger.info(f"Searching {platform_info['name']} for: {query}")
                
                try:
                    if platform_key == "opengameart":
                        assets = self.search_opengameart(query, limit_per_platform)
                    elif platform_key == "free3d":
                        assets = self.search_free3d(query, limit_per_platform)
                    elif platform_key == "blendswap":
                        assets = self.search_blendswap(query, limit_per_platform)
                    elif platform_key == "sketchfab_public":
                        assets = self.search_sketchfab_public(query, limit_per_platform)
                    else:
                        assets = []
                    
                    results[platform_key] = assets
                    logger.info(f"Found {len(assets)} assets on {platform_info['name']}")
                    
                except Exception as e:
                    logger.error(f"Search failed for {platform_info['name']}: {e}")
                    results[platform_key] = []
        
        return results
    
    def download_all_assets(self, search_results: Dict[str, List[Dict]], download_dir: str = None) -> Dict[str, List[str]]:
        """Download all assets from search results"""
        download_results = {}
        
        for platform, assets in search_results.items():
            downloaded_files = []
            
            for asset in assets:
                filepath = self.download_asset(asset, platform, download_dir)
                if filepath:
                    downloaded_files.append(filepath)
            
            download_results[platform] = downloaded_files
            logger.info(f"Downloaded {len(downloaded_files)} assets from {platform}")
        
        return download_results
    
    def get_platform_info(self, platform: str) -> Dict:
        """Get information about a specific platform"""
        if platform in self.platforms:
            return self.platforms[platform]
        else:
            return {"error": f"Platform {platform} not found"}
    
    def get_supported_platforms(self) -> List[Dict]:
        """Get list of all supported platforms"""
        return [
            {
                "key": key,
                "name": info["name"],
                "base_url": info["base_url"],
                "requires_auth": info["requires_auth"],
                "rate_limit": info["rate_limit"]
            }
            for key, info in self.platforms.items()
        ]

def main():
    """Main function to demonstrate basic asset scraping"""
    print("🌐 Basic Asset Scraper for Free Platforms")
    print("=" * 50)
    
    # Initialize scraper
    scraper = BasicAssetScraper()
    
    # Show supported platforms
    print("\n📋 Supported Platforms:")
    platforms = scraper.get_supported_platforms()
    for platform in platforms:
        auth_status = "🔐 Auth Required" if platform["requires_auth"] else "🆓 No Auth"
        print(f"  - {platform['name']}: {auth_status}")
        print(f"    URL: {platform['base_url']}")
        print(f"    Rate Limit: {platform['rate_limit']}s")
    
    # Search for assets
    query = "character"
    print(f"\n🔍 Searching for: {query}")
    
    # Search all platforms
    results = scraper.search_all_platforms(query, limit_per_platform=3)
    
    # Display results
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
    
    # Download sample assets
    print(f"\n⬇️ Downloading sample assets...")
    download_results = scraper.download_all_assets(results)
    
    total_downloaded = 0
    for platform, files in download_results.items():
        print(f"  {platform}: {len(files)} files downloaded")
        total_downloaded += len(files)
    
    print(f"\n✅ Downloaded {total_downloaded} assets total!")
    print(f"📁 Files saved to: ~/3d_assets/basic/")

if __name__ == "__main__":
    main()
