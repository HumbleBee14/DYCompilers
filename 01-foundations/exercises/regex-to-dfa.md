# Exercise: Regex to DFA

Work through the conversion pipeline for a handful of small grammars. Show every intermediate step (regex → postfix → NFA → DFA → minimised DFA) and verify against sample strings.

## Prompt 1 — Arithmetic Tokens
- Regex: `[0-9]+(\.[0-9]+)?`
- Tasks:
  - Build Thompson NFA (sketch/or explain states).
  - Subset construction to DFA (provide transition table).
  - Minimise the DFA and highlight accepting states.
  - Validate against sample inputs (`42`, `13.37`, `09`).

## Prompt 2 — Identifiers
- Regex: `[A-Za-z_][A-Za-z0-9_]*`
- Repeat the pipeline; document ambiguities or pitfalls.

## Prompt 3 — Whitespace vs Comments
- Regex union: `(\s+)|(//.*)`
- Explore how to prioritise tokens in the final lexer.

## Reflection
- What patterns were hardest to convert and why?
- How would you automate this conversion in code?

Add automations/code snippets in `projects/lexer-playground/src` and link back here.
