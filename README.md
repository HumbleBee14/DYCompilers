# DYCompilers

A structured workspace for growing from compiler fundamentals to advanced ML compiler development. Each stage groups notes, exercises, and hands-on projects so you can progress quickly without losing track of assets or reusable tooling.

## Learning Phases
- `01-foundations` — math/CS refreshers, formal language theory, automata, data-structures, and first lexer/parser experiments
- `02-basic-compilers` — single-file compilers, expression evaluators, bytecode interpreters, and pipeline anatomy
- `03-intermediate-compilers` — typed languages, IR design, optimisations, register allocation, and simple VMs
- `04-advanced-compilers` — SSA-based optimisers, JITs, multi-pass backends, and language feature research
- `05-ml-compilers` — graph compilers, autodiff, MLIR/TVM pipelines, hardware acceleration, and model lowering
- `docs` — roadmap, study plans, and reference material that span every phase
- `shared` — reusable tooling, scripts, and project templates for consistent scaffolding

## Getting Started
1. Read `docs/ROADMAP.md` for the month-long journey and weekly milestones.
2. Follow `docs/LEARNING_PATH.md` to schedule study blocks and pick companion resources.
3. Start logging theory notes inside `01-foundations/notes` and tackle the exercises before moving onto projects.
4. Use the template in `shared/templates/compiler-project` when spinning up a new compiler project.

## Contributing Projects
- Place each new compiler under the phase that matches its scope and create a fresh folder using the template.
- Keep project documentation (design notes, decisions, benchmarks) inside its nested `docs/` directory.
- Share reusable components (lexers, IR utilities, testing harnesses) in `shared/tools` so future projects can reuse them.

Move forward phase by phase; once you are comfortable compiling traditional languages, the ML compiler track will feel natural.
