# Syntax Analysis Deep Dive — Expressions, Derivations, and Grammar Hygiene

This appendix keeps concepts painfully simple, with examples that show why the classic E/T/F grammar exists and how we use it. 

## 1) The goal (what are we trying to do?)
- Give the parser rules that force the right grouping of tokens:
  - `*` happens before `+` (precedence)
  - parentheses override precedence
  - `+` and `*` chain left‑to‑right (associativity)

## 2) Rename the scary letters
- `E` = Expr (things with `+`)
- `T` = Term (things with `*`)
- `F` = Factor (a single number/identifier, or `( … )`)

LEGO analogy
- Factor = one brick (or a bundled mini‑model `( … )`).
- Term = bricks stuck with `*`.
- Expr = terms tied together with `+`.

## 3) The three rules in plain English
```
Expr   → Expr + Term | Term
Term   → Term * Factor | Factor
Factor → ( Expr ) | id
```
- Expr is either Expr + Term (keep adding) or just a Term (stop adding).
- Term is either Term * Factor (keep multiplying) or just a Factor (stop multiplying).
- Factor is either (Expr) (a bundled sub‑expr) or an id/number.

Why it works
- You can only make `+` while building an Expr.
- You can only make `*` while building a Term.
- Since Expr is built from Terms, all `*` groups are formed before we combine them with `+` → `*` has higher precedence.
- Left sides (`Expr → Expr + …`, `Term → Term * …`) make `+`/`*` left‑associative.

## 4) One slow example (watch grouping appear)
Target tokens: `id + id * id`

1) Build the Term on the right of `+` first (because `*` binds tighter):
```
Term → Term * Factor → Factor * Factor → id * id
```
2) Now make the Expr with the `+`:
```
Expr → Expr + Term
     → Term + (id * id)
     → Factor + (id * id)
     → id + (id * id)
```
AST shape:
```
      (+)
     /   \
   id     (*)
         /   \
       id     id
```

## 5) Derivations and parse trees (left‑most vs right‑most)
- Derivation = the sequence of rule applications that expands the start symbol into the input tokens.
- Left‑most derivation: always expand the left‑most nonterminal next (top‑down parsers mimic this).
- Right‑most derivation: expand the right‑most nonterminal (LR parsers mimic this in reverse, a.k.a. right‑most in reverse).
- Parse tree = a picture of one derivation: interior nodes are nonterminals; leaves, read left‑to‑right, are the original token sequence.
- AST vs parse tree: AST drops punctuation and compresses chains; operators/keywords become node types.

Side‑by‑side taste (grammar: left‑factored E/T/F form)
```
E  → T E'
E' → + T E' | ε
T  → F T'
T' → * F T' | ε
F  → ( E ) | id
```

Input: `id + id * id`

Left‑most derivation
```
E ⇒ T E'
  ⇒ F T' E'
  ⇒ id T' E'
  ⇒ id E'            (T' ⇒ ε)
  ⇒ id + T E'
  ⇒ id + F T' E'
  ⇒ id + id T' E'
  ⇒ id + id * F E'
  ⇒ id + id * id E'
  ⇒ id + id * id     (E' ⇒ ε)
```

Right‑most derivation (same input)
```
E ⇒ T E'
  ⇒ T                (E' ⇒ ε)
  ⇒ F T'
  ⇒ F * F T'
  ⇒ F * F            (T' ⇒ ε)
  ⇒ F * id
  ⇒ id * id
  ⇒ id + id * id     (by expanding E' earlier with +)
```
(Notice both end at the same string; the parse tree shape is the same.)

## 6) Grammar hygiene: remove left recursion (for LL/recursive‑descent)
Problem
```
E → E + T | T     # immediate left recursion (loops for LL)
```
Rewrite (standard transformation)
```
E  → T E'
E' → + T E' | ε
```
Explanation: build one `T`, then optionally repeat `(+ T)` as many times via `E'`.

Do the same for multiplication
```
T  → F T'
T' → * F T' | ε
F  → ( E ) | id
```

Walkthrough for `id + id * id`
```
E  ⇒ T E'
   ⇒ F T' E'                  (since T ⇒ F T')
   ⇒ id T' E'
   ⇒ id E'                    (T' ⇒ ε)
   ⇒ id + T E'                (E' ⇒ + T E')
   ⇒ id + F T' E'
   ⇒ id + id T' E'
   ⇒ id + id * F E'
   ⇒ id + id * id E'
   ⇒ id + id * id             (E' ⇒ ε)
```

## 7) Left factoring (make choices unambiguous for LL)
Problem: shared prefixes make predictive choice impossible
```
Stmt → if Expr then Stmt else Stmt
     | if Expr then Stmt
```
Factor the prefix `if Expr then Stmt`
```
Stmt  → if Expr then Stmt Stmt'
Stmt' → else Stmt | ε
```
Now the parser can decide using one token of lookahead.

Quick synthetic example
```
A → αβ | αγ | …   →   A  → α A'
                      A' → β | γ | …
```

## 8) What to infer when you see any production
- Left side = category you’re building (Expr, Term, Factor).
- Right side = how to build it (sequence of categories/tokens).
- `|` means “or”.
- Parentheses in the grammar are literal tokens only when quoted; otherwise grouping in the meta‑notation.

## 9) Tiny cheat card (carry this)
- E/T/F are just names (Expr/Term/Factor).
- Goal: rules that force the right grouping.
- Expr uses Term; Term uses Factor → `*` before `+`.
- Left recursion → left‑associative (rewrite for LL if needed).
- `( … )` comes from `Factor → ( Expr )`.

## 10) FAQ
- Why study CFGs at all?
  - They are the contract between tokens and trees. A clean grammar makes parsers and error messages predictable.
- Are ASTs binary trees?
  - No. Some nodes are binary (e.g., `Binary(+)`), many are n‑ary (blocks, param lists). Overall the AST is n‑ary.
- Do parentheses and keywords disappear?
  - Parentheses: the tree structure already encodes grouping. Keywords: they become node kinds (`IfNode`, `WhileNode`) instead of raw strings.

## 11) Practice prompts
- Derive `id + id + id` with both the left‑recursive and factored forms.
- Factor a grammar fragment with a common prefix and write the `A'` rules.
- Write recursive‑descent functions `parseExpr/parseTerm/parseFactor` and confirm they build the expected AST.

## 12) FIRST/FOLLOW & one LL(1) table cell (micro example)
Grammar (factored):
```
E  → T E'
E' → + T E' | ε
T  → F T'
T' → * F T' | ε
F  → ( E ) | id
```

FIRST sets (intuition):
- FIRST(F)  = { '(', id }
- FIRST(T)  = FIRST(F) = { '(', id }
- FIRST(T') = { '*', ε }
- FIRST(E)  = FIRST(T) = { '(', id }
- FIRST(E') = { '+', ε }

FOLLOW sets (partial):
- FOLLOW(E)  includes { ')', $ }
- FOLLOW(E') includes FOLLOW(E)
- FOLLOW(T)  includes FIRST(E') without ε → { '+', ')', $ }
- FOLLOW(T') includes FOLLOW(T)

LL(1) table cell example (row E', lookahead '+'):
- Lookahead `+` is in FIRST(`+ T E'`) → choose `E' → + T E'`.
- If lookahead is in FOLLOW(E') (e.g., `)` or end), choose `E' → ε`.

Why this matters: factoring plus disjoint FIRST/FOLLOW lets a predictive parser decide with one token of lookahead.
