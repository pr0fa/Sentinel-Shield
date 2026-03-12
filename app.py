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