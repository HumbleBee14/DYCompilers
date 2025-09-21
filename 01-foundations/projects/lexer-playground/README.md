# Lexer Playground

> Goal: compare regex-driven and manual lexers, visualise tokens, and record trade-offs.

## Suggested Milestones
1. Define tiny grammars (math expressions, JSON fragments) in `docs/grammar.md`.
2. Implement two lexer variants in `src/` (regex + state machine).
3. Create visualisation scripts (graphs, tables) and store outputs in `docs/`.
4. Add property-based tests for token coverage under `tests/`.

## Stretch Ideas
- Benchmark throughput across lexer variants.
- Extend to parser prototypes (LL vs Pratt) for select grammars.
- Experiment with Unicode and error recovery strategies.

Document learnings and gotchas as you go.
