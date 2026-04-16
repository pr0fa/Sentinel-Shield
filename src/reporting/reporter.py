import json

class Reporter:
    def __init__(self, use_colour: bool = True):
        self._use_colour = use_colour

    def print_report(self, complexity, scan, tdi) -> None:
        print(f"--- SentinelShield Report ---")
        print(f"File: {tdi.filepath} | Score: {tdi.tdi} | Risk: {tdi.risk_level}")

    def to_json(self, results) -> str:
        return json.dumps([{"file": r[2].filepath, "tdi": r[2].tdi} for r in results], indent=2)