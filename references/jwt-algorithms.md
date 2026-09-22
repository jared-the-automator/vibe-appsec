# VA-01 — JWT algorithm pinning

## Failure mode

LLMs generate JWT parsing/issuance code that trusts the token header. Two
documented failure classes:

- **`alg: none` accepted by default** — older/naive libraries sign nothing [3];
  an attacker forges valid tokens for arbitrary identities [3].
- **Key type confusion (RS256 → HS256)** — the algorithm field is switched
  from RS256 to HS256; the library then signs/verifies with HMAC using the
  RSA *public* key (public in the JWKS) as the HMAC secret, so the attacker
  can forge signatures [4].

## Detection

```bash
# parsers without an explicit algorithm allow-list
grep -rnE "jwt\.(verify|decode)|jsonwebtoken\.verify|decode_jwt|JWT\.decode" \
  --include="*.js" --include="*.ts" --include="*.py" --include="*.go" .
# then, for each hit, check: is `algorithms:` / `algorithms=` / `allowed_algorithms`
# pinned to a specific list (e.g. ["RS256"]), NOT read from the token header?
```

Fail signals: algorithm list derived from the token's `header.alg`;
`verify` called without an algorithm argument; custom JWT parsing that
checks a signature "if present".

## Control

- Pin the accepted algorithm(s) at parse time, e.g. Node `jsonwebtoken`:
  `jwt.verify(token, key, { algorithms: ["RS256"] })`.
- Reject `none` explicitly; treat it as a 401, not a fallback.
- Never select the verification algorithm from untrusted input (the token
  header).

## Grounding (fetched 2026-09-22, see evidence/ledger.json)

- [3] OWASP JSON Web Token Cheat Sheet:
  > "Some JWT libraries, used to accept unsecured JWTs by default ( "alg":"none" ). In this case, an attacker would be able to forge their own JWTs"
  > "Make sure that "alg":"none" is not accepted by your JWT parser."
- [4] RFC 8725 (JWT Threats), §13:
  > "The algorithm can be changed to "none" by an attacker, and some libraries would trust this value and "validate" the JWT without checking any signature"
  > "An "RS256" (RSA, 2048 bit) parameter value can be changed into "HS256" (HMAC, SHA-256), and some libraries would try to validate the signature using HMAC-SHA256 and using the RSA public key as the HMAC"
- [6] RFC 7519 (JWS), §6 Unsecured JWT — the norm this rule defends:
  > "An Unsecured JWT is a JWS using the "alg" Header Parameter value "none" and with the empty string for its JWS Signature value"

## Fix recipes

- **Node (jsonwebtoken):** `jwt.verify(token, publicKey, { algorithms: ["RS256"] })`
- **Python (PyJWT):** `jwt.decode(token, key, algorithms=["RS256"])`
- **Go (golang-jwt):** `jwt.ParseWithClaims(token, claims, func(t *jwt.Token) (interface{}, error) { if _, ok := t.Method.(*jwt.SigningMethodRSA); !ok { return nil, fmt.Errorf(...) }; return key })`
- **Retrofit after the fact:** rotate the signing key; treat previously issued
  tokens as untrusted; audit issuance sites.

## Sources

[3] https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_Cheat_Sheet.html — OWASP JWT Cheat Sheet
[4] https://datatracker.ietf.org/doc/html/rfc8725 — RFC 8725 JWT Threats
[6] https://datatracker.ietf.org/doc/html/rfc7519 — RFC 7519 JWS
