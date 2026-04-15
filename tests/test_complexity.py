import unittest
from src.metrics.complexity import ComplexityAnalyser

class TestComplexity(unittest.TestCase):
    def setUp(self):
        self.analyser = ComplexityAnalyser()

    def test_simple_function(self):
        code = "def test(): pass"
        res = self.analyser.analyse_source(code)
        self.assertEqual(res.functions[0].complexity, 1)

    def test_if_statement(self):
        code = "def test(x):\n    if x: return True\n    return False"
        res = self.analyser.analyse_source(code)
        self.assertEqual(res.functions[0].complexity, 2)