"""
Advanced Integration Features Configuration
Settings for AI recommendations, batch processing, and custom platforms
"""

from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent.parent
ASSETS_DIR = BASE_DIR / "assets"

# AI Recommendation Settings
AI_SETTINGS = {
    "model_type": "content_based",
    "similarity_threshold": 0.7,
    "max_recommendations": 10,
    "learning_rate": 0.01,
    "feature_weights": {
        "visual": 0.3,
        "technical": 0.25,
        "content": 0.2,
        "quality": 0.15,
        "usage": 0.1
    },
    "recommendation_engine": {
        "enabled": True,
        "model_path": "models/asset_recommender.pkl",
        "feature_extraction": True,
        "collaborative_filtering": True,
        "content_based_filtering": True
    }
}

# Batch Processing Settings
BATCH_SETTINGS = {
    "max_workers": 4,
    "chunk_size": 10,
    "timeout": 300,
    "retry_attempts": 3,
    "progress_callback": True,
    "memory_limit": "2GB",
    "temp_directory": "/tmp/batch_processing",
    "cleanup_after_hours": 24,
    "parallel_processing": True,
    "task_prioritization": True
}

# Custom Platform Settings
CUSTOM_PLATFORM_SETTINGS = {
    "template_directory": "templates",
    "plugin_directory": "plugins",
    "validation_enabled": True,
    "auto_discovery": True,
    "plugin_auto_reload": True,
    "sandbox_mode": False
}

# Integration Templates
INTEGRATION_TEMPLATES = {
    "basic": "basic_platform_template.py",
    "advanced": "advanced_platform_template.py",
    "api_based": "api_platform_template.py",
    "oauth": "oauth_platform_template.py",
    "graphql": "graphql_platform_template.py"
}

# Advanced Workflow Settings
ADVANCED_WORKFLOW = {
    "ai_recommendations": {
        "enabled": True,
        "min_similarity": 0.6,
        "max_recommendations": 20,
        "learning_enabled": True,
        "feedback_weight": 0.1
    },
    "batch_processing": {
        "enabled": True,
        "max_concurrent_jobs": 5,
        "job_timeout": 3600,
        "retry_failed_tasks": True,
        "progress_tracking": True
    },
    "custom_platforms": {
        "enabled": True,
        "auto_validation": True,
        "plugin_management": True,
        "template_generation": True
    },
    "analytics": {
        "enabled": True,
        "track_usage": True,
        "performance_metrics": True,
        "user_behavior": True,
        "asset_trends": True
    }
}

# AI Model Configuration
AI_MODELS = {
    "content_based": {
        "type": "content_based",
        "algorithm": "cosine_similarity",
        "features": ["visual", "technical", "content", "quality", "usage"],
        "similarity_threshold": 0.7,
        "max_features": 100
    },
    "collaborative": {
        "type": "collaborative",
        "algorithm": "matrix_factorization",
        "min_users": 5,
        "min_items": 3,
        "factors": 50,
        "regularization": 0.01
    },
    "hybrid": {
        "type": "hybrid",
        "content_weight": 0.6,
        "collaborative_weight": 0.4,
        "ensemble_method": "weighted_average"
    }
}

# Batch Processing Configuration
PROCESSING_CONFIG = {
    "parallel_processing": True,
    "memory_limit": "2GB",
    "temp_directory": "/tmp/batch_processing",
    "log_level": "INFO",
    "task_types": [
        "asset_download",
        "asset_import", 
        "asset_optimization",
        "asset_export",
        "asset_analysis",
        "asset_conversion",
        "asset_validation"
    ],
    "priority_levels": {
        "high": 1,
        "medium": 2,
        "low": 3
    },
    "retry_strategies": {
        "exponential_backoff": True,
        "max_retry_delay": 300,
        "retry_multiplier": 2.0
    }
}

# Custom Platform Templates
PLATFORM_TEMPLATES = {
    "basic": {
        "description": "Basic platform integration with essential features",
        "features": ["search", "download", "authentication"],
        "complexity": "low",
        "estimated_time": "2-4 hours"
    },
    "advanced": {
        "description": "Advanced platform integration with enhanced features",
        "features": ["search", "download", "authentication", "rate_limiting", "quality_scoring"],
        "complexity": "medium",
        "estimated_time": "1-2 days"
    },
    "api_based": {
        "description": "API-based platform integration",
        "features": ["api_integration", "rate_limiting", "error_handling"],
        "complexity": "medium",
        "estimated_time": "1-2 days"
    },
    "oauth": {
        "description": "OAuth-based platform integration",
        "features": ["oauth_authentication", "token_management", "refresh_tokens"],
        "complexity": "high",
        "estimated_time": "2-3 days"
    },
    "graphql": {
        "description": "GraphQL-based platform integration",
        "features": ["graphql_queries", "schema_validation", "query_optimization"],
        "complexity": "high",
        "estimated_time": "2-3 days"
    }
}

# Analytics Configuration
ANALYTICS_CONFIG = {
    "tracking_enabled": True,
    "metrics": {
        "usage_stats": True,
        "performance_metrics": True,
        "user_behavior": True,
        "asset_trends": True,
        "error_rates": True,
        "success_rates": True
    },
    "data_retention": {
        "raw_data_days": 30,
        "aggregated_data_days": 365,
        "anonymize_data": True
    },
    "reporting": {
        "daily_reports": True,
        "weekly_reports": True,
        "monthly_reports": True,
        "custom_reports": True
    }
}

# Performance Optimization
PERFORMANCE_CONFIG = {
    "caching": {
        "enabled": True,
        "cache_size": "100MB",
        "ttl": 3600,
        "cache_backend": "memory"
    },
    "compression": {
        "enabled": True,
        "algorithm": "gzip",
        "level": 6
    },
    "optimization": {
        "lazy_loading": True,
        "connection_pooling": True,
        "request_batching": True,
        "parallel_processing": True
    }
}

# Security Configuration
SECURITY_CONFIG = {
    "authentication": {
        "api_key_encryption": True,
        "token_expiration": 3600,
        "refresh_token_rotation": True
    },
    "data_protection": {
        "encrypt_sensitive_data": True,
        "secure_temp_files": True,
        "audit_logging": True
    },
    "rate_limiting": {
        "enabled": True,
        "requests_per_minute": 60,
        "burst_limit": 10
    }
}

# Logging Configuration
LOGGING = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": str(BASE_DIR / "advanced.log"),
    "max_size": 52428800,  # 50MB
    "backup_count": 10,
    "advanced_features": {
        "structured_logging": True,
        "log_aggregation": True,
        "real_time_monitoring": True
    }
}
