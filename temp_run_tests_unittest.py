import sys
import os

# Add project root to path
project_root = '${PROJECT_ROOT}'
sys.path.insert(0, project_root)

# Change to project root
os.chdir(project_root)

# Run the tests
import unittest
loader = unittest.TestLoader()
suite = loader.discover('tests/explosions', pattern='test_*.py')
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
