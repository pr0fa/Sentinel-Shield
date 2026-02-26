import re
from typing import List, Dict, Any

_RAW_RULES: List[Dict[str, Any]] = [
    {
        "id": "HC001",
        "name": "Hardcoded Password",
        "pattern": r'(?i)(password|passwd|pwd)\s*=\s*["\'][^"\']{1,}["\']',
        "severity": "HIGH",
        "category": "Hardcoded Credentials",
        "rationale": "Hardcoded passwords can be extracted by anyone with read access.",
    },
    {
        "id": "SQL001",
        "name": "SQL Injection – %-format",
        "pattern": r'\.execute\s*\(\s*["\'].*%[sd]',
        "severity": "HIGH",
        "category": "SQL Injection",
        "rationale": "String-formatting SQL enables SQL injection.",
    },
]

SECURITY_RULES = _RAW_RULES # Simplified for this commit