# Phase 02 — Basic Compilers

Focus: ship an end-to-end compiler for a small language. Emphasis on parsing, AST building, semantic checks, and bytecode/runtime design.

## Objectives
- Implement full lexical + syntactic analysis for expression-oriented languages.
- Build semantic analysis: symbol tables, scope rules, type checking basics.
- Emit bytecode or direct evaluation structures; create a simple VM or interpreter.
- Establish testing discipline (unit + integration) and CI-ready scripts.

## Core Project — Tiny Arithmetic Compiler
Target: compile a small arithmetic language with variables and functions to a stack-machine bytecode.

Suggested pipeline:
1. Lexer + Pratt parser for precedence climbing.
2. AST validation, constant folding, and symbol resolution.
3. Bytecode generation and stack-machine runtime implementation.
4. CLI driver with REPL and file compilation modes.
5. Unit + regression suites plus benchmarks.

## Additional Experiments
- Try recursive descent vs parser generator approaches.
- Explore error reporting UX (highlight spans, suggestions).
- Add intermediate representation dumps to inspect pipeline stages.

Progress to Phase 03 once you can extend this compiler confidently.
