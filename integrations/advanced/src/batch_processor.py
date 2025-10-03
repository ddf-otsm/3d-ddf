#!/usr/bin/env python3
"""
Batch Processing System for 3D Assets
Advanced integration feature for processing multiple assets across all phases
"""

import os
import sys
import json
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import threading
from queue import Queue

# Add the config directory to the path
config_path = os.path.join(os.path.dirname(__file__), '..', 'config')
sys.path.insert(0, config_path)

try:
    from settings import BATCH_SETTINGS, PROCESSING_CONFIG
except ImportError:
    # Fallback configuration
    BATCH_SETTINGS = {
        "max_workers": 4,
        "chunk_size": 10,
        "timeout": 300,
        "retry_attempts": 3,
        "progress_callback": True
    }
    PROCESSING_CONFIG = {
        "parallel_processing": True,
        "memory_limit": "2GB",
        "temp_directory": "/tmp/batch_processing",
        "log_level": "INFO"
    }

logger = logging.getLogger(__name__)

class BatchProcessor:
    """Batch processing system for 3D assets across all phases"""
    
    def __init__(self):
        self.batch_settings = BATCH_SETTINGS
        self.processing_config = PROCESSING_CONFIG
        self.processing_queue = Queue()
        self.results = {}
        self.errors = {}
        self.progress = {}
        
        # Initialize processing statistics
        self.stats = {
            "total_tasks": 0,
            "completed_tasks": 0,
            "failed_tasks": 0,
            "processing_time": 0,
            "start_time": None
        }
        
        # Setup temp directory
        self.temp_dir = Path(self.processing_config["temp_directory"])
        self.temp_dir.mkdir(parents=True, exist_ok=True)
    
    def create_batch_job(self, job_name: str, tasks: List[Dict], job_type: str = "asset_processing") -> str:
        """Create a new batch processing job"""
        job_id = f"{job_name}_{int(time.time())}"
        
        job_config = {
            "job_id": job_id,
            "job_name": job_name,
            "job_type": job_type,
            "tasks": tasks,
            "status": "created",
            "created_at": time.time(),
            "progress": 0,
            "results": [],
            "errors": []
        }
        
        # Save job configuration
        job_file = self.temp_dir / f"{job_id}.json"
        with open(job_file, 'w') as f:
            json.dump(job_config, f, indent=2)
        
        logger.info(f"Created batch job: {job_id} with {len(tasks)} tasks")
        return job_id
    
    def process_batch_job(self, job_id: str, callback: Optional[Callable] = None) -> Dict:
        """Process a batch job with parallel execution"""
        job_file = self.temp_dir / f"{job_id}.json"
        if not job_file.exists():
            raise FileNotFoundError(f"Job {job_id} not found")
        
        # Load job configuration
        with open(job_file, 'r') as f:
            job_config = json.load(f)
        
        job_config["status"] = "processing"
        job_config["started_at"] = time.time()
        
        # Update job file
        with open(job_file, 'w') as f:
            json.dump(job_config, f, indent=2)
        
        self.stats["start_time"] = time.time()
        self.stats["total_tasks"] = len(job_config["tasks"])
        
        try:
            if self.batch_settings["max_workers"] > 1:
                results = self._process_parallel(job_config, callback)
            else:
                results = self._process_sequential(job_config, callback)
            
            # Update job status
            job_config["status"] = "completed"
            job_config["completed_at"] = time.time()
            job_config["results"] = results
            
            with open(job_file, 'w') as f:
                json.dump(job_config, f, indent=2)
            
            self.stats["processing_time"] = time.time() - self.stats["start_time"]
            logger.info(f"Batch job {job_id} completed in {self.stats['processing_time']:.2f} seconds")
            
            return {
                "job_id": job_id,
                "status": "completed",
                "results": results,
                "stats": self.stats
            }
            
        except Exception as e:
            job_config["status"] = "failed"
            job_config["error"] = str(e)
            
            with open(job_file, 'w') as f:
                json.dump(job_config, f, indent=2)
            
            logger.error(f"Batch job {job_id} failed: {e}")
            raise
    
    def _process_parallel(self, job_config: Dict, callback: Optional[Callable] = None) -> List[Dict]:
        """Process tasks in parallel using ThreadPoolExecutor"""
        results = []
        errors = []
        
        with ThreadPoolExecutor(max_workers=self.batch_settings["max_workers"]) as executor:
            # Submit all tasks
            future_to_task = {}
            for i, task in enumerate(job_config["tasks"]):
                future = executor.submit(self._process_single_task, task, i)
                future_to_task[future] = (task, i)
            
            # Collect results as they complete
            for future in future_to_task:
                task, task_index = future_to_task[future]
                try:
                    result = future.result(timeout=self.batch_settings["timeout"])
                    results.append({
                        "task_index": task_index,
                        "task": task,
                        "result": result,
                        "status": "success"
                    })
                    self.stats["completed_tasks"] += 1
                    
                    # Call progress callback if provided
                    if callback:
                        progress = (self.stats["completed_tasks"] / self.stats["total_tasks"]) * 100
                        callback(progress, f"Completed task {task_index + 1}")
                    
                except Exception as e:
                    error_info = {
                        "task_index": task_index,
                        "task": task,
                        "error": str(e),
                        "status": "failed"
                    }
                    errors.append(error_info)
                    results.append(error_info)
                    self.stats["failed_tasks"] += 1
                    
                    logger.error(f"Task {task_index} failed: {e}")
        
        return results
    
    def _process_sequential(self, job_config: Dict, callback: Optional[Callable] = None) -> List[Dict]:
        """Process tasks sequentially"""
        results = []
        
        for i, task in enumerate(job_config["tasks"]):
            try:
                result = self._process_single_task(task, i)
                results.append({
                    "task_index": i,
                    "task": task,
                    "result": result,
                    "status": "success"
                })
                self.stats["completed_tasks"] += 1
                
                # Call progress callback if provided
                if callback:
                    progress = ((i + 1) / len(job_config["tasks"])) * 100
                    callback(progress, f"Completed task {i + 1}")
                
            except Exception as e:
                error_info = {
                    "task_index": i,
                    "task": task,
                    "error": str(e),
                    "status": "failed"
                }
                results.append(error_info)
                self.stats["failed_tasks"] += 1
                
                logger.error(f"Task {i} failed: {e}")
        
        return results
    
    def _process_single_task(self, task: Dict, task_index: int) -> Dict:
        """Process a single task"""
        task_type = task.get("type", "unknown")
        
        if task_type == "asset_download":
            return self._process_asset_download(task)
        elif task_type == "asset_import":
            return self._process_asset_import(task)
        elif task_type == "asset_optimization":
            return self._process_asset_optimization(task)
        elif task_type == "asset_export":
            return self._process_asset_export(task)
        elif task_type == "asset_analysis":
            return self._process_asset_analysis(task)
        else:
            raise ValueError(f"Unknown task type: {task_type}")
    
    def _process_asset_download(self, task: Dict) -> Dict:
        """Process asset download task"""
        # Simulate asset download
        time.sleep(0.1)  # Simulate download time
        
        return {
            "action": "download",
            "asset_id": task.get("asset_id"),
            "platform": task.get("platform"),
            "status": "downloaded",
            "file_path": f"/tmp/downloaded_{task.get('asset_id')}.fbx",
            "file_size": 1024000,  # 1MB
            "download_time": 0.1
        }
    
    def _process_asset_import(self, task: Dict) -> Dict:
        """Process asset import task"""
        # Simulate asset import
        time.sleep(0.2)  # Simulate import time
        
        return {
            "action": "import",
            "asset_id": task.get("asset_id"),
            "blender_object": f"Imported_{task.get('asset_id')}",
            "status": "imported",
            "import_time": 0.2,
            "objects_created": 1
        }
    
    def _process_asset_optimization(self, task: Dict) -> Dict:
        """Process asset optimization task"""
        # Simulate asset optimization
        time.sleep(0.3)  # Simulate optimization time
        
        return {
            "action": "optimize",
            "asset_id": task.get("asset_id"),
            "optimization_level": task.get("optimization_level", "medium"),
            "status": "optimized",
            "optimization_time": 0.3,
            "polygon_reduction": 0.2,
            "texture_optimization": True
        }
    
    def _process_asset_export(self, task: Dict) -> Dict:
        """Process asset export task"""
        # Simulate asset export
        time.sleep(0.15)  # Simulate export time
        
        return {
            "action": "export",
            "asset_id": task.get("asset_id"),
            "export_format": task.get("export_format", "fbx"),
            "status": "exported",
            "export_time": 0.15,
            "output_path": f"/tmp/exported_{task.get('asset_id')}.fbx"
        }
    
    def _process_asset_analysis(self, task: Dict) -> Dict:
        """Process asset analysis task"""
        # Simulate asset analysis
        time.sleep(0.05)  # Simulate analysis time
        
        return {
            "action": "analyze",
            "asset_id": task.get("asset_id"),
            "analysis_type": task.get("analysis_type", "general"),
            "status": "analyzed",
            "analysis_time": 0.05,
            "polygon_count": 15000,
            "texture_count": 5,
            "material_count": 3,
            "animation_frames": 0
        }
    
    def get_job_status(self, job_id: str) -> Dict:
        """Get the status of a batch job"""
        job_file = self.temp_dir / f"{job_id}.json"
        if not job_file.exists():
            return {"error": f"Job {job_id} not found"}
        
        with open(job_file, 'r') as f:
            job_config = json.load(f)
        
        return {
            "job_id": job_id,
            "status": job_config["status"],
            "progress": job_config.get("progress", 0),
            "total_tasks": len(job_config["tasks"]),
            "completed_tasks": len([r for r in job_config.get("results", []) if r.get("status") == "success"]),
            "failed_tasks": len([r for r in job_config.get("results", []) if r.get("status") == "failed"]),
            "created_at": job_config.get("created_at"),
            "started_at": job_config.get("started_at"),
            "completed_at": job_config.get("completed_at")
        }
    
    def cancel_job(self, job_id: str) -> bool:
        """Cancel a running batch job"""
        job_file = self.temp_dir / f"{job_id}.json"
        if not job_file.exists():
            return False
        
        with open(job_file, 'r') as f:
            job_config = json.load(f)
        
        if job_config["status"] == "processing":
            job_config["status"] = "cancelled"
            job_config["cancelled_at"] = time.time()
            
            with open(job_file, 'w') as f:
                json.dump(job_config, f, indent=2)
            
            logger.info(f"Job {job_id} cancelled")
            return True
        
        return False
    
    def cleanup_completed_jobs(self, older_than_hours: int = 24) -> int:
        """Clean up completed jobs older than specified hours"""
        current_time = time.time()
        cutoff_time = current_time - (older_than_hours * 3600)
        
        cleaned_count = 0
        for job_file in self.temp_dir.glob("*.json"):
            try:
                with open(job_file, 'r') as f:
                    job_config = json.load(f)
                
                if (job_config.get("status") in ["completed", "failed", "cancelled"] and 
                    job_config.get("completed_at", 0) < cutoff_time):
                    job_file.unlink()
                    cleaned_count += 1
                    
            except Exception as e:
                logger.error(f"Error cleaning up job file {job_file}: {e}")
        
        logger.info(f"Cleaned up {cleaned_count} old job files")
        return cleaned_count
    
    def get_processing_stats(self) -> Dict:
        """Get processing statistics"""
        return {
            "total_tasks": self.stats["total_tasks"],
            "completed_tasks": self.stats["completed_tasks"],
            "failed_tasks": self.stats["failed_tasks"],
            "success_rate": (self.stats["completed_tasks"] / max(self.stats["total_tasks"], 1)) * 100,
            "processing_time": self.stats["processing_time"],
            "average_task_time": self.stats["processing_time"] / max(self.stats["completed_tasks"], 1),
            "active_jobs": len(list(self.temp_dir.glob("*.json")))
        }

def main():
    """Main function to demonstrate batch processing"""
    print("⚡ Batch Processing System for 3D Assets")
    print("=" * 50)
    
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
    
    # Get job status
    print(f"\n📋 Job Status:")
    status = processor.get_job_status(job_id)
    print(f"  Status: {status['status']}")
    print(f"  Progress: {status['progress']}%")
    print(f"  Completed tasks: {status['completed_tasks']}/{status['total_tasks']}")
    
    print(f"\n✅ Batch processing system ready!")

if __name__ == "__main__":
    main()
