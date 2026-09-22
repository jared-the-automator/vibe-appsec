#!/usr/bin/env python3
"""Verify candidate primary sources: check each URL exists (HTTP status) and
fetch a snippet of the title/body. Writes results to evidence/source_check.json."""
import json, re, urllib.request, ssl

CANDIDATES = {
  "jwt_algo": [
    "https://cheatsheetseries.owasp.org/cheatsheets/JSON_web_token_Cheat_Sheet.html",
    "https://auth0.com/blog/attack-of-the-week-algorithm-confusion-on-json-web-tokens/",
  ],
  "oauth_redirect": [
    "https://cheatsheetseries.owasp.org/cheatsheets/OAuth_2_0_Cheat_Sheet.html",
    "https://datatracker.ietf.org/doc/html/rfc6749",
  ],
  "cf_origin": [
    "https://developers.cloudflare.com/security/known-cloudflare-ips/",
  ],
  "secrets_exfil": [
    "https://github.com/gitleaks/gitleaks",
  ],
  "npm_supply": [
    "https://github.com/advisories",
    "https://docs.npmjs.com/cli/commands/npm-audit",
  ],
  "prompt_inject": [
    "https://embracethered.com/blog/posts/2025/github-copilot-remote-code-execution-via-prompt-injection/",
    "https://nvd.nist.gov/vuln/detail/CVE-2025-53773",
  ],
  "email_spoofing": [
    "https://datatracker.ietf.org/doc/html/rfc7489",
    "https://datatracker.ietf.org/doc/html/rfc4404",
  ],
  "ai_act": [
    "https://eur-lex.europa.eu/eli/reg/2024/1689/oj",
  ],
  "cred_stuffing": [
    "https://owasp.org/www-community/attacks/Credential_stuffing",
  ],
  "zscaler_appsec": [
    "https://www.zaproxy.org/",
    "https://portswigger.net/burp",
  ],
}

def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
    })
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
        body = r.read(60000).decode("utf-8", "replace")
        return r.status, r.geturl(), body

results = {}
for principle, urls in CANDIDATES.items():
    results[principle] = []
    for url in urls:
        try:
            status, final_url, body = fetch(url)
            m = re.search(r"<title[^>]*>([^<]{0,200})", body, re.I | re.S)
            title = re.sub(r"\s+", " ", m.group(1)).strip() if m else ""
            # first meaningful text paragraph
            text = re.sub(r"<script.*?</script>", " ", body, flags=re.S | re.I)
            text = re.sub(r"<style.*?</style>", " ", text, flags=re.S | re.I)
            text = re.sub(r"<[^>]+>", " ", text)
            text = re.sub(r"\s+", " ", text).strip()
            snippet = text[:400]
            results[principle].append({"url": url, "final": final_url, "status": status, "title": title, "snippet": snippet})
        except Exception as e:
            results[principle].append({"url": url, "error": str(e)[:300]})

with open("/home/biggerfisch/Developer/vibe-appsec-skill/evidence/source_check.json", "w") as f:
    json.dump(results, f, indent=2)

for p, items in results.items():
    for it in items:
        if "error" in it:
            print(f"FAIL {p} {it['url']}  {it['error'][:120]}")
        else:
            print(f"OK   {it['status']} {p} {it['url']}\n     title: {it['title'][:100]}")
