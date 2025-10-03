import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Import the test module
from tests.explosions.test_explosion_system import *

if __name__ == "__main__":
    # Run unittest
    unittest.main(verbosity=2, exit=False)
