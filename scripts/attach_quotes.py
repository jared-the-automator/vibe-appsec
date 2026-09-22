#!/usr/bin/env python3
"""Attach verbatim evidence quotes to ledger sources (mechanically verified)."""
import re, subprocess

S = "/home/biggerfisch/.hermes/skills/research/grounded-citations/scripts/sources.py"
ENV = "HERMES_CITATION_LEDGER=/home/biggerfisch/Developer/vibe-appsec-skill/evidence/ledger.json"
PAGES = "/home/biggerfisch/Developer/vibe-appsec-skill/evidence/pages/"

def q(lid, text, page):
    r = subprocess.run(
        f'{ENV} python3 {S} quote {lid} --text {subprocess.list2cmdline([text])} --from {PAGES}{page}',
        shell=True, executable="/bin/bash", capture_output=True, text=True)
    ok = r.returncode == 0
    print(f"{'OK  ' if ok else 'FAIL'} [{lid}] {text[:55]}...  {'' if ok else (r.stdout+r.stderr).strip()[:200]}")
    return ok

results = []
results.append(q(3, "to accept unsecured JWTs by default (\"alg\":\"none\"). In this case, an attacker would be able to forge their own JWTs", "3.txt"))
results.append(q(3, "It must not rely on the information of the JWT header to select the verification algorithm", "3.txt"))
results.append(q(4, "The algorithm can be changed to \"none\" by an attacker, and some libraries would trust this value and \"validate\" the JWT without checking any signature", "4.txt"))
results.append(q(4, "An \"RS256\" (RSA, 2048 bit) parameter value can be changed into \"HS256\" (HMAC, SHA-256), and some libraries would try to validate the signature using HMAC-SHA256 and using the RSA public key as the HMAC", "4.txt"))
results.append(q(5, "the authorization server MUST ensure that the redirection URI used to obtain the authorization code is identical to the redirection URI provided when exchanging the authorization code for an access token", "5.txt"))
results.append(q(5, "The client MUST implement CSRF protection for its redirection URI", "5.txt"))
results.append(q(5, "The client SHOULD utilize the \"state\" request parameter to deliver this value to the authorization server when making an authorization request", "5.txt"))
results.append(q(5, "the authorization server MUST validate it against the registered value", "5.txt"))
results.append(q(7, "You can also use the Cloudflare API to access this list", "7.txt"))
results.append(q(8, "Find secrets with Gitleaks", "8.txt"))
results.append(q(9, "Security vulnerability database inclusive of CVEs and GitHub originated security advisories from the world of open source software", "9.txt"))
results.append(q(11, "This post is about an important, but also scary, prompt injection discovery that leads to full system compromise of the developer\u2019s machine in GitHub Copilot and VS Code", "11.txt"))
results.append(q(12, "Improper neutralization of special elements used in a command ('command injection') in GitHub Copilot and Visual Studio allows an unauthorized attacker to execute code locally.", "12_nvd_api.json"))
results.append(q(14, "phishing emails crafted using this vulnerability will pass SPF, DKIM, and DMARC checks and appear completely authentic to email security filters and recipients", "14.txt"))
results.append(q(15, "transparency obligations for certain AI systems", "15.txt"))
results.append(q(15, "Providers shall ensure that AI systems intended to interact directly with natural persons are designed and developed in such a way that the natural persons concerned are informed that they are interacting with an AI system", "15b_ai_act_a50.txt"))
results.append(q(19, "Providers shall ensure that AI systems intended to interact directly with natural persons are designed and developed in such a way that the natural persons concerned are informed that they are interacting with an AI system", "15b_ai_act_a50.txt"))
results.append(q(20, "a critical vulnerability in GitHub Copilot Chat (CVSS 9.6) that allowed silent exfiltration of secrets and source code from private repos", "12c_camoleak.txt"))

print(f"\n{sum(results)}/{len(results)} quotes attached")
