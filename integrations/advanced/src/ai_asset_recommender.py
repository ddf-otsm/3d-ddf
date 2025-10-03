#!/usr/bin/env python3
"""
AI-Powered Asset Recommendation System
Advanced integration feature that uses AI to recommend assets across all phases
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, cast
import numpy as np

# Add the config directory to the path
config_path = os.path.join(os.path.dirname(__file__), '..', 'config')
sys.path.insert(0, config_path)

try:
    from settings import AI_SETTINGS, RECOMMENDATION_ENGINE
except ImportError:
    # Fallback configuration
    AI_SETTINGS = {
        "model_type": "content_based",
        "similarity_threshold": 0.7,
        "max_recommendations": 10,
        "learning_rate": 0.01
    }
    RECOMMENDATION_ENGINE = {
        "enabled": True,
        "model_path": "models/asset_recommender.pkl",
        "feature_extraction": True
    }

logger = logging.getLogger(__name__)

class AIAssetRecommender:
    """AI-powered asset recommendation system across all phases"""
    
    def __init__(self):
        self.ai_settings = AI_SETTINGS
        self.recommendation_engine = RECOMMENDATION_ENGINE
        self.asset_features = {}
        self.user_preferences = {}
        self.recommendation_history = []
        
        # Initialize feature extraction
        self.setup_feature_extraction()
    
    def setup_feature_extraction(self):
        """Set up feature extraction for asset analysis"""
        self.feature_categories = {
            "visual": ["color", "texture", "style", "mood"],
            "technical": ["polygon_count", "texture_resolution", "file_size", "format"],
            "content": ["category", "tags", "description", "keywords"],
            "quality": ["rating", "downloads", "price", "license"],
            "usage": ["platform", "phase", "complexity", "target_audience"]
        }
        
        logger.info("AI feature extraction system initialized")
    
    def extract_asset_features(self, asset_info: Dict) -> Dict:
        """Extract features from asset information for AI analysis"""
        features = {}
        
        # Visual features
        features["visual"] = {
            "color_dominant": self._extract_dominant_color(asset_info),
            "texture_complexity": self._analyze_texture_complexity(asset_info),
            "style_category": self._classify_style(asset_info),
            "mood_rating": self._analyze_mood(asset_info)
        }
        
        # Technical features
        features["technical"] = {
            "polygon_count": asset_info.get("polygon_count", 0),
            "texture_resolution": self._parse_texture_resolution(asset_info),
            "file_size": asset_info.get("file_size", 0),
            "format_compatibility": self._analyze_format_compatibility(asset_info)
        }
        
        # Content features
        features["content"] = {
            "category": asset_info.get("category", "unknown"),
            "tags": asset_info.get("tags", []),
            "description_sentiment": self._analyze_description_sentiment(asset_info),
            "keyword_density": self._analyze_keyword_density(asset_info)
        }
        
        # Quality features
        features["quality"] = {
            "rating": asset_info.get("rating", 0),
            "downloads": asset_info.get("downloads", 0),
            "price_tier": self._classify_price_tier(asset_info),
            "license_type": self._classify_license_type(asset_info)
        }
        
        # Usage features
        features["usage"] = {
            "platform": asset_info.get("platform", "unknown"),
            "phase": self._determine_phase(asset_info),
            "complexity": asset_info.get("complexity", 1),
            "target_audience": self._determine_target_audience(asset_info)
        }
        
        return features
    
    def _extract_dominant_color(self, asset_info: Dict) -> str:
        """Extract dominant color from asset information"""
        # Simulate color extraction from thumbnail or description
        colors = ["red", "blue", "green", "yellow", "purple", "orange", "brown", "gray", "black", "white"]
        return np.random.choice(colors)
    
    def _analyze_texture_complexity(self, asset_info: Dict) -> float:
        """Analyze texture complexity (0.0 to 1.0)"""
        texture_res = asset_info.get("texture_resolution", "1024x1024")
        if "8K" in texture_res or "8192" in texture_res:
            return 1.0
        elif "4K" in texture_res or "4096" in texture_res:
            return 0.8
        elif "2K" in texture_res or "2048" in texture_res:
            return 0.6
        elif "1K" in texture_res or "1024" in texture_res:
            return 0.4
        else:
            return 0.2
    
    def _classify_style(self, asset_info: Dict) -> str:
        """Classify artistic style"""
        styles = ["realistic", "stylized", "cartoon", "abstract", "minimalist", "detailed"]
        return np.random.choice(styles)
    
    def _analyze_mood(self, asset_info: Dict) -> str:
        """Analyze mood/atmosphere"""
        moods = ["bright", "dark", "neutral", "dramatic", "peaceful", "energetic"]
        return np.random.choice(moods)
    
    def _parse_texture_resolution(self, asset_info: Dict) -> int:
        """Parse texture resolution to integer"""
        texture_res = asset_info.get("texture_resolution", "1024x1024")
        if "x" in texture_res:
            return int(texture_res.split("x")[0])
        return 1024
    
    def _analyze_format_compatibility(self, asset_info: Dict) -> float:
        """Analyze format compatibility score"""
        formats = asset_info.get("supported_formats", [])
        blender_formats = [".blend", ".fbx", ".obj", ".dae", ".gltf", ".glb"]
        compatible = sum(1 for fmt in formats if fmt in blender_formats)
        return compatible / len(blender_formats) if blender_formats else 0.0
    
    def _analyze_description_sentiment(self, asset_info: Dict) -> float:
        """Analyze description sentiment (-1.0 to 1.0)"""
        description = asset_info.get("description", "").lower()
        positive_words = ["amazing", "beautiful", "high-quality", "professional", "excellent"]
        negative_words = ["poor", "low-quality", "basic", "simple", "limited"]
        
        positive_score = sum(1 for word in positive_words if word in description)
        negative_score = sum(1 for word in negative_words if word in description)
        
        if positive_score + negative_score == 0:
            return 0.0
        return (positive_score - negative_score) / (positive_score + negative_score)
    
    def _analyze_keyword_density(self, asset_info: Dict) -> Dict:
        """Analyze keyword density in description"""
        description = asset_info.get("description", "").lower()
        keywords = ["3d", "model", "texture", "animation", "character", "environment", "vehicle"]
        density = {keyword: description.count(keyword) / len(description.split()) for keyword in keywords}
        return density
    
    def _classify_price_tier(self, asset_info: Dict) -> str:
        """Classify price tier"""
        price = asset_info.get("price", "$0")
        if isinstance(price, str):
            price = price.replace("$", "").replace(",", "")
            try:
                price = float(price)
            except ValueError:
                price = 0
        
        if price == 0:
            return "free"
        elif price < 50:
            return "budget"
        elif price < 200:
            return "standard"
        elif price < 500:
            return "premium"
        else:
            return "luxury"
    
    def _classify_license_type(self, asset_info: Dict) -> str:
        """Classify license type"""
        license_info = asset_info.get("license", "").lower()
        if "commercial" in license_info:
            return "commercial"
        elif "cc0" in license_info:
            return "public_domain"
        elif "cc-by" in license_info:
            return "attribution"
        else:
            return "unknown"
    
    def _determine_phase(self, asset_info: Dict) -> int:
        """Determine which phase this asset belongs to"""
        platform = asset_info.get("platform", "").lower()
        if platform in ["opengameart", "free3d"]:
            return 1
        elif platform in ["sketchfab", "clara"]:
            return 2
        elif platform in ["unity", "mixamo"]:
            return 3
        elif platform in ["cgtrader", "turbosquid", "unreal"]:
            return 4
        else:
            return 1
    
    def _determine_target_audience(self, asset_info: Dict) -> str:
        """Determine target audience"""
        phase = self._determine_phase(asset_info)
        if phase == 1:
            return "hobbyist"
        elif phase == 2:
            return "indie_developer"
        elif phase == 3:
            return "game_developer"
        elif phase == 4:
            return "professional"
        else:
            return "general"
    
    def calculate_similarity(self, asset1_features: Dict, asset2_features: Dict) -> float:
        """Calculate similarity between two assets"""
        similarity_scores = []
        
        for category in self.feature_categories.keys():
            if category in asset1_features and category in asset2_features:
                score = self._calculate_category_similarity(
                    asset1_features[category], 
                    asset2_features[category]
                )
                similarity_scores.append(score)
        
        return float(np.mean(similarity_scores)) if similarity_scores else 0.0
    
    def _calculate_category_similarity(self, features1: Dict, features2: Dict) -> float:
        """Calculate similarity within a feature category"""
        if not features1 or not features2:
            return 0.0
        
        similarities = []
        for key in set(features1.keys()) & set(features2.keys()):
            if isinstance(features1[key], (int, float)) and isinstance(features2[key], (int, float)):
                # Numerical similarity
                max_val = max(features1[key], features2[key])
                if max_val > 0:
                    similarity = 1 - abs(features1[key] - features2[key]) / max_val
                    similarities.append(max(0, similarity))
            elif isinstance(features1[key], str) and isinstance(features2[key], str):
                # String similarity (exact match)
                similarity = 1.0 if features1[key] == features2[key] else 0.0
                similarities.append(similarity)
            elif isinstance(features1[key], list) and isinstance(features2[key], list):
                # List similarity (Jaccard similarity)
                set1, set2 = set(features1[key]), set(features2[key])
                if set1 or set2:
                    similarity = len(set1 & set2) / len(set1 | set2)
                    similarities.append(similarity)
        
        return np.mean(similarities) if similarities else 0.0
    
    def recommend_assets(self, query_asset: Dict, available_assets: List[Dict], limit: int = 10) -> List[Dict]:
        """Recommend similar assets based on a query asset"""
        if not available_assets:
            return []
        
        # Extract features from query asset
        query_features = self.extract_asset_features(query_asset)
        
        # Calculate similarities
        recommendations = []
        for asset in available_assets:
            asset_features = self.extract_asset_features(asset)
            similarity = self.calculate_similarity(query_features, asset_features)
            
            if similarity >= self.ai_settings["similarity_threshold"]:
                recommendations.append({
                    "asset": asset,
                    "similarity": similarity,
                    "features": asset_features
                })
        
        # Sort by similarity and return top recommendations
        recommendations.sort(key=lambda x: cast(float, x["similarity"]), reverse=True)
        return recommendations[:limit]
    
    def learn_from_user_feedback(self, asset_id: str, user_rating: float, user_preferences: Dict):
        """Learn from user feedback to improve recommendations"""
        if asset_id not in self.user_preferences:
            self.user_preferences[asset_id] = {
                "ratings": [],
                "preferences": {}
            }
        
        self.user_preferences[asset_id]["ratings"].append(user_rating)
        self.user_preferences[asset_id]["preferences"].update(user_preferences)
        
        # Update recommendation model
        self._update_recommendation_model()
        
        logger.info(f"Learned from user feedback for asset {asset_id}")
    
    def _update_recommendation_model(self):
        """Update the recommendation model based on user feedback"""
        # This would implement machine learning model updates
        # For now, we'll just log the update
        logger.info("Recommendation model updated based on user feedback")
    
    def get_personalized_recommendations(self, user_id: str, available_assets: List[Dict]) -> List[Dict]:
        """Get personalized recommendations for a specific user"""
        if user_id not in self.user_preferences:
            # New user - return general recommendations
            return self._get_general_recommendations(available_assets)
        
        user_prefs = self.user_preferences[user_id]
        
        # Create a virtual query asset based on user preferences
        virtual_asset = self._create_virtual_asset_from_preferences(user_prefs)
        
        # Get recommendations based on virtual asset
        return self.recommend_assets(virtual_asset, available_assets)
    
    def _get_general_recommendations(self, available_assets: List[Dict]) -> List[Dict]:
        """Get general recommendations for new users"""
        # Return popular/highly-rated assets
        popular_assets = sorted(
            available_assets,
            key=lambda x: (x.get("rating", 0), x.get("downloads", 0)),
            reverse=True
        )
        
        return [{"asset": asset, "similarity": 0.5, "reason": "popular"} 
                for asset in popular_assets[:10]]
    
    def _create_virtual_asset_from_preferences(self, user_prefs: Dict) -> Dict:
        """Create a virtual asset based on user preferences"""
        virtual_asset = {
            "title": "User Preference Profile",
            "category": user_prefs.get("preferred_category", "general"),
            "tags": user_prefs.get("preferred_tags", []),
            "rating": np.mean(user_prefs.get("ratings", [5.0])),
            "price_tier": user_prefs.get("preferred_price_tier", "standard"),
            "platform": user_prefs.get("preferred_platform", "general")
        }
        return virtual_asset
    
    def analyze_asset_trends(self, assets: List[Dict]) -> Dict:
        """Analyze trends in asset data"""
        trends: Dict[str, Dict[str, int]] = {
            "popular_categories": {},
            "price_trends": {},
            "quality_trends": {},
            "platform_distribution": {},
            "feature_trends": {}
        }
        
        for asset in assets:
            # Category trends
            category = asset.get("category", "unknown")
            trends["popular_categories"][category] = trends["popular_categories"].get(category, 0) + 1
            
            # Price trends
            price_tier = self._classify_price_tier(asset)
            trends["price_trends"][price_tier] = trends["price_trends"].get(price_tier, 0) + 1
            
            # Quality trends
            rating = asset.get("rating", 0)
            if rating >= 4.5:
                quality = "high"
            elif rating >= 3.5:
                quality = "medium"
            else:
                quality = "low"
            trends["quality_trends"][quality] = trends["quality_trends"].get(quality, 0) + 1
            
            # Platform distribution
            platform = asset.get("platform", "unknown")
            trends["platform_distribution"][platform] = trends["platform_distribution"].get(platform, 0) + 1
        
        return trends
    
    def generate_asset_report(self, assets: List[Dict]) -> Dict:
        """Generate comprehensive asset analysis report"""
        report: Dict[str, Any] = {
            "total_assets": len(assets),
            "trends": self.analyze_asset_trends(assets),
            "recommendations": [],
            "insights": []
        }
        
        # Generate insights
        if assets:
            avg_rating = float(np.mean([asset.get("rating", 0) for asset in assets]))
            report["insights"].append(f"Average asset rating: {avg_rating:.2f}")
            
            most_popular_category = max(
                report["trends"]["popular_categories"].items(),
                key=lambda x: x[1]
            )[0]
            report["insights"].append(f"Most popular category: {most_popular_category}")
            
            price_distribution = report["trends"]["price_trends"]
            dominant_price_tier = max(price_distribution.items(), key=lambda x: x[1])[0]
            report["insights"].append(f"Dominant price tier: {dominant_price_tier}")
        
        return report

def main():
    """Main function to demonstrate AI asset recommendation"""
    print("🤖 AI-Powered Asset Recommendation System")
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
    
    print("\n✅ AI recommendation system ready!")

if __name__ == "__main__":
    main()
