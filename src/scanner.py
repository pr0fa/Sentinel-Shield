from .metrics.complexity import ComplexityAnalyser
from .security.vulnerability_scanner import VulnerabilityScanner
from .metrics.tdi import TDICalculator

class Scanner:
    def __init__(self, threshold=50.0):
        self._complexity_analyser = ComplexityAnalyser()
        self._vuln_scanner = VulnerabilityScanner()
        self._tdi_calc = TDICalculator(threshold=threshold)

    def scan_source(self, source_code: str, filepath: str = "<unknown>"):
        complexity = self._complexity_analyser.analyse_source(source_code, filepath)
        scan = self._vuln_scanner.scan_source(source_code, filepath)
        tdi = self._tdi_calc.calculate(complexity, scan)
        return complexity, scan, tdi