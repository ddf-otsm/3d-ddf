# 3D Asset Integration System - Quick Start Guide

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
