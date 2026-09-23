# vibe-appsec

A portable security skill for AI coding agents that hardens **AI-generated
("vibe-coded") applications** before they meet real users.

Most AI coding agents can review code for security, but generic review misses
the *specific* things LLM-generated apps actually ship: JWTs that accept
`alg:none`, OAuth logins with open redirects, Cloudflare-fronted apps whose
origin IP leaked, default connection strings in production, dependencies that
phoned home with your env vars, transactional emails that render user input as
HTML. This skill exists to close that gap.

Every rule is **grounded in a primary source**, i.e. an OWASP cheat sheet, an IETF
RFC, a NVD CVE entry, or a published vendor advisory, with verbatim quotes in
`references/`. No control numbers from memory, no invented CVEs, no unsourced
statistics. If a claim can't be tied to a fetched source, it isn't in the skill.

## What it covers

The ten rules map the failure classes documented in primary sources:

- JWT `alg:none` and key-confusion forgeries — OWASP JWT Cheat Sheet [3],
  RFC 7519 [6].
- OAuth open redirects and missing `state` (login CSRF) — RFC 6749 [5].
- Cloudflare origin exposure — Cloudflare's documented IP-range contract [7].
- Secrets in client bundles and no rotation — gitleaks [8].
- Dependency supply-chain risk — npm audit [9].
- Prompt injection → RCE in AI coding tooling — CVE-2025-53773 [12],
  CamoLeak CVSS 9.6 [20].
- Transactional-email HTML injection that passes SPF/DKIM/DMARC —
  advisory class [14], DMARC baseline RFC 7489 [13].
- Undisclosed AI interaction — EU AI Act Article 50 [19],
  Regulation (EU) 2024/1689 [15].
- Credential stuffing — OWASP [16].
- No pre-deploy self-scanning — ZAP [17], Burp [18].

| Rule | The failure | Grounded in |
|---|---|---|
| `jwt-algorithms` | Tokens that accept `alg:none` / algorithm confusion | OWASP JWT Cheat Sheet [3], RFC 7519 [6] |
| `oauth-redirects` | OAuth logins with open redirects, missing `state` | RFC 6749 [5] |
| `cf-origin-leak` | Real server IP exposed, WAF bypassed | Cloudflare IP ranges [7] |
| `secrets-exfil` | API keys in client bundles, static creds, no rotation | gitleaks [8] |
| `npm-supply-chain` | Deps that exfiltrate env vars, no lockfile audit | npm audit [9] |
| `prompt-injection-ai-tooling` | RCE via prompt injection in AI coding assistants | CVE-2025-53773 (NVD) [12], CamoLeak [20] |
| `email-spoofing-html` | Phishing that passes SPF/DKIM/DMARC via HTML injection | RFC 7489 [13], email HTML injection advisory [14] |
| `ai-act-disclosure` | Undisclosed AI content under EU AI Act | Regulation (EU) 2024/1689 [15], Art. 50 [19] |
| `credential-stuffing` | Login endpoints with no bot/stuffing controls | OWASP credential stuffing [16] |
| `self-attack-tooling` | No automated self-scanning before launch | OWASP ZAP [17], Burp Suite [18] |

## Install

### Claude Code (native skill discovery)
```bash
git clone https://github.com/jared-the-automator/vibe-appsec-skill
mkdir -p ~/.claude/skills
cp -r vibe-appsec-skill ~/.claude/skills/
```

### Gemini CLI
```bash
cp -r vibe-appsec-skill ~/.gemini/skills/
```

### Cursor
```bash
cp -r vibe-appsec-skill/skill.md .cursor/rules/vibe-appsec.md
```

### Codex CLI / Kiro / any agent
Point the agent at `SKILL.md` in your project or user config; the `references/`
directory loads on demand.

## Use

Invoke it when you're about to ship AI-generated code, or ask the agent to
"harden this app for production" / "vibe-appsec review this repo". The skill
runs the check loop in `SKILL.md`: scan the codebase against the ten rules,
map findings to their grounded control, fix, re-scan.

## Provenance

This skill was distilled from a 316-post public security corpus (an active
creator's production-hardening content for vibe-coders) and every claim was
re-grounded to its primary source before inclusion. The creator's content is
**not** reproduced — only the underlying principles, each traced to
OWASP/IETF/NVD/vendor documentation. The citation ledger and verbatim evidence
snapshots live in `evidence/` for audit.

## Sources

[3] https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_Cheat_Sheet.html — OWASP JWT Cheat Sheet
[5] https://datatracker.ietf.org/doc/html/rfc6749 — RFC 6749 OAuth 2.0
[6] https://datatracker.ietf.org/doc/html/rfc7519 — RFC 7519 JWS
[7] https://www.cloudflare.com/ips — Cloudflare current IP ranges
[8] https://github.com/gitleaks/gitleaks — gitleaks
[9] https://github.com/advisories — GitHub Advisory Database
[12] https://nvd.nist.gov/vuln/detail/CVE-2025-53773 — NVD CVE-2025-53773
[13] https://datatracker.ietf.org/doc/html/rfc7489 — RFC 7489 DMARC
[14] https://github.com/papra-hq/papra/security/advisories/GHSA-6f8x-2rc9-vgh4 — GHSA-6f8x-2rc9-vgh4 email HTML injection
[15] https://eur-lex.europa.eu/eli/reg/2024/1689/oj — EU AI Act Regulation 2024/1689
[16] https://owasp.org/www-community/attacks/Credential_stuffing — OWASP credential stuffing
[17] https://www.zaproxy.org — OWASP ZAP
[18] https://portswigger.net/burp — Burp Suite
[19] https://artificialintelligenceact.eu/article/50 — EU AI Act Article 50 (AI Act Explorer mirror)
[20] https://www.legitsecurity.com/blog/camoleak-critical-github-copilot-vulnerability-leaks-private-source-code — Legit Security: CamoLeak disclosure
