#!/usr/bin/env python3
"""Attach the ZAP quote with the page's exact curly apostrophe."""
import subprocess, sys, os

S = "/home/biggerfisch/.hermes/skills/research/grounded-citations/scripts/sources.py"
LEDGER = "/home/biggerfisch/Developer/vibe-appsec-skill/evidence/ledger.json"
P = "/home/biggerfisch/Developer/vibe-appsec-skill/evidence/pages/"
env = dict(os.environ, HERMES_CITATION_LEDGER=LEDGER)

text = "Zed Attack Proxy (ZAP) by The world\u2019s most widely used web app scanner."
r = subprocess.run([sys.executable, S, "quote", "17", "--text", text, "--from", f"{P}17.txt"],
                   capture_output=True, text=True, env=env)
print(("OK  " if r.returncode == 0 else "FAIL"), (r.stdout + r.stderr).strip()[:200])
