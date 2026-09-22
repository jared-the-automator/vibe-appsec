# VA-04 — Secrets hygiene

## Failure mode

AI-generated apps ship secrets in the wrong places and with no lifecycle:

- **Default/hosted-service connection strings in the client bundle** —
  e.g. an Upstash/Redis/Neon connection string with the database password
  pasted into `NEXT_PUBLIC_*`, a config file in `src/`, or a `.env` that gets
  committed. Anyone can read the bundle and own the database [8].
- **Long-lived static credentials with no rotation story** — the key that
  "gets it working" is the key that lives forever, in code, in CI, in
  screenshots [8].
- **No scanner in the pipeline** — the leak is only found when it's in the
  public history [8].

## Detection

```bash
# 1. committed secrets: run gitleaks (the canonical tool for this):
npx gitleaks detect --no-banner --redact -v
# 2. PUBLIC_ env vars that are connection strings / keys:
grep -rnE "NEXT_PUBLIC_|REACT_APP_|VITE_" . --include="*.js" --include="*.ts" --include="*.tsx" \
  | grep -iE "key|token|secret|password|connectionstring|dsn"
# 3. .env files in git:
git log --all --diff-filter=A --name-only -- '*.env' | sort -u
# 4. hardcoded connection strings:
grep -rnE "redis://|mongodb(\+srv)?://|postgres://|mysql://|amqps?://" . \
  | grep -vE "process\.env|\$\{.*env|os\.environ|getenv"
```

Fail signals: any credential value in a file tracked by git [8]; any
`*_PUBLIC_*` variable whose name or value is a credential; connection
strings with literal passwords instead of `env()` lookups [8].

## Control

- All secrets from the environment: `process.env`, `os.environ`, platform
  secret stores — never literals [8].
- A public/client bundle variable must never contain a credential, a
  connection string, or an internal endpoint.
- gitleaks (or equivalent) in CI, **blocking** — a green build that contains
  a leaked secret is not green.
- Rotation story: short-lived credentials where the platform allows it
  (workload identity, short-TTL API keys); at minimum, a documented rotation
  runbook.
- Leaked = burned: on any commit of a secret, rotate it immediately; a
  `git filter-repo` rewrite does not un-leak it.

## Grounding (fetched 2026-09-22, see evidence/ledger.json)

[8] gitleaks (github.com/gitleaks/gitleaks):
> "Find secrets with Gitleaks"

The tool's own framing — it is the canonical detection step for this rule [8].
(gitleaks ships a default ruleset covering API keys, connection strings,
cloud creds; use it rather than hand-rolled regexes.)

## Sources

[8] https://github.com/gitleaks/gitleaks — gitleaks
