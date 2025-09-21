# Exercise: LL(1) Practice

Derive FIRST/FOLLOW sets and LL(1) parsing tables for the sample grammars below. Highlight conflicts and propose fixes.

## Grammar 1 — Expression Core
```
E  -> T E'
E' -> + T E' | ε
T  -> F T'
T' -> * F T' | ε
F  -> ( E ) | id
```
- Compute FIRST/FOLLOW for each non-terminal.
- Build the parsing table; verify there are no conflicts.
- Test the table manually on inputs: `id + id * id`, `( id + id ) * id`.

## Grammar 2 — If/Else Ambiguity
```
S -> if E then S else S | if E then S | stmt
```
- Show why this grammar is not LL(1).
- Transform it to an LL(1)-friendly version (introduce explicit `if` constructs or tokens) and redo the table.

## Grammar 3 — Function Declarations
```
P -> func id ( Params ) Block
Params -> id ParamTail | ε
ParamTail -> , id ParamTail | ε
Block -> { Stmts }
Stmts -> Stmt Stmts | ε
```
- Analyse FIRST/FOLLOW.
- Build the LL(1) table and test on multiple inputs (with/without params).

## Reflection
- Document any conflicts encountered and resolution strategies (left factoring, left recursion elimination).
- Note where an LR approach might be more suitable and why.

Store worked tables and derivations here; keep accompanying parser implementations in the project directory.
