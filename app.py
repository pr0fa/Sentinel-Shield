import sys
import os
import uuid
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from src.scanner import Scanner

app = Flask(__name__)
app.secret_key = "sentinelshield-dev-key"

_scan_store = {}
_scanner = Scanner()

@app.route("/")
def dashboard():
    results = sorted(_scan_store.values(), key=lambda r: r["scanned_at"], reverse=True)
    return render_template("dashboard.html", results=results, active="dashboard")

def _security_score(scan_result):
    critical = len(scan_result.flags_by_severity("CRITICAL"))
    high     = len(scan_result.flags_by_severity("HIGH"))
    medium   = len(scan_result.flags_by_severity("MEDIUM"))
    low      = len(scan_result.flags_by_severity("LOW"))
    penalty  = critical * 10 + high * 5 + medium * 2 + low * 1
    score    = max(0, 100 - penalty)
    return {
        "score": score, "critical": critical, "high": high,
        "medium": medium, "low": low, "penalty": penalty,
        "formula": f"100 - ({critical}x10 + {high}x5 + {medium}x2 + {low}x1)"
    }

@app.route("/upload", methods=["POST"])
def upload():
    files = request.files.getlist("files")
    for f in files:
        if not f.filename: continue
        source = f.read().decode("utf-8", errors="replace")
        try:
            comp, scan, tdi = _scanner.scan_source(source, f.filename)
            file_id = str(uuid.uuid4())[:8]
            _scan_store[file_id] = {
                "id": file_id, "filename": f.filename, "source": source,
                "complexity": comp, "scan": scan, "tdi": tdi,
                "score": _security_score(scan), "scanned_at": datetime.now()
            }
        except SyntaxError: continue
    return redirect(url_for("dashboard"))

@app.route("/analysis/<file_id>")
def analysis(file_id):
    result = _scan_store.get(file_id)
    if not result: return redirect(url_for("dashboard"))
    return render_template("analysis.html", result=result, active="analysis")

if name == "main":
    app.run(debug=True, port=5000)