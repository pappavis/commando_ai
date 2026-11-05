"""
Verwysing na amptelike toetse in ./tests/
"""
import os
import sys

# Laai toetse vanuit ./tests/
if __name__ == "__main__":
    import unittest
    suite = unittest.defaultTestLoader.discover(os.path.join(os.path.dirname(__file__), "..", "tests"))
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    sys.exit(not result.wasSuccessful())
