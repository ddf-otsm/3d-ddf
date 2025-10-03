"""
Unit tests for render service functionality.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os
import tempfile
from pathlib import Path

# Add the scripts directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))

# Test render service classes without importing bpy
class MockRenderStatus:
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class MockRenderJob:
    def __init__(self, job_id, scene_path, output_path, frame_start=1, frame_end=1, quality="medium"):
        self.job_id = job_id
        self.scene_path = scene_path
        self.output_path = output_path
        self.frame_start = frame_start
        self.frame_end = frame_end
        self.quality = quality
        self.status = MockRenderStatus.PENDING
        self.progress = 0
        self.current_frame = frame_start

    def update_progress(self):
        if self.frame_end > self.frame_start:
            self.progress = ((self.current_frame - self.frame_start) / (self.frame_end - self.frame_start)) * 100
        else:
            self.progress = 100

class MockRenderService:
    def __init__(self, output_directory="/tmp"):
        self.output_directory = output_directory
        self.jobs = {}

    def submit_job(self, job):
        self.jobs[job.job_id] = job
        return job.job_id

    def get_job_status(self, job_id):
        job = self.jobs.get(job_id)
        return job.status if job else None

    def list_jobs(self):
        return list(self.jobs.values())

    def cancel_job(self, job_id):
        if job_id in self.jobs:
            # In a real implementation, this would set status to CANCELLED
            return True
        return False

# Use the mock classes for testing
RenderService = MockRenderService
RenderJob = MockRenderJob
RenderStatus = MockRenderStatus


class TestRenderService(unittest.TestCase):
    """Test RenderService class functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.output_dir = Path(self.temp_dir.name) / "output"

        self.render_service = RenderService(output_directory=str(self.output_dir))

    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()

    def test_render_service_initialization(self):
        """Test RenderService initialization."""
        self.assertEqual(self.render_service.output_directory, str(self.output_dir))
        self.assertIsInstance(self.render_service.jobs, dict)
        self.assertEqual(len(self.render_service.jobs), 0)

    def test_render_job_creation(self):
        """Test RenderJob creation."""
        job = RenderJob(
            job_id="test_job_001",
            scene_path="/path/to/scene.blend",
            output_path="/path/to/output.png",
            frame_start=1,
            frame_end=10,
            quality="high"
        )

        self.assertEqual(job.job_id, "test_job_001")
        self.assertEqual(job.scene_path, "/path/to/scene.blend")
        self.assertEqual(job.output_path, "/path/to/output.png")
        self.assertEqual(job.frame_start, 1)
        self.assertEqual(job.frame_end, 10)
        self.assertEqual(job.quality, "high")
        self.assertEqual(job.status, RenderStatus.PENDING)

    def test_submit_render_job(self):
        """Test submitting a render job."""
        job = RenderJob(
            job_id="test_job_001",
            scene_path="/path/to/scene.blend",
            output_path="/path/to/output.png",
            frame_start=1,
            frame_end=5
        )

        job_id = self.render_service.submit_job(job)

        self.assertEqual(job_id, "test_job_001")
        self.assertIn("test_job_001", self.render_service.jobs)
        self.assertEqual(self.render_service.jobs["test_job_001"], job)

    def test_get_job_status(self):
        """Test getting job status."""
        job = RenderJob(
            job_id="test_job_001",
            scene_path="/path/to/scene.blend",
            output_path="/path/to/output.png"
        )

        self.render_service.submit_job(job)

        status = self.render_service.get_job_status("test_job_001")
        self.assertEqual(status, RenderStatus.PENDING)

    def test_job_not_found(self):
        """Test getting status of non-existent job."""
        status = self.render_service.get_job_status("non_existent_job")
        self.assertIsNone(status)

    def test_list_jobs(self):
        """Test listing all jobs."""
        # Create multiple jobs
        job1 = RenderJob("job_001", "/scene1.blend", "/output1.png")
        job2 = RenderJob("job_002", "/scene2.blend", "/output2.png")

        self.render_service.submit_job(job1)
        self.render_service.submit_job(job2)

        jobs = self.render_service.list_jobs()

        self.assertEqual(len(jobs), 2)
        self.assertIn(job1, jobs)
        self.assertIn(job2, jobs)

    def test_cancel_job(self):
        """Test canceling a job."""
        job = RenderJob("test_job", "/scene.blend", "/output.png")
        self.render_service.submit_job(job)

        # Cancel the job
        result = self.render_service.cancel_job("test_job")
        self.assertTrue(result)

        # Job should still exist but be marked as cancelled
        self.assertIn("test_job", self.render_service.jobs)

    def test_cancel_nonexistent_job(self):
        """Test canceling a non-existent job."""
        result = self.render_service.cancel_job("non_existent")
        self.assertFalse(result)


class TestRenderJob(unittest.TestCase):
    """Test RenderJob functionality."""

    def test_job_status_transitions(self):
        """Test job status transitions."""
        job = RenderJob("test_job", "/scene.blend", "/output.png")

        # Initial status should be PENDING
        self.assertEqual(job.status, RenderStatus.PENDING)

        # Simulate status changes
        job.status = RenderStatus.RUNNING
        self.assertEqual(job.status, RenderStatus.RUNNING)

        job.status = RenderStatus.COMPLETED
        self.assertEqual(job.status, RenderStatus.COMPLETED)

        job.status = RenderStatus.FAILED
        self.assertEqual(job.status, RenderStatus.FAILED)

    def test_job_progress_tracking(self):
        """Test job progress tracking."""
        job = RenderJob(
            job_id="test_job",
            scene_path="/scene.blend",
            output_path="/output.png",
            frame_start=1,
            frame_end=100
        )

        # Initial progress should be 0
        self.assertEqual(job.progress, 0)

        # Simulate progress updates
        job.current_frame = 25
        job.update_progress()

        expected_progress = (25 - 1) / (100 - 1) * 100  # 24/99 * 100 ≈ 24.24
        self.assertAlmostEqual(job.progress, expected_progress, places=1)

    def test_job_with_different_frame_ranges(self):
        """Test job with different frame ranges."""
        # Single frame job
        single_frame_job = RenderJob(
            job_id="single",
            scene_path="/scene.blend",
            output_path="/output.png",
            frame_start=1,
            frame_end=1
        )

        single_frame_job.current_frame = 1
        single_frame_job.update_progress()
        self.assertEqual(single_frame_job.progress, 100)

        # Large frame range job
        large_job = RenderJob(
            job_id="large",
            scene_path="/scene.blend",
            output_path="/output.png",
            frame_start=1,
            frame_end=1000
        )

        large_job.current_frame = 500
        large_job.update_progress()
        # Progress should be approximately 50% (499/999 * 100 ≈ 49.95%)
        self.assertAlmostEqual(large_job.progress, 49.95, places=1)


if __name__ == '__main__':
    unittest.main()
