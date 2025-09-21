# Week 1 Plan — Foundations & Tooling

> Objective: Build theoretical grounding, complete targeted parsing/automata exercises, and stand up the tooling required for subsequent compiler projects.

## Weekly Outcomes
- Annotated summaries for Dragon Book Ch. 1-3 *or* Crafting Interpreters Part I.
- Completed regex→DFA + LL(1) table exercises checked into `01-foundations/exercises`.
- Lexer Playground prototype ready to iterate on (skeleton committed, basic token stream visualiser).
- Core dev environment configured with formatter, linter, build/test scripts recorded under `shared/tools`.
- Daily reflections appended to `docs/LEARNING_PATH.md` (end-of-day ritual).

## Daily Breakdown

### Day 1 — Kickoff & Baseline
- [ ] Read roadmap + learning path, set personal goals for the week (log in `docs/LEARNING_PATH.md`).
- [ ] Refresh math/data-structure fundamentals using preferred references; capture quick notes in `01-foundations/notes/basics.md`.
- [ ] Install/verify toolchains (Rust/C++/Python) and create a tooling backlog in `shared/tools/README.md`.
- [ ] Create template note files (`notes/templates`) and exercise scratchpads.

### Day 2 — Automata & Regular Languages
- [ ] Study regular languages + DFAs/NFAs (Dragon Book Ch. 2 or Stanford CS143 lecture 2).
- [ ] Derive regex→NFA→DFA for two sample grammars; store derivations in `01-foundations/exercises/regex-to-dfa.md`.
- [ ] Implement a small script/notebook that converts simple regexes to DFA transition tables (language of choice) inside `01-foundations/projects/lexer-playground/src`.
- [ ] Note key pitfalls/questions in `01-foundations/notes/automata.md`.

### Day 3 — Context-Free Grammars & Parsing Basics
- [ ] Read grammar + parsing theory (Dragon Book Ch. 3 §3.1–3.4 or Crafting Interpreters parsing chapters).
- [ ] Work through FIRST/FOLLOW derivations for arithmetic expressions; document in `01-foundations/exercises/ll1-practice.md`.
- [ ] Draft LL(1) parsing table for the toy grammar; add validation checklist in the same exercise file.
- [ ] Summarise insights plus remaining confusions in notes.

### Day 4 — Parser Implementations
- [ ] Implement a hand-written recursive-descent parser for the toy grammar inside `lexer-playground` (even without full evaluator yet).
- [ ] Compare with Pratt parsing approach (outline precedence table, optional quick prototype).
- [ ] Record comparison (pros/cons, error handling) in `projects/lexer-playground/docs/parser-comparison.md`.
- [ ] Add unit tests for parser snippets under `projects/lexer-playground/tests` (start with golden AST snapshots).

### Day 5 — Tooling & Automation
- [ ] Set up formatter/linter/test commands (e.g., `cargo fmt`, `clang-format`, `pytest`) and document usage in `shared/tools/README.md`.
- [ ] Create a common `Makefile` or task runner script scaffold in `shared/tools` (`build.sh`, `test.sh`).
- [ ] Wire basic CI checklist (manual for now) describing how to run lint/test for new projects.
- [ ] Review progress; update backlog of tooling gaps.

### Day 6 — Lexer Playground Milestone
- [ ] Flesh out token definitions, error handling, and CLI/REPL for the lexer playground.
- [ ] Generate sample token streams for JSON/math input; store fixtures under `docs/samples`.
- [ ] Add property-based or fuzz-style tests for token boundaries.
- [ ] Write a short retro covering design decisions and TODOs in `docs/changelog.md`.

### Day 7 — Consolidation & Reflection
- [ ] Revisit notes, clean up documentation, and tick off completed checkboxes.
- [ ] Run through all exercises/tests to ensure they pass after refactors.
- [ ] Draft Week 1 retrospective (what worked/blocked) in `docs/week-plans/week1-retro.md` (create file if absent).
- [ ] Prep Week 2 by outlining next-week goals in `docs/LEARNING_PATH.md` and backlog items in `02-basic-compilers`.

## Checkpoints & Metrics
- DFA and LL(1) exercises reviewed by midweek.
- Lexer Playground CLI runs end-to-end with at least two sample inputs by Day 6.
- Tooling scripts demonstrably run format + tests for the playground project.
- Retrospective + TODO backlog ready before starting Week 2.

## Stretch Goals
- Implement visual DFA/parse-tree renderers (graphviz or similar) and store outputs under `projects/lexer-playground/docs/visuals/`.
- Explore parser generators (ANTLR, Lark) and note differences vs manual approach.
- Begin drafting a glossary of compiler terminology in `docs/glossary.md`.

Stay disciplined with daily summaries; they compound your understanding and make debugging easier in future phases.
