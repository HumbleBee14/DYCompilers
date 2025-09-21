# Minerva Language Compiler

> Goal: build a statically-typed language with modules, compile to a mid-level IR, and run on a custom VM or LLVM.

## Roadmap
1. **Specification** — Define syntax, typing rules, and evaluation model (`docs/spec.md`).
2. **Front-end** — Implement lexer, parser, and type checker with rich diagnostics.
3. **IR Design** — Create a three-address or SSA-lite IR with CFG representation.
4. **Optimisations** — Ship data-flow analyses (dominators, liveness) and passes (CSE, DCE, simplification).
5. **Backend** — Lower IR to bytecode or LLVM IR; integrate register allocation if needed.
6. **Tooling** — Provide CLI, REPL, and debugger hooks.
7. **Testing** — Extend unit/property tests and differential tests against interpreters.

## Research Hooks
- Explore algebraic effect handlers or pattern matching compilation strategies.
- Prototype incremental compilation or caching.
- Investigate IR verification and invariants checks.

Document each milestone in `docs/` and keep the change history transparent.
