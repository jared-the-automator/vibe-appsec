# VA-09 — Credential stuffing defense

## Failure mode

Your login endpoint is the target, not the source: attackers run **breached
username/password pairs from other sites** against your app with automated
tools. If your app lets them log in at speed — no rate limit, no lockout, no
MFA, no anomaly signal — they convert every user who reused a password into
a takeover [16]. This is "one of the most common techniques used to take-over
user accounts" (OWASP [16]).

## Detection

```bash
# locate the auth endpoint(s):
grep -rnE "POST.*login|/signin|/auth|password" --include="*.js" --include="*.ts" --include="*.py" . \
  | grep -iE "router|app\.|route|@|handler"
```

Then verify, for each:
- **Rate limiting** on the endpoint (per IP *and* per account) — brute force
  needs volume; the limit kills the economics.
- **MFA/2FA offered** — the primary counter-measure per OWASP [16].
- **Account lockout or progressive delay** after repeated failures.
- **Anomaly signals** (new device/geo + password reset) wired to review, not
  silently ignored.

## Control

- Rate-limit login attempts (per IP, per account, per global); exponential
  backoff after failure.
- Offer MFA (TOTP/passkeys) to all users; require it for sensitive actions [16].
- Generic failure messages ("invalid credentials") — no user enumeration.
- Monitor login-success after many failures (the "one got through" event) —
  alert on it, don't just log it.

## Grounding (fetched 2026-09-22, see evidence/ledger.json)

[16] OWASP, "Credential stuffing":
> "Credential Stuffing typically refers to specifically using known (breached) username / password pairs against other websites"
> "The attacker uses automated tools to test the stolen credentials against many websites (for instance, social media sites, online marketplaces, or web apps)"
> "Multi-Factor Authentication being a primary counter-measure"

## Sources

[16] https://owasp.org/www-community/attacks/Credential_stuffing — OWASP credential stuffing
