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

    def test_loops(self):
        code = "def test(lst):\n    for x in lst:\n        while x < 10: x += 1"
        res = self.analyser.analyse_source(code)
        # Base(1) + For(1) + While(1) = 3
        self.assertEqual(res.functions[0].complexity, 3)

    def test_boolean_logic(self):
        code = "def test(a, b, c):\n    if a and b or c: return True"
        res = self.analyser.analyse_source(code)
        # Base(1) + If(1) + And(1) + Or(1) = 4
        self.assertEqual(res.functions[0].complexity, 4)

    def test_syntax_error(self):
        with self.assertRaises(SyntaxError):
            self.analyser.analyse_source("def broken(x): if x")

if __name__ == "__main__":
    unittest.main()