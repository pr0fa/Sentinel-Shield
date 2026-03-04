from dataclasses import dataclass
from .complexity import ModuleComplexity

def _risk_level(tdi: float) -> str:
    if tdi < 20: return "LOW"
    if tdi < 50: return "MODERATE"
    if tdi < 80: return "HIGH"
    return "CRITICAL"

@dataclass
class TDIResult:
    filepath: str
    complexity_score: float
    vulnerability_density: float
    tdi: float
    risk_level: str
    alert: bool

class TDICalculator:
    def __init__(self, threshold: float = 50.0):
        self._threshold = threshold

    def calculate(self, complexity: ModuleComplexity, scan) -> TDIResult:
        complexity_score = float(complexity.average_complexity)
        vulnerability_density = scan.vulnerability_density
        tdi = (complexity_score * 0.5) + (vulnerability_density * 0.5)
        risk = _risk_level(tdi)
        return TDIResult(
            filepath=complexity.filepath,
            complexity_score=complexity_score,
            vulnerability_density=vulnerability_density,
            tdi=tdi,
            risk_level=risk,
            alert=tdi >= self._threshold
        )