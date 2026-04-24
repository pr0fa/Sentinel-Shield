import unittest
from unittest.mock import MagicMock
from src.metrics.tdi import TDICalculator

class TestTDI(unittest.TestCase):
    def setUp(self):
        self.calc = TDICalculator(threshold=50.0)

    def test_formula_calculation(self):
        # Mock complexity (Avg = 10)
        comp = MagicMock()
        comp.average_complexity = 10.0
        comp.filepath = "test.py"
        
        # Mock scan (Density = 20)
        scan = MagicMock()
        scan.vulnerability_density = 20.0
        
        res = self.calc.calculate(comp, scan)
        
        self.assertEqual(res.tdi, 15.0)