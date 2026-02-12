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