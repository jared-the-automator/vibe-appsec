# VA-07 — Email HTML injection (transactional email)

## Failure mode

Apps send transactional email (receipts, resets, alerts) through a provider
(Resend, SendGrid, Mailgun, Postmark, ...) with **user-controlled values
interpolated into HTML templates**. An attacker registers/acts with a crafted
name, order title, or address containing `<script>`/`<img>`/`<form>` and the
provider renders it inside an email **from your domain**.

Why this is severe: your domain's SPF/DKIM/DMARC are *correct* [13] — the mail is
genuinely yours — so the injected content "passes SPF, DKIM, and DMARC checks
and appears completely authentic to email security filters and recipients" [14].
The spoofing filter is the last line of defense users have; this attack walks
past it. Published 2025 advisories show this becoming a real phishing vector
rather than a theoretical one [14].

## Detection

```bash
# find template rendering with user data:
grep -rnE "resend\.send|sendgrid\.send|mailgun|postmark|nodemailer" \
  --include="*.js" --include="*.ts" --include="*.py" .
# then, for each template, check: is any user-supplied value inserted
# without escaping? (mustache {{ }} without {{#escape}}-style handling,
# f-string / .format() interpolation, raw HTML strings from requests)
```

Fail signals: user content in `html`/`text` fields of an email payload
without server-side escaping; client-side rendering of email HTML with
`dangerouslySetInnerHTML`-style injection; editable "custom fields" that feed
templates.

## Control

- **Escape all user values server-side** before template interpolation
  (HTML-escape `& < > " '` at minimum; `escape()`/`html.escape()`).
- Prefer **text-only** transactional email where design allows.
- If HTML is required, use the provider's **template/transactional-block
  model** where your layout is locked and user data is inserted as escaped
  variables — not free-form HTML from the client.
- Review every provider template for `{{ }}` variables sourced from request
  input.

## Grounding (fetched 2026-09-22, see evidence/ledger.json)

[14] Papra GHSA-6f8x-2rc9-vgh4 (email HTML injection advisory, 2025):
> "phishing emails crafted using this vulnerability will pass SPF, DKIM, and DMARC checks and appear completely authentic to email security filters and recipients"

[13] RFC 7489 (DMARC), §2.4 Anti-Phishing — the control this attack defeats:
> "DMARC is designed to prevent bad actors from sending mail that claims to come from legitimate senders, particularly senders of transactional email"
> "One of the primary uses of this kind of spoofed mail is phishing (enticing users to provide information by pretending to be the legitimate service requesting the information)"

The pairing is the point: authentication (SPF/DKIM/DMARC) protects against
*external* spoofing of your domain; HTML injection achieves the same effect
*from inside* your own sending infrastructure.

## Sources

[13] https://datatracker.ietf.org/doc/html/rfc7489 — RFC 7489 DMARC
[14] https://github.com/papra-hq/papra/security/advisories/GHSA-6f8x-2rc9-vgh4 — GHSA-6f8x-2rc9-vgh4 email HTML injection
