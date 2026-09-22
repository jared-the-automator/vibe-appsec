# VA-03 — Cloudflare origin exposure

## Failure mode

Apps behind Cloudflare with the origin server still listening on a public IP.
The proxy hides you from *casual* access, but anyone who learns the origin IP [7]
(can be in old DNS records, error logs, or BGP) reaches the app **completely
bypassing the WAF, rate limits, and bot protection** — the exact controls the
agent that built the app probably added via Cloudflare rather than in the
app itself.

## Detection

1. Identify whether the site is fronted by Cloudflare:
   ```bash
   dig +short <domain>          # Cloudflare front → 104.16.x / 108.162.x / 172.64-71.x
   ```
2. Find candidate origin IPs (prior DNS, DNS-over-Time-style leaks, error
   pages in old logs, `server` headers from the API edge).
3. Test each candidate:
   ```bash
   curl -I --max-time 5 http://<candidate-ip>:443 -H "Host: <domain>"
   ```
   If the origin serves the app (or 403s with the app's error page), it's
   exposed.
4. Check the origin firewall: only Cloudflare's current IP ranges should be
   accepted on 80/443.

## Control

- Restrict the origin firewall (security group / `ufw` / `iptables`) to
  Cloudflare's published ranges only.
- Rotate the origin IP if it's ever been publicly served.
- Keep the origin out of DNS; use private DNS or a non-guessable address [7].

## Grounding (fetched 2026-09-22, see evidence/ledger.json)

[7] Cloudflare, "Known IP address ranges":
> "You can also use the Cloudflare API to access this list"

(Practical control: the firewall allow-list is derived from exactly this
list — fetch it at deploy time, don't hardcode stale ranges.)

## Fix recipe

```bash
# fetch current CF ranges, then rebuild the allow-list at deploy time:
curl -s https://www.cloudflare.com/ips-v4 -o /tmp/cf_v4.txt
curl -s https://www.cloudflare.com/ips-v6 -o /tmp/cf_v6.txt

# ufw example:
ufw delete allow 80/tcp; ufw delete allow 443/tcp
while read -r cidr; do ufw allow from "$cidr" to any port 80,443 proto tcp; done < /tmp/cf_v4.txt
```

## Sources

[7] https://www.cloudflare.com/ips — Cloudflare current IP ranges
