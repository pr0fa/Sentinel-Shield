import sys
import json
from src.scanner import Scanner

def main():
    if len(sys.argv) < 2: return
    scanner = Scanner()
    with open(sys.argv[1], 'r') as f:
        comp, scan, tdi = scanner.scan_source(f.read(), sys.argv[1])
    if "--json" in sys.argv:
        print(json.dumps({"tdi": tdi.tdi, "risk": tdi.risk_level}))
    else:
        print(f"Final TDI: {tdi.tdi} ({tdi.risk_level})")

if __name__ == "__main__":
    main()