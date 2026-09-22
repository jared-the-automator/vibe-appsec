# VA-10 — Self-attack tooling in the pre-deploy path

## Failure mode

The app ships with only *passive* review (a human reading code, or an LLM
suggesting fixes). No tool actually **attacks the running app** before users
do. For AI-generated code this matters more, not less: the code is
unfamiliar to everyone, so the only reliable reviewer of its actual behavior
is an automated scanner pointed at a staging deployment [17].

## Detection

- Is there a pre-deploy step that scans the **running** app (DAST) or the
  code (SAST) — in CI, not as a one-off?
- Concretely: a ZAP/Burp/semgrep/Trivy step wired into the pipeline, failing
  the build (or at minimum alerting) on high-severity findings.

```bash
# what's actually in the pipeline?
grep -rnE "zaproxy|zap|burpsuite|semgrep|trivy|gitleaks|npm audit" \
  .github/ .gitlab-ci.yml Jenkinsfile *.yml 2>/dev/null || echo "NO SECURITY STEP IN PIPELINE"
```

## Control

- **ZAP (free, OSS)** for automated scanning: baseline + full scan in CI
  against staging. It's the "world's most widely used web app scanner" [17] and
  the natural first line because it costs nothing.
- **Burp Suite** where you need hands-on pentest depth (Pro: "the world's
  #1 web penetration testing toolkit" [18]; DAST edition for CI-driven scans [18]).
- **SAST/SCA layer** for code-level: semgrep (custom + community rules),
  gitleaks (secrets), `npm audit` (deps — see VA-05), Trivy (container images).
- Run the scan on every deploy to staging; treat high-severity as blocking [17].

## Grounding (fetched 2026-09-22, see evidence/ledger.json)

[17] OWASP ZAP (zaproxy.org) — automation framing [17]:
> "Zed Attack Proxy (ZAP) by The world’s most widely used web app scanner."
> "ZAP provides range of options for security automation."

[18] PortSwigger, Burp:
> "The enterprise-enabled dynamic web vulnerability scanner"
> "The world's #1 web penetration testing toolkit."

## Sources

[17] https://www.zaproxy.org — OWASP ZAP
[18] https://portswigger.net/burp — Burp Suite
