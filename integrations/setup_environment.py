#!/usr/bin/env python3
"""
Environment Setup Script for 3D Asset Integration System
Helps users configure API keys and credentials for different platforms
"""

import os
import sys
import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional

def create_env_file():
    """Create .env file from template"""
    template_path = Path(__file__).parent / "env.template"
    env_path = Path(__file__).parent / ".env"
    
    if template_path.exists():
        if env_path.exists():
            print("⚠️  .env file already exists. Backing up to .env.backup")
            shutil.copy(env_path, env_path.with_suffix('.backup'))
        
        shutil.copy(template_path, env_path)
        print(f"✅ Created .env file from template: {env_path}")
        return True
    else:
        print("❌ Template file not found: env.template")
        return False

def setup_basic_integration():
    """Set up basic integration that works without authentication"""
    print("\n🌐 Setting up Basic Integration (No Authentication Required)")
    print("=" * 60)
    
    basic_platforms = [
        {
            "name": "OpenGameArt.org",
            "description": "Free 3D assets with CC0, CC-BY licenses",
            "url": "https://opengameart.org",
            "requires_auth": False,
            "rate_limit": "2 seconds between requests",
            "usage": "Direct web scraping (respects robots.txt)"
        },
        {
            "name": "Free3D",
            "description": "Free 3D models and assets",
            "url": "https://free3d.com",
            "requires_auth": False,
            "rate_limit": "2 seconds between requests",
            "usage": "Direct web scraping (respects robots.txt)"
        },
        {
            "name": "BlendSwap",
            "description": "Free Blender files and assets",
            "url": "https://blendswap.com",
            "requires_auth": False,
            "rate_limit": "2 seconds between requests",
            "usage": "Direct web scraping (respects robots.txt)"
        },
        {
            "name": "Sketchfab (Public)",
            "description": "Public 3D models on Sketchfab",
            "url": "https://sketchfab.com",
            "requires_auth": False,
            "rate_limit": "1 second between requests",
            "usage": "Public API access (limited)"
        }
    ]
    
    print("✅ Basic integration platforms available:")
    for platform in basic_platforms:
        print(f"  🆓 {platform['name']}")
        print(f"     Description: {platform['description']}")
        print(f"     URL: {platform['url']}")
        print(f"     Rate Limit: {platform['rate_limit']}")
        print(f"     Usage: {platform['usage']}")
        print()
    
    return basic_platforms

def setup_authentication_guide():
    """Provide guide for setting up authentication"""
    print("\n🔐 Authentication Setup Guide")
    print("=" * 40)
    
    auth_platforms = [
        {
            "name": "Sketchfab",
            "phase": "Phase 2",
            "cost": "Free tier available",
            "auth_type": "API Key + OAuth",
            "setup_url": "https://sketchfab.com/developers/oauth",
            "steps": [
                "1. Create account at sketchfab.com",
                "2. Go to Account Settings > API",
                "3. Create new application",
                "4. Get Client ID and Client Secret",
                "5. Set SKETCHFAB_API_KEY in .env file"
            ]
        },
        {
            "name": "Clara.io",
            "phase": "Phase 2", 
            "cost": "Free tier available",
            "auth_type": "API Token",
            "setup_url": "https://clara.io/api",
            "steps": [
                "1. Create account at clara.io",
                "2. Go to Account Settings > API",
                "3. Generate API token",
                "4. Set CLARA_IO_TOKEN in .env file"
            ]
        },
        {
            "name": "Unity Asset Store",
            "phase": "Phase 3",
            "cost": "Free + Premium assets",
            "auth_type": "Unity ID",
            "setup_url": "https://assetstore.unity.com/publisher-settings",
            "steps": [
                "1. Create Unity ID at unity.com",
                "2. Go to Asset Store > Publisher",
                "3. Set up publisher account",
                "4. Set UNITY_ID in .env file"
            ]
        },
        {
            "name": "Adobe Mixamo",
            "phase": "Phase 3",
            "cost": "Free with Adobe ID",
            "auth_type": "Adobe ID + OAuth",
            "setup_url": "https://www.adobe.io/authentication/auth-methods.html",
            "steps": [
                "1. Create Adobe ID at adobe.com",
                "2. Go to Adobe Developer Console",
                "3. Create new project",
                "4. Get Client ID and Client Secret",
                "5. Set ADOBE_ID in .env file"
            ]
        },
        {
            "name": "CGTrader",
            "phase": "Phase 4",
            "cost": "Commercial license required",
            "auth_type": "API Key",
            "setup_url": "https://www.cgtrader.com/developers",
            "steps": [
                "1. Create account at cgtrader.com",
                "2. Go to Developer Settings",
                "3. Request API access",
                "4. Get API key",
                "5. Set CGTRADER_API_KEY in .env file"
            ]
        },
        {
            "name": "TurboSquid",
            "phase": "Phase 4",
            "cost": "Commercial license required",
            "auth_type": "API Key",
            "setup_url": "https://www.turbosquid.com/developers",
            "steps": [
                "1. Create account at turbosquid.com",
                "2. Go to Developer Portal",
                "3. Request API access",
                "4. Get API key",
                "5. Set TURBOSQUID_API_KEY in .env file"
            ]
        },
        {
            "name": "Unreal Marketplace",
            "phase": "Phase 4",
            "cost": "Free with Epic Games ID",
            "auth_type": "Epic Games ID",
            "setup_url": "https://dev.epicgames.com/docs/services/en-US/",
            "steps": [
                "1. Create Epic Games ID at epicgames.com",
                "2. Go to Epic Developer Portal",
                "3. Create new product",
                "4. Get Client ID and Client Secret",
                "5. Set EPIC_ID in .env file"
            ]
        }
    ]
    
    for platform in auth_platforms:
        print(f"🔑 {platform['name']} ({platform['phase']})")
        print(f"   Cost: {platform['cost']}")
        print(f"   Auth Type: {platform['auth_type']}")
        print(f"   Setup URL: {platform['setup_url']}")
        print("   Setup Steps:")
        for step in platform['steps']:
            print(f"     {step}")
        print()
    
    return auth_platforms

def create_quick_start_guide():
    """Create a quick start guide for users"""
    guide_content = """# 3D Asset Integration System - Quick Start Guide

## 🚀 Getting Started

### 1. Basic Setup (No Authentication Required)
```bash
# Run basic integration that works without API keys
cd integrations/basic
python src/basic_asset_scraper.py
```

### 2. Phase 1 - Free & Simple (No Authentication)
```bash
cd integrations/phase1
python main.py setup
python main.py workflow
```

### 3. Phase 2 - Free with Registration (API Keys Required)
```bash
# First, set up your API keys in .env file
cp env.template .env
# Edit .env file with your API keys

cd integrations/phase2
export SKETCHFAB_API_KEY="your_key"
export CLARA_IO_TOKEN="your_token"
python main.py setup
python main.py workflow
```

### 4. Phase 3 - Game Development (Unity/Adobe ID Required)
```bash
cd integrations/phase3
export UNITY_ID="your_unity_id"
export ADOBE_ID="your_adobe_id"
python main.py setup
python main.py workflow
```

### 5. Phase 4 - Professional Marketplaces (Commercial API Keys Required)
```bash
cd integrations/phase4
export CGTRADER_API_KEY="your_key"
export TURBOSQUID_API_KEY="your_key"
export EPIC_ID="your_epic_id"
python main.py setup
python main.py workflow
```

### 6. Advanced Features (Optional)
```bash
cd integrations/advanced
python main.py demo
```

## 🔐 Authentication Setup

### Free Platforms (No Authentication Required)
- OpenGameArt.org
- Free3D
- BlendSwap
- Sketchfab (public assets only)

### Free with Registration
- Sketchfab (full access)
- Clara.io
- Unity Asset Store (free assets)
- Adobe Mixamo (free with Adobe ID)
- Unreal Marketplace (free with Epic ID)

### Commercial Platforms
- CGTrader
- TurboSquid
- Unity Asset Store (premium assets)

## 📝 Environment Variables

Copy `env.template` to `.env` and fill in your credentials:

```bash
cp env.template .env
# Edit .env file with your actual API keys
```

## 🧪 Testing

Test each phase individually:
```bash
# Test Phase 1
cd integrations/phase1 && python main.py test

# Test Phase 2 (requires API keys)
cd integrations/phase2 && python main.py test

# Test Phase 3 (requires Unity/Adobe ID)
cd integrations/phase3 && python main.py test

# Test Phase 4 (requires commercial API keys)
cd integrations/phase4 && python main.py test
```

## 🆘 Troubleshooting

### Common Issues
1. **API Key Not Working**: Check if the key is valid and has proper permissions
2. **Rate Limiting**: Increase delays between requests in configuration
3. **Authentication Failed**: Verify credentials and check platform status
4. **Download Failures**: Check internet connection and file permissions

### Getting Help
- Check the README files in each phase directory
- Review the configuration files
- Check the logs for error messages
- Ensure all dependencies are installed

## 📚 Documentation

- [Phase 1 README](phase1/README.md)
- [Phase 2 README](phase2/README.md)
- [Phase 3 README](phase3/README.md)
- [Phase 4 README](phase4/README.md)
- [Advanced Features README](advanced/README.md)
- [Integration Summary](INTEGRATION_SUMMARY.md)
"""
    
    guide_path = Path(__file__).parent / "QUICK_START_GUIDE.md"
    with open(guide_path, 'w') as f:
        f.write(guide_content)
    
    print(f"✅ Created quick start guide: {guide_path}")
    return guide_path

def main():
    """Main setup function"""
    print("🚀 3D Asset Integration System - Environment Setup")
    print("=" * 60)
    
    # Create .env file from template
    print("\n📝 Setting up environment file...")
    if create_env_file():
        print("✅ Environment file created successfully")
    else:
        print("❌ Failed to create environment file")
        return
    
    # Set up basic integration
    basic_platforms = setup_basic_integration()
    
    # Set up authentication guide
    auth_platforms = setup_authentication_guide()
    
    # Create quick start guide
    guide_path = create_quick_start_guide()
    
    # Summary
    print("\n🎉 Setup Complete!")
    print("=" * 30)
    print(f"✅ Environment file: .env")
    print(f"✅ Quick start guide: {guide_path}")
    print(f"✅ Basic platforms: {len(basic_platforms)} (no auth required)")
    print(f"✅ Auth platforms: {len(auth_platforms)} (API keys required)")
    
    print("\n🚀 Next Steps:")
    print("1. Edit .env file with your API keys (optional)")
    print("2. Start with basic integration: cd integrations/basic && python src/basic_asset_scraper.py")
    print("3. Or start with Phase 1: cd integrations/phase1 && python main.py setup")
    print("4. Read the quick start guide for detailed instructions")
    
    print("\n💡 Tips:")
    print("- Start with basic integration (no API keys needed)")
    print("- Phase 1 works without authentication")
    print("- Get API keys for Phase 2+ for full functionality")
    print("- Check the quick start guide for detailed setup instructions")

if __name__ == "__main__":
    main()
