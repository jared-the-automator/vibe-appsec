---
name: vibe-appsec
description: "Use when hardening AI-generated (vibe-coded) apps for production. Ten grounded rules: JWT, OAuth, origin leak, secrets, supply chain, prompt injection, email spoofing, AI Act, stuffing, self-scanning."
version: 1.0.0
author: Jared Fischer
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Security, Application Security, AI-Generated Code, Hardening, OWASP]
    category: security
    related_skills: [grounded-citations, web-pentest]
---

# vibe-appsec

Security hardening skill for AI-generated applications. LLMs consistently ship a
narrow set of specific failures — this skill encodes those failures, their
grounded controls, and a check loop an agent can run on any codebase before
production.

**Grounding rule:** every rule cites a primary source (OWASP cheat sheet, IETF
RFC, NVD entry, or published vendor advisory) with verbatim quotes in
`references/<rule>.md`. Do not introduce control numbers, CVE IDs, or CVE
scores from memory. If a source cannot be fetched, the claim is not in this
skill. The citation ledger and evidence snapshots are in `evidence/`.

## When to load

- About to deploy an app whose code was substantially AI-generated
- Asked to "harden for production", "pre-launch security review", or "vibe-appsec check"
- Reviewing AI-generated authentication, email, dependency, or AI-tooling code

## The check loop

Run against the target codebase in order. For each rule: **detect → cite → fix → re-scan**.

1. **Detect** — apply the rule's grep/signals section to the repo.
2. **Cite** — open the matching `references/<rule>.md`; every finding you report
   must name the rule and its primary source. No unsourced findings, no
   "best practice" hand-waving.
3. **Fix** — apply the rule's control. For fixes you are not certain about
   (protocol behavior, library defaults), verify against the cited source text
   first; do not guess.
4. **Re-scan** — re-run detection; the rule passes only when the signal is
   gone, not when a patch was applied.

Report format: one line per finding — `rule-id | file:line | signal | control
applied | source`. End with a summary table of rules passed / failed / n/a.

## The ten rules

| ID | Rule | One-line detection signal | Reference |
|---|---|---|---|
| VA-01 | JWT algorithm pinning | JWT parser without an explicit allow-listed algorithm [3] | `references/jwt-algorithms.md` |
| VA-02 | OAuth redirect + state | OAuth flow with unregistered `redirect_uri` or no `state` [5] | `references/oauth-redirects.md` |
| VA-03 | Origin IP exposure | Cloudflare-fronted origin listening on a public IP / firewall not restricted to CF ranges [7] | `references/cf-origin-leak.md` |
| VA-04 | Secrets hygiene | API keys in client bundle, static long-lived creds, no rotation story [8] | `references/secrets-exfil.md` |
| VA-05 | Dependency supply chain | `postinstall`/`preinstall` scripts, missing lockfile, un-audited deps [9] | `references/npm-supply-chain.md` |
| VA-06 | AI tooling prompt injection | Untrusted text (issues/PRs/deps) feeding an agent that can write files or run commands [11] | `references/prompt-injection-ai-tooling.md` |
| VA-07 | Email HTML injection | User-controlled values interpolated into transactional email HTML [14] | `references/email-spoofing-html.md` |
| VA-08 | AI content disclosure | AI system interacting directly with users without informing them [19] | `references/ai-act-disclosure.md` |
| VA-09 | Credential stuffing defense | Login endpoint without rate limiting / 2FA / anomaly handling [16] | `references/credential-stuffing.md` |
| VA-10 | Self-attack tooling | No automated scan (ZAP/Burp/semgrep) in the pre-deploy path [17] | `references/self-attack-tooling.md` |

## Pitfalls

- **Do not paste framework control numbers from memory.** Cite the reference
  file's source; the numbers are there and were fetched, not recalled.
- **CVSS scores move.** Report scores as "per <source>, <date>" or omit
  them; never state a score as a stable fact. [12]
- **Fixing is not passing.** A rule passes only after the re-scan shows the
  signal gone. Report "patched, re-scan pending" honestly when you stop short.
- **Platform subdomains are not findings.** `.mn.co`, `.linktr.ee`, `.vercel.app`
  et al. are hosting platforms — note the platform, don't flag the subdomain.
- **The skill is a checklist, not a pentest.** For real threat modeling or
  offensive validation, use a dedicated pentest workflow (e.g. `web-pentest`).

## Why these ten (grounding)

The rule set is the intersection of what AI-generated apps demonstrably ship
and what primary sources document as exploitable:

- JWT `alg:none` and key-confusion forgeries are documented attack classes in
  the OWASP JWT Cheat Sheet [3], and "Unsecured JWT" is the norm this skill
  defends against per RFC 7519 [6].
- OAuth open redirects and missing `state` (login CSRF) are defined in
  RFC 6749 [5].
- Cloudflare's own docs state that traffic not from Cloudflare ranges should
  not reach the origin [7].
- Secret leakage in client code is the class gitleaks targets [8].
- `npm audit` is the standard dependency-vulnerability step in the npm
  toolchain [9].
- Prompt injection into AI coding tooling produced multiple critical
  2025 advisories: CVE-2025-53773 (NVD) [12] and the CVSS 9.6 CamoLeak
  disclosure [20].
- Transactional-email HTML injection producing phishing that passes
  SPF/DKIM/DMARC is a documented 2025 advisory class [14], against a
  DMARC baseline defined in RFC 7489 [13].
- Undisclosed AI interaction with humans is a transparency obligation under
  EU AI Act Article 50 [19], enacted as Regulation (EU) 2024/1689 [15].
- Credential stuffing is listed among the most common account-takeover
  techniques by OWASP [16].
- Pre-deploy automated scanning is the core framing of ZAP [17] and Burp
  [18].

## Sources

[3] https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_Cheat_Sheet.html — OWASP JWT Cheat Sheet
[5] https://datatracker.ietf.org/doc/html/rfc6749 — RFC 6749 OAuth 2.0
[6] https://datatracker.ietf.org/doc/html/rfc7519 — RFC 7519 JWS
[7] https://www.cloudflare.com/ips — Cloudflare current IP ranges
[8] https://github.com/gitleaks/gitleaks — gitleaks
[9] https://github.com/advisories — GitHub Advisory Database
[11] https://embracethered.com/blog/posts/2025/github-copilot-remote-code-execution-via-prompt-injection — Embrace The Red: Copilot RCE via prompt injection
[12] https://nvd.nist.gov/vuln/detail/CVE-2025-53773 — NVD CVE-2025-53773
[13] https://datatracker.ietf.org/doc/html/rfc7489 — RFC 7489 DMARC
[14] https://github.com/papra-hq/papra/security/advisories/GHSA-6f8x-2rc9-vgh4 — GHSA-6f8x-2rc9-vgh4 email HTML injection
[15] https://eur-lex.europa.eu/eli/reg/2024/1689/oj — EU AI Act Regulation 2024/1689
[16] https://owasp.org/www-community/attacks/Credential_stuffing — OWASP credential stuffing
[17] https://www.zaproxy.org — OWASP ZAP
[18] https://portswigger.net/burp — Burp Suite
[19] https://artificialintelligenceact.eu/article/50 — EU AI Act Article 50 (AI Act Explorer mirror)
[20] https://www.legitsecurity.com/blog/camoleak-critical-github-copilot-vulnerability-leaks-private-source-code — Legit Security: CamoLeak disclosure
