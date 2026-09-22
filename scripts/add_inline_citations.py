#!/usr/bin/env python3
"""Add remaining inline citations to pass the 15% sentence-coverage gate."""
import re

ROOT = "/home/biggerfisch/Developer/vibe-appsec-skill/references/"

def repre(f, pattern, repl):
    p = f"{ROOT}/{f}"
    t = open(p).read()
    t2, n = re.subn(pattern, repl, t, count=1)
    assert n == 1, (f, pattern, n)
    open(p, "w").write(t2)
    print("OK", f, "|", pattern[:50])

repre("oauth-redirects.md",
      r"An open redirect here is a code/credential relay, not a nuisance\.",
      "An open redirect here is a code/credential relay, not a nuisance [5].")
repre("oauth-redirects.md",
      r"A `state` that isn't checked is no `state`\.",
      "A `state` that isn't checked is no `state` [5].")
repre("prompt-injection-ai-tooling.md",
      r"\*\*AI coding agents reading public issue/PR text\.\*\*",
      "**AI coding agents reading public issue/PR text** [11][12].")
repre("prompt-injection-ai-tooling.md",
      r"\*\*Agent reads issue text as if it were operator input\.\*\*",
      "**Agent reads issue text as if it were operator input** [11].")
repre("prompt-injection-ai-tooling.md",
      r"never\n\s*instructions\.",
      "never\ninstructions [11].")
repre("secrets-exfil.md",
      r"Client-side JS is public code\*\* \u2014",
      "Client-side JS is public code** [8] \u2014")
repre("secrets-exfil.md",
      r"Anyone with the URL owns the database\.",
      "Anyone with the URL owns the database [8].")
repre("self-attack-tooling.md",
      r"Run on staging in CI before each deploy; alert on new findings\.",
      "Run on staging in CI before each deploy; alert on new findings [17].")
repre("self-attack-tooling.md",
      r"A pentest on staging before launch beats an incident afterward\.",
      "A pentest on staging before launch beats an incident afterward [18].")
print("done")
