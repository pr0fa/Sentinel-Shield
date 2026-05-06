import sys
import os
import uuid
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from src.scanner import Scanner

app = Flask(__name__, template_folder="web/templates", static_folder="web/static")
app.secret_key = "sentinelshield-dev-key"
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024  # 1 MB cap 

@app.template_filter("time_ago")
def time_ago_filter(dt):
    diff = datetime.now() - dt
    s = int(diff.total_seconds())
    if s < 60: return f"{s}s ago"
    if s < 3600: return f"{s // 60}m ago"
    if s < 86400: return f"{s // 3600}h ago"
    return f"{s // 86400}d ago"

ALLOWED_EXTENSIONS = {".py"}
_scan_store = {}
_scanner = Scanner()

@app.route("/")
def dashboard():
    results = sorted(_scan_store.values(), key=lambda r: r["scanned_at"], reverse=True)
    return render_template("dashboard.html", results=results, active="dashboard")

def _security_score(scan_result):
    by_sev = lambda s: [f for f in scan_result.red_flags if f.severity == s]
    critical = len(by_sev("CRITICAL"))
    high     = len(by_sev("HIGH"))
    medium   = len(by_sev("MEDIUM"))
    low      = len(by_sev("LOW"))
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
        if os.path.splitext(f.filename)[1].lower() not in ALLOWED_EXTENSIONS:
            flash(f"Rejected '{f.filename}', only .py files are allowed.", "error")
            continue
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

@app.route("/reports")
def reports():
    results = sorted(_scan_store.values(), key=lambda r: r["scanned_at"], reverse=True)
    return render_template("reports.html", results=results, active="reports")

@app.route("/settings")
def settings():
    return render_template("settings.html", active="settings")

@app.errorhandler(413)
def too_large(e):
    flash("File too large, maximum upload size is 1 MB.", "error")
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=False, port=5000)