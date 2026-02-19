import ast
from dataclasses import dataclass, field
from typing import List

def _risk_level(complexity: int) -> str:
    if complexity <= 5:
        return "LOW"
    if complexity <= 10:
        return "MODERATE"
    if complexity <= 15:
        return "HIGH"
    return "CRITICAL"

@dataclass
class FunctionComplexity:
    name: str
    lineno: int
    complexity: int
    risk_level: str = field(init=False)

    def __post_init__(self):
        self.risk_level = _risk_level(self.complexity)

@dataclass
class ModuleComplexity:
    filepath: str
    functions: List[FunctionComplexity]

    @property
    def total_complexity(self) -> int:
        return sum(f.complexity for f in self.functions)

    @property
    def average_complexity(self) -> float:
        if not self.functions:
            return 0.0
        return self.total_complexity / len(self.functions)
    
class _ComplexityVisitor(ast.NodeVisitor):
    def __init__(self):
        self.complexity = 1 

    def visit_If(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_For(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_While(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        self.complexity += len(node.values) - 1
        self.generic_visit(node)

class ComplexityAnalyser:
    def analyse_source(self, source_code: str, filepath: str = "<unknown>") -> ModuleComplexity:
        tree = ast.parse(source_code, filename=filepath)
        functions: List[FunctionComplexity] = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                visitor = _ComplexityVisitor()
                visitor.visit(node)
                functions.append(FunctionComplexity(name=node.name, lineno=node.lineno, complexity=visitor.complexity))
        return ModuleComplexity(filepath=filepath, functions=functions)