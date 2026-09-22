#!/usr/bin/env python3
"""Attach final quotes (npm audit, RFC 7489, credential stuffing, ZAP, Burp)."""
import re, subprocess, sys, os

P = "/home/biggerfisch/Developer/vibe-appsec-skill/evidence/pages"
LEDGER = "/home/biggerfisch/Developer/vibe-appsec-skill/evidence/ledger.json"
S = "/home/biggerfisch/.hermes/skills/research/grounded-citations/scripts/sources.py"

# npm audit: normalize web_extract markdown into pages/10.txt
md = open("/home/biggerfisch/.hermes/cache/web/docs.npmjs.com-328d4ed379.md").read()
body = md.split("## See Also")[0]
body = body.replace("[... middle omitted — see footer ...]", " ")
body = body.replace("──────── [TRUNCATED] ────────", " ")
body = re.sub(r"^-{2,}.*$", "", body, flags=re.M)
body = re.sub(r"^Showing.*$", "", body, flags=re.M)
body = re.sub(r"^Full text saved.*$", "", body, flags=re.M)
body = re.sub(r"^read_file path.*$", "", body, flags=re.M)
body = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", body)
body = re.sub(r"\s+", " ", body)
open(f"{P}/10.txt", "w").write(body)
print(f"pages/10.txt: {len(body)} chars")

env = dict(os.environ, HERMES_CITATION_LEDGER=LEDGER)

def q(lid, text, page):
    r = subprocess.run([sys.executable, S, "quote", str(lid), "--text", text,
                        "--from", f"{P}/{page}"],
                       capture_output=True, text=True, env=env)
    print(("OK  " if r.returncode == 0 else "FAIL"), f"[{lid}]", text[:55],
          "" if r.returncode == 0 else (r.stdout + r.stderr).strip()[:150])
    return r.returncode == 0

res = []
res.append(q(10, "The audit command submits a description of the dependencies configured in your project to your default registry and asks for a report of known vulnerabilities", "10.txt"))
res.append(q(10, "By default, the audit command will exit with a non-zero code if any vulnerability is found", "10.txt"))
res.append(q(13, "DMARC is designed to prevent bad actors from sending mail that claims to come from legitimate senders, particularly senders of transactional email", "13.txt"))
res.append(q(13, "One of the primary uses of this kind of spoofed mail is phishing (enticing users to provide information by pretending to be the legitimate service requesting the information)", "13.txt"))
res.append(q(16, "Credential Stuffing typically refers to specifically using known (breached) username / password pairs against other websites", "16.txt"))
res.append(q(16, "The attacker uses automated tools to test the stolen credentials against many websites (for instance, social media sites, online marketplaces, or web apps)", "16.txt"))
res.append(q(16, "Multi-Factor Authentication being a primary counter-measure", "16.txt"))
res.append(q(17, "Zed Attack Proxy (ZAP) by The world's most widely used web app scanner", "17.txt"))
res.append(q(18, "The enterprise-enabled dynamic web vulnerability scanner", "18.txt"))

print(f"\n{sum(res)}/{len(res)} quotes attached")
