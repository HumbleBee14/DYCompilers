# Math & CS Baseline Notes

Use this file to capture quick refreshers on sets, functions, graphs, complexity, and data structures. Keep entries concise and link out to deeper resources when needed.

## Key Topics
- Sets & functions reminders
- Big-O / complexity checkpoints
- Graph terminology & traversal cheat sheet
- Data structure invariants worth revisiting

## Open Questions
- 
- 

## Follow-up Resources
- 
- 

## 2025-09-20 Session Notes
- Environment: Windows primary, with Rust, GCC/G++, and Python already installed; will keep scripts cross-platform (Windows/WSL/macOS).
- Compiler pipeline recap: lexing -> parsing -> semantic analysis -> IR -> optimisation -> codegen -> runtime, with Week 1 focused on the front-end stages.
- Tooling approach: maintain paired bash and PowerShell helpers; revisit for macOS/WSL compatibility when needed.

### Drill Reference
1. DFA determinism comes from having exactly one outgoing transition per symbol for each state; subset construction enforces this.
2. Average-case hash map insert is O(1) thanks to expected constant-time hashing and resizing strategies.
3. Real-world stack example: browser navigation history, undo/redo buffers, or pile of plates.

### Action Items
- Run shared build/test wrappers to confirm environment hooks.
- Start populating automata.md and exercise files after reviewing resources.

### Follow-up Questions
- None logged yet; capture any roadblocks from tooling setup or theory refresh.
