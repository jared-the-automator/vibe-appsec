# VA-02 — OAuth redirect URI + `state`

## Failure mode

AI-generated OAuth login flows routinely leave two holes open at once:

- **Open redirect** — the callback accepts `redirect_uri` values that weren't
  registered, so an attacker can bounce a code (or a user) to their own
  domain [5].
- **No `state`** — the authorization request carries no unguessable
  round-trip value, so a login CSRF attack (attacker forces a victim to
  complete the flow with the *attacker's* account) succeeds silently [5].

## Detection

```bash
# find the OAuth/SSO wiring, then inspect two things:
grep -rnE "authorization_url|authorize\?|redirect_uri|state=" \
  --include="*.py" --include="*.js" --include="*.ts" --include="*.go" .
```

Fail signals:
- `redirect_uri` compared against a user-supplied or templated value instead
  of the exact registered URI [5].
- No `state` parameter in the authorize URL; or `state` is not stored in the
  session before the redirect and checked on return [5].
- PKCE (`code_challenge`) absent for public clients.

## Control

- Register exactly the callback URIs you will use; compare against them
  strictly [5].
- Generate an unguessable `state` per authorization request, store it in the
  server session, and reject the callback on mismatch or absence [5].
- Use PKCE for public/mobile clients.

## Grounding (fetched 2026-09-22, see evidence/ledger.json)

[5] RFC 6749 (OAuth 2.0):
- §3.1.2.1, on the code being delivered to the redirection URI:
  > "the authorization server MUST ensure that the redirection URI used to obtain the authorization code is identical to the redirection URI provided when exchanging the authorization code for an access token"
- §4.1, redirect-URI validation:
  > "the authorization server MUST validate it against the registered value"
- §10.12 (login CSRF):
  > "The client SHOULD utilize the "state" request parameter to deliver this value to the authorization server when making an authorization request"
  > "The client MUST implement CSRF protection for its redirection URI"

## Fix recipe

```python
# BEFORE (vibe-coded):
url = f"{provider}/authorize?redirect_uri={redirect_uri}&scope=..."

# AFTER:
state = secrets.token_urlsafe(32)
session["oauth_state"] = state
url = (f"{provider}/authorize"
       f"?response_type=code"
       f"&client_id={CLIENT_ID}"
       f"&redirect_uri={REGISTERED_REDIRECT_URI}"   # literal, not user input
       f"&state={state}")

# callback:
if session.pop("oauth_state", None) != request.args["state"]:
    abort(400, "state mismatch")
```

## Sources

[5] https://datatracker.ietf.org/doc/html/rfc6749 — RFC 6749 OAuth 2.0
