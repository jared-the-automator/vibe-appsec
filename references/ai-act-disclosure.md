# VA-08 — AI content disclosure (EU AI Act, Art. 50)

## Failure mode

The app includes a system that **interacts directly with natural persons** —
a chatbot, voice agent, AI-generated content presented as human-made — but
never tells the other side it's a machine. For EU-facing products this is a
hard transparency obligation under the EU AI Act (Regulation (EU) 2024/1689) [15],
Article 50 [19], with enforcement ramping in through 2026–2027.

Vibe-coded products hit this often: the LLM chat UI ships "just works," and
nobody adds the disclosure because the model never flagged it.

## Detection

- Does the app have any user-facing LLM interaction (chat, voice, avatar)?
- Is there a visible, pre-interaction disclosure ("you are talking to an AI
  assistant") — not buried in ToS only?
- If the app generates synthetic content (images/text/audio/video that users
  can mistake for human-made): is there a metadata/watermark/labeling
  mechanism per Art. 50(2)?

## Control

- Pre-interaction disclosure: clear, at the point of first contact, in the
  UI (not only in ToS/privacy).
- For generated content: machine-readable marking of synthetic output
  (provider-level content credentials where available — e.g., C2PA — or
  platform labeling).
- Keep the legal assessment documented: which AI Act obligations apply to
  which component (transparency is the one most AI-generated apps trip on).

## Grounding (fetched 2026-09-22, see evidence/ledger.json)

[15] Regulation (EU) 2024/1689 (EU AI Act), EUR-Lex — the Act's structure
includes "transparency obligations for certain AI systems."

[19] Article 50 as published on the AI Act Explorer (mirror of EUR-Lex):
> "Providers shall ensure that AI systems intended to interact directly with natural persons are designed and developed in such a way that the natural persons concerned are informed that they are interacting with an AI system"

(Check EUR-Lex [15] for the authoritative text and its enforcement timeline;
the mirror [19] is for quick reference.)

## Sources

[15] https://eur-lex.europa.eu/eli/reg/2024/1689/oj — EU AI Act Regulation 2024/1689
[19] https://artificialintelligenceact.eu/article/50 — EU AI Act Article 50 (AI Act Explorer mirror)
