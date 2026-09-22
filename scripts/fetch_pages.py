#!/usr/bin/env python3
"""Fetch each verified source page to evidence/pages/ for verbatim quoting."""
import json, os, re, ssl, time, urllib.request

PAGES = [
    ("3", "https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_Cheat_Sheet.html"),
    ("4", "https://datatracker.ietf.org/doc/html/rfc8725"),
    ("5", "https://datatracker.ietf.org/doc/html/rfc6749"),
    ("6", "https://datatracker.ietf.org/doc/html/rfc7519"),
    ("7", "https://www.cloudflare.com/ips/"),
    ("8", "https://github.com/gitleaks/gitleaks"),
    ("9", "https://github.com/advisories"),
    ("10", "https://docs.npmjs.com/cli/commands/npm-audit"),
    ("11", "https://embracethered.com/blog/posts/2025/github-copilot-remote-code-execution-via-prompt-injection/"),
    ("12", "https://nvd.nist.gov/vuln/detail/CVE-2025-53773"),
    ("13", "https://datatracker.ietf.org/doc/html/rfc7489"),
    ("14", "https://github.com/papra-hq/papra/security/advisories/GHSA-6f8x-2rc9-vgh4"),
    ("15", "https://eur-lex.europa.eu/eli/reg/2024/1689/oj"),
    ("16", "https://owasp.org/www-community/attacks/Credential_stuffing"),
    ("17", "https://www.zaproxy.org/"),
    ("18", "https://portswigger.net/burp"),
]

outdir = "/home/biggerfisch/Developer/vibe-appsec-skill/evidence/pages"
os.makedirs(outdir, exist_ok=True)

def html_to_text(html):
    html = re.sub(r"<script.*?</script>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<style.*?</style>", " ", html, flags=re.S | re.I)
    html = re.sub(r"</(p|div|li|h[1-6]|tr|pre)>", "\n", html, flags=re.I)
    html = re.sub(r"<br\s*/?>", "\n", html, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", html)
    import html as htmlmod
    text = htmlmod.unescape(text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)
    return text

for lid, url in PAGES:
    out = f"{outdir}/{lid}.txt"
    if os.path.exists(out) and os.path.getsize(out) > 500:
        print(f"skip {lid} (cached)")
        continue
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36"})
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
            body = r.read(400000).decode("utf-8", "replace")
        text = html_to_text(body)
        with open(out, "w") as f:
            f.write(text)
        print(f"ok   {lid} {url} -> {len(text)} chars")
    except Exception as e:
        print(f"FAIL {lid} {url}  {str(e)[:150]}")
    time.sleep(1)
