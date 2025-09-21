# Tiny Arithmetic Compiler

> Goal: compile arithmetic + control flow constructs to a stack-based bytecode VM within one month.

## Language Scope
- Expressions: +, -, *, /, power, comparisons.
- Statements: let-binding, conditional, while loop, function definitions.
- Types: integers, floats, booleans.
- Standard library: minimal math helpers (abs, pow).

## Implementation Checklist
- [ ] Grammar spec stored in `docs/grammar.md`.
- [ ] Pratt parser with precedence table defined in code and docs.
- [ ] Symbol table with lexical scope handling and type inference for simple constructs.
- [ ] Bytecode format documented in `docs/bytecode.md`.
- [ ] Stack-machine runtime with tracing / debug hooks.
- [ ] Test suites covering parser, semantic errors, runtime behaviour, and CLI UX.
- [ ] Benchmark scripts (micro + macro) and performance notes.

## Stretch Goals
- Add SSA-style IR as an optional lowering step.
- Experiment with basic optimisations (const folding, dead code elimination).
- Emit LLVM IR or WebAssembly as an alternate backend.

Keep a changelog in `docs/changelog.md` as you iterate.
