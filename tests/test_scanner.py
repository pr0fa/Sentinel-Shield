import unittest
from src.scanner import Scanner

class TestIntegration(unittest.TestCase):
    def test_full_scan(self):
        s = Scanner()
        c, sc, t = s.scan_source("def f(): pass", "test.py")
        self.assertIsNotNone(t.tdi)

if __name__ == "__main__":
    unittest.main()