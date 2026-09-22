# VA-05 — npm / dependency supply chain

## Failure mode

AI agents add dependencies with no ownership of what they execute:

- **`preinstall`/`install`/`postinstall` scripts** run arbitrary code at
  install time — the classic npm supply-chain exfiltration vector (env vars,
  SSH keys, local files shipped home to an attacker) [9].
- **No lockfile / drifting versions** — the build that "works on my machine"
  installs a different (possibly compromised) package tree in CI.
- **No advisory check** — known-CVE dependencies shipped because the agent
  picked the name, not the risk [10].

## Detection

```bash
# 1. install scripts across the whole tree:
npm ls --all 2>/dev/null | awk '{print $1}' | sort -u | while read -r pkg; do
  node -e "const p=require('$pkg/package.json');
           if(p.scripts && (p.scripts.preinstall||p.scripts.install||p.scripts.postinstall))
             console.log('$pkg', JSON.stringify({pre:p.scripts.preinstall,post:p.scripts.postinstall}))" 2>/dev/null
done
# (in CI, use `npm ls --json` and filter `scripts` in code instead)

# 2. lockfile present and committed?
git ls-files | grep -E "package-lock.json|yarn.lock|pnpm-lock.yaml" || echo "NO LOCKFILE"

# 3. known-vulnerable dependencies:
npm audit --audit-level=high
```

Fail signals: any dependency (or transitive dep) with `preinstall`/`postinstall`
scripts you can't explain; missing lockfile; `npm audit` reporting high-or-
worse advisories.

## Control

- **Review every install-script package** in the tree. A dependency you can't
  explain, that runs code at install time, is blocked or replaced.
- Lockfile committed; CI installs from the lockfile only (`npm ci`).
- `npm audit` in CI, failing the build on high/critical [10].
- Prefer registries with signature verification where available
  (`npm audit signatures` verifies registry signatures of downloaded packages).
- Pin exact versions for anything security-relevant; no `*`/`^` on auth/crypto libs.

## Grounding (fetched 2026-09-22, see evidence/ledger.json)

[10] npm CLI docs, `npm audit`:
> "The audit command submits a description of the dependencies configured in your project to your default registry and asks for a report of known vulnerabilities"
> "By default, the audit command will exit with a non-zero code if any vulnerability is found"

[9] GitHub Advisory Database (github.com/advisories):
> "Security vulnerability database inclusive of CVEs and GitHub originated security advisories from the world of open source software"

(npm's registry advisory feed is cross-populated with this database — the
reason `npm audit` catches real CVEs, not just registry-side flags.)

## Sources

[9] https://github.com/advisories — GitHub Advisory Database
[10] https://docs.npmjs.com/cli/commands/npm-audit — npm audit docs
