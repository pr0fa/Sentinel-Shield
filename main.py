import sys
from src.metrics.complexity import ComplexityAnalyser
from src.security.vulnerability_scanner import VulnerabilityScanner

def main():
    if len(sys.argv) < 2: return
    source = open(sys.argv[1]).read()
    comp = ComplexityAnalyser().analyse_source(source, sys.argv[1])
    vuln = VulnerabilityScanner().scan_source(source, sys.argv[1])
    print(f"File: {sys.argv[1]} | Complexity: {comp.average_complexity} | Vulns: {len(vuln.red_flags)}")

if __name__ == "__main__":
    main()