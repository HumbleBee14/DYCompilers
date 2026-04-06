# Chapter 1: Toy Language and AST — The Frontend

## What Are We Building?

The **frontend** of a compiler. This is the part that reads human-written text and converts it into a structured data format the rest of the compiler can work with.

```
Source text  →  [Lexer]  →  Token stream  →  [Parser]  →  AST
  (string)                   (flat list)                  (tree)
```

Three components, three files:

| File | Role | Java Analogy |
|------|------|-------------|
| `Lexer.h` | Characters → Tokens | `StreamTokenizer` / `Scanner` |
| `AST.h` | Defines tree node types | Class hierarchy for a data model |
| `Parser.h` | Tokens → AST | A hand-written deserializer that builds objects from text |

The driver (`toyc.cpp`) wires them together into an executable.

---

## Part 1: The Language Design

Before writing a compiler, you design what the language looks like. Every decision here affects the lexer and parser complexity.

The Toy language makes **deliberately simple** choices:

### One data type: `f64` (double)

- No `int`, `bool`, `string`. Everything is a 64-bit float.
- **Why?** Eliminates type checking complexity. The compiler never needs to ask "can I add an int to a float?"
- **Java comparison:** Imagine if Java only had `double`.

### Tensors up to rank 2

- Scalars (`42.0`), vectors (`[1, 2, 3]`), and matrices (`[[1, 2], [3, 4]]`). No higher.
- **Why?** Keeps the parser simple — you only need to handle `[` nesting 1-2 levels deep.
- Tensor shapes can be declared explicitly (`var b<2, 3> = ...`) or inferred from literals.

### Immutable values

- `var a = [1, 2, 3]` — once assigned, `a` never changes.
- **Why?** No need for mutation tracking, no aliasing problems, simpler memory model. Deallocation is automatic.

### Only two builtins: `transpose()` and `print()`

- Everything else is user-defined functions.
- **Why?** Enough to demonstrate the full compiler pipeline without drowning in standard library implementation.

### Generic functions with call-site specialization

- `def foo(a, b)` — parameters have no type annotations. The shapes get figured out when you call the function.
- This is actually sophisticated — similar to C++ templates or Java generics, but resolved differently.
- Each unique combination of argument shapes creates a new specialization (handled in Chapter 4).

### Example Toy program

```
# User defined generic function that operates on unknown shaped arguments.
def multiply_transpose(a, b) {
  return transpose(a) * transpose(b);
}

def main() {
  # Define a variable `a` with shape <2, 3>, initialized with the literal value.
  # The shape is inferred from the supplied literal.
  var a = [[1, 2, 3], [4, 5, 6]];

  # b is identical to a, the literal tensor is implicitly reshaped: defining new
  # variables is the way to reshape tensors (element count must match).
  var b<2, 3> = [1, 2, 3, 4, 5, 6];

  # This call will specialize `multiply_transpose` with <2, 3> for both
  # arguments and deduce a return type of <3, 2> in initialization of `c`.
  var c = multiply_transpose(a, b);
  var d = multiply_transpose(b, a);
  var e = multiply_transpose(c, d);

  # Calling with incompatible shapes (<2, 3> and <3, 2>) will trigger
  # a shape inference error (caught in later chapters, not Ch1).
  var f = multiply_transpose(a, c);
}
```

---

## Part 2: The Lexer — Turning Characters into Tokens

> Source file: `Ch1/include/toy/Lexer.h`

This is where the [02-lexical-analysis](../../../01-foundations/notes/02-lexical-analysis.md) notes come alive.

### The fundamental question

How do you go from a stream of characters to meaningful chunks?

```
"var a = [[1, 2], [3, 4]];"

becomes:

tok_var  tok_identifier("a")  '='  '['  '['  tok_number(1)  ','  tok_number(2)  ']'  ...  ';'
```

Recall the trio from lexical analysis theory:
- **Token:** the category label (e.g., `tok_identifier`, `tok_number`, `tok_var`)
- **Lexeme:** the exact characters that matched (e.g., `"a"`, `"3.14"`, `"var"`)
- **Pattern:** the rule that describes which lexemes belong to a token (e.g., `[a-zA-Z][a-zA-Z0-9_]*` for identifiers)

### The Token enum — the vocabulary of the language

```cpp
enum Token : int {
  // Single-char tokens ARE their ASCII value — brilliant trick
  tok_semicolon = ';',       // 59
  tok_parenthese_open = '(', // 40
  tok_parenthese_close = ')',
  tok_bracket_open = '{',
  tok_bracket_close = '}',
  tok_sbracket_open = '[',
  tok_sbracket_close = ']',

  // Multi-char and special tokens get negative values
  tok_eof = -1,
  tok_return = -2,    // keyword "return"
  tok_var = -3,       // keyword "var"
  tok_def = -4,       // keyword "def"
  tok_identifier = -5, // any name like "a", "foo", "transpose"
  tok_number = -6,     // any number like "3.14"
};
```

**Why this design?**

Single-character tokens like `(`, `)`, `{`, `[`, `+`, `*` use their ASCII code directly as the token value. Multi-character tokens (keywords, identifiers, numbers) get negative values to avoid collision.

When the parser sees token value `40`, it knows it's `(`. When it sees `-5`, it knows it's an identifier and calls `lexer.getId()` to get the actual name. No string comparisons at parse time — just integer checks. Fast.

Operators like `+`, `-`, `*` don't even get named enum entries — they're returned as their raw ASCII value. The parser checks `== '+'` directly.

### The Lexer class design

```cpp
class Lexer {
public:
  Token getCurToken();       // peek at current token
  Token getNextToken();      // advance and return next token
  void consume(Token tok);   // assert current == tok, then advance
  StringRef getId();         // get identifier string (when curTok == tok_identifier)
  double getValue();         // get number value (when curTok == tok_number)
  Location getLastLocation(); // where the current token started

private:
  virtual StringRef readNextLine() = 0;  // abstract — subclass provides input
  int getNextChar();                      // read one character
  Token getTok();                         // the core: read next token

  Token curTok;           // current token
  Location lastLocation;  // where curTok started
  std::string identifierStr; // filled when curTok == tok_identifier
  double numVal;          // filled when curTok == tok_number
  Token lastChar;         // one-character lookahead buffer
  int curLineNum, curCol; // position tracking
};
```

The Lexer is an **abstract base class**. `readNextLine()` is pure virtual — the subclass `LexerBuffer` provides input from a memory buffer. This separation means you could also write a `LexerStdin` for interactive input.

**Java analogy:** Think of `Lexer` as an abstract class with a `readLine()` method, and `LexerBuffer` as a concrete implementation backed by a `String`.

### The core algorithm — `getTok()`

This is the heart of every lexer. Located at `Lexer.h:127`:

```
1. Skip whitespace
2. Save current position (for error messages later)
3. Look at current character:
   - Letter?       → read full word → is it "return"/"def"/"var"?
                                        yes → return keyword token
                                        no  → return tok_identifier
   - Digit or '.'? → read full number → strtod() → return tok_number
   - '#'?          → skip to end of line (comment) → recurse to get next real token
   - EOF?          → return tok_eof
   - Anything else? → return the character itself as a token
```

In code:

```cpp
Token getTok() {
  // 1. Skip whitespace
  while (isspace(lastChar))
    lastChar = Token(getNextChar());

  // 2. Save location for diagnostics
  lastLocation.line = curLineNum;
  lastLocation.col = curCol;

  // 3a. Identifier or keyword: [a-zA-Z][a-zA-Z0-9_]*
  if (isalpha(lastChar)) {
    identifierStr = (char)lastChar;
    while (isalnum((lastChar = Token(getNextChar()))) || lastChar == '_')
      identifierStr += (char)lastChar;

    if (identifierStr == "return") return tok_return;
    if (identifierStr == "def")    return tok_def;
    if (identifierStr == "var")    return tok_var;
    return tok_identifier;
  }

  // 3b. Number: [0-9.]+
  if (isdigit(lastChar) || lastChar == '.') {
    std::string numStr;
    do {
      numStr += lastChar;
      lastChar = Token(getNextChar());
    } while (isdigit(lastChar) || lastChar == '.');
    numVal = strtod(numStr.c_str(), nullptr);
    return tok_number;
  }

  // 3c. Comment: # to end of line
  if (lastChar == '#') {
    do { lastChar = Token(getNextChar()); }
    while (lastChar != EOF && lastChar != '\n' && lastChar != '\r');
    if (lastChar != EOF) return getTok(); // recurse to skip comment
  }

  // 3d. EOF
  if (lastChar == EOF) return tok_eof;

  // 3e. Any other single character (operators, punctuation)
  Token thisChar = Token(lastChar);
  lastChar = Token(getNextChar());
  return thisChar;
}
```

### The lookahead pattern

```cpp
Token lastChar = Token(' ');
```

The lexer always holds one character it has already read but not yet processed. This is called **one-character lookahead**. Why? Because you can't know when a token ends until you see the character that *doesn't* belong to it.

Example — reading `var`:
```
lastChar = 'v' → is letter? start reading identifier
read 'a' → still letter, add to identifierStr
read 'r' → still letter, add to identifierStr
read ' ' → NOT a letter! Token is done. identifierStr = "var"
           But we already consumed ' '. Store it in lastChar for next getTok() call.
```

**Java analogy:** Same as `BufferedReader` with `mark()`/`reset()`, but more explicit. You always read one character ahead, then hold it for the next round.

### Location tracking

```cpp
struct Location {
  std::shared_ptr<std::string> file; // filename
  int line;                          // line number
  int col;                           // column number
};
```

Every token records where it came from (file, line, column). This seems like overhead now, but:
- Error messages need it: `"Parse error at ast.toy:5:25"`
- MLIR **requires** source locations on every operation (unlike LLVM IR where they're optional)
- This is a key MLIR philosophy — you should always be able to trace back to the source

### The `consume()` helper

```cpp
void consume(Token tok) {
  assert(tok == curTok && "consume Token mismatch expectation");
  getNextToken();
}
```

A convenience method the parser uses heavily. It says "I expect the current token to be X; if it is, advance; if not, crash (assertion failure)." This makes the parser code cleaner — instead of checking and advancing separately.

---

## Part 3: The AST — The Tree Structure

> Source file: `Ch1/include/toy/AST.h`

Once we have tokens, we need a **data structure** to represent the program's meaning. This is the AST — Abstract Syntax Tree.

### Why "abstract"?

Because it throws away syntax noise. The **parse tree** (concrete syntax tree) for `(a + b)` would include nodes for `(` and `)`. The **AST** just stores:
```
BinaryExprAST('+', a, b)
```
The parentheses did their job (grouping) and are gone. Semicolons, commas, `{` `}` — all syntax scaffolding — disappear from the AST. Only the **meaning** remains.

### The class hierarchy

```

ModuleAST                         ← "the whole program"
  └── vector<FunctionAST>         ← list of functions

FunctionAST                       ← one function definition
  ├── PrototypeAST                ← name + params: "def foo(a, b)"
  └── ExprASTList (body)          ← list of statements in { }

ExprAST (base class)              ← every expression node
  ├── NumberExprAST               ← 1.0, 42.0
  ├── LiteralExprAST              ← [[1, 2], [3, 4]]
  ├── VariableExprAST             ← reference to "a"
  ├── VarDeclExprAST              ← "var a<2,3> = ..."
  ├── BinaryExprAST               ← "a + b", "a * b"
  ├── CallExprAST                 ← "multiply_transpose(a, b)"
  ├── PrintExprAST                ← "print(x)"
  └── ReturnExprAST               ← "return expr"


======================================================


ModuleAST                         ← "the whole program" = list of functions
  └── vector<FunctionAST>

FunctionAST                       ← one function definition
  ├── PrototypeAST                ← name + params: "def foo(a, b)"
  │     ├── name: string
  │     └── args: vector<VariableExprAST>
  └── ExprASTList (body)          ← list of statements in { }

ExprAST (base class)              ← every expression/statement node
  ├── NumberExprAST               ← numeric literal: 1.0, 42.0
  ├── LiteralExprAST              ← tensor literal: [[1, 2], [3, 4]]
  │     ├── values: vector<ExprAST>   (nested numbers or literals)
  │     └── dims: vector<int64_t>     (shape, e.g., [2, 3])
  ├── VariableExprAST             ← variable reference: "a", "b"
  ├── VarDeclExprAST              ← variable declaration: "var a<2,3> = ..."
  │     ├── name: string
  │     ├── type: VarType (optional shape)
  │     └── initVal: ExprAST
  ├── BinaryExprAST               ← binary operation: "a + b", "a * b"
  │     ├── op: char ('+', '-', '*')
  │     ├── lhs: ExprAST
  │     └── rhs: ExprAST
  ├── CallExprAST                 ← function call: "multiply_transpose(a, b)"
  │     ├── callee: string
  │     └── args: vector<ExprAST>
  ├── PrintExprAST                ← builtin print: "print(x)"
  │     └── arg: ExprAST
  └── ReturnExprAST               ← return statement: "return expr"
        └── expr: optional<ExprAST>
```

### The base class and LLVM-style RTTI

```cpp
class ExprAST {
public:
  enum ExprASTKind {
    Expr_VarDecl, Expr_Return, Expr_Num, Expr_Literal,
    Expr_Var, Expr_BinOp, Expr_Call, Expr_Print,
  };

  ExprAST(ExprASTKind kind, Location location)
      : kind(kind), location(std::move(location)) {}

  ExprASTKind getKind() const { return kind; }
  const Location &loc() { return location; }

private:
  const ExprASTKind kind;
  Location location;
};
```

Every node stores:
1. **`kind`** — which concrete type it is (used for type-checking at runtime)
2. **`location`** — where in the source file this came from

**LLVM-style RTTI vs Java `instanceof`:**

In Java, you'd write:
```java
if (expr instanceof BinaryExprAST binOp) {
    char op = binOp.getOp();
}
```

In LLVM C++, each subclass defines `classof`:
```cpp
class BinaryExprAST : public ExprAST {
  // ...
  static bool classof(const ExprAST *c) { return c->getKind() == Expr_BinOp; }
};
```

Then you use `llvm::dyn_cast<>` instead of `dynamic_cast`:
```cpp
if (auto *binOp = llvm::dyn_cast<BinaryExprAST>(expr)) {
    char op = binOp->getOp();
}
```

**Why not just use C++ `dynamic_cast`?** Because LLVM is compiled with `-fno-rtti` (no Run-Time Type Information) for performance. Their custom RTTI via `classof` is faster and uses no memory overhead. This is why we had to add `-fno-rtti` in our CMakeLists when building — to match LLVM's build settings.

Basically LLVM uses its own faster RTTI system. Each AST class has:

```
// In the base class:
enum ExprASTKind { Expr_VarDecl, Expr_Num, Expr_BinOp, ... };
const ExprASTKind kind;

// In each subclass:
static bool classof(const ExprAST *c) { return c->getKind() == Expr_BinOp; }

```

Then you use llvm::dyn_cast<BinaryExprAST>(expr) instead of dynamic_cast. Same concept, but works without C++ RTTI enabled (that's the -fno-rtti flag we hit during the build!).


### Ownership model with `unique_ptr`

Notice everything uses `std::unique_ptr`:
```cpp
class BinaryExprAST : public ExprAST {
  char op;
  std::unique_ptr<ExprAST> lhs, rhs;  // this BinaryExprAST node OWNS its children
};
```

In Java, garbage collection handles memory. In C++, `unique_ptr` means "this node owns its children and destroys them when it dies." The AST is a **tree of ownership** — parent owns children. Destroying the root `ModuleAST` recursively destroys the entire tree. No leaks, no dangling pointers.

**Why `unique_ptr` and not `shared_ptr`?** Because a tree node has exactly one parent. There's no shared ownership. `unique_ptr` is cheaper (no reference counting) and makes ownership explicit.

### VarType — optional shape information

```cpp
struct VarType {
  std::vector<int64_t> shape;
};
```

Used in variable declarations. `var a = [1, 2, 3]` has shape `<>` (inferred from the literal). `var b<2, 3> = [1, 2, 3, 4, 5, 6]` has explicit shape `<2, 3>`.

---

## Part 4: The Parser — Building the Tree

> Source file: `Ch1/include/toy/Parser.h`

This is a **recursive descent parser** — the most intuitive parsing technique. Each grammar rule becomes a method.

### Grammar rules → methods

| Grammar Rule | Parser Method | What it recognizes |
|---|---|---|
| `module → function*` | `parseModule()` | Whole program = list of functions |
| `function → prototype block` | `parseDefinition()` | `def foo(a, b) { ... }` |
| `prototype → "def" name "(" params ")"` | `parsePrototype()` | `def foo(a, b)` |
| `block → "{" stmt* "}"` | `parseBlock()` | `{ stmt; stmt; ... }` |
| `stmt → var_decl \| return \| expr` | (inside parseBlock) | Statement dispatch |
| `var_decl → "var" name [type] "=" expr` | `parseDeclaration()` | `var a<2,3> = expr` |
| `return → "return" [expr]` | `parseReturn()` | `return expr;` or `return;` |
| `expr → primary binop_rhs` | `parseExpression()` | `a + b * c` |
| `primary → ident \| number \| "(" expr ")" \| "[" tensor "]"` | `parsePrimary()` | Base values |
| `type → "<" num ("," num)* ">"` | `parseType()` | `<2, 3>` |

### How recursive descent works

Each method handles one grammar rule. It looks at the current token to decide what to do. If a rule contains another rule, it **calls that method** — hence "recursive."

The parser starts with `parseModule()` which calls `parseDefinition()` in a loop. Each `parseDefinition()` calls `parsePrototype()` then `parseBlock()`. `parseBlock()` dispatches to `parseDeclaration()`, `parseReturn()`, or `parseExpression()` based on the current token. And so on, recursively down the tree.

### Trace: parsing `var c = a + b;`

```
parseBlock()
  sees tok_var → calls parseDeclaration()
    parseDeclaration()
      consumes "var"
      reads identifier "c"
      no <type> specified → creates empty VarType
      consumes "="
      calls parseExpression()
        parseExpression()
          calls parsePrimary()
            sees tok_identifier "a" → returns VariableExprAST("a")
          calls parseBinOpRHS(0, VariableExprAST("a"))
            sees '+' (precedence 20 >= 0) → consume it
            calls parsePrimary()
              sees tok_identifier "b" → returns VariableExprAST("b")
            next token is ';' (precedence -1 < 20) → stop
            returns BinaryExprAST('+', Var("a"), Var("b"))
      returns VarDeclExprAST("c", <>, BinaryExprAST('+', Var("a"), Var("b")))
    consumes ";"
```

### `parsePrimary()` — the dispatch point

```cpp
std::unique_ptr<ExprAST> parsePrimary() {
  switch (lexer.getCurToken()) {
  case tok_identifier:  return parseIdentifierExpr();  // variable ref or function call
  case tok_number:      return parseNumberExpr();       // numeric literal
  case '(':             return parseParenExpr();        // (expr)
  case '[':             return parseTensorLiteralExpr(); // [[1, 2], [3, 4]]
  case ';':             return nullptr;  // empty expression
  case '}':             return nullptr;  // end of block
  default:              /* error */
  }
}
```

This is where the parser decides what kind of expression it's looking at based on the first token. This technique is called **predictive parsing** — one token of lookahead is enough to decide.

### `parseIdentifierExpr()` — variable ref vs function call

```cpp
std::unique_ptr<ExprAST> parseIdentifierExpr() {
  std::string name(lexer.getId());
  lexer.getNextToken(); // eat the identifier

  if (lexer.getCurToken() != '(')
    // No '(' after name → it's just a variable reference
    return std::make_unique<VariableExprAST>(loc, name);

  // Has '(' → it's a function call, parse arguments
  lexer.consume(Token('('));
  // ... parse comma-separated argument list ...
  lexer.consume(Token(')'));

  // Special case: "print" is a builtin
  if (name == "print")
    return std::make_unique<PrintExprAST>(loc, std::move(args[0]));

  return std::make_unique<CallExprAST>(loc, name, std::move(args));
}
```

Notice how one token of lookahead (peeking at `(`) determines the entire parse path. `foo` alone is a variable. `foo(` starts a function call.

### Operator precedence — the hardest part

`parseBinOpRHS()` at `Parser.h:244` implements **precedence climbing**.

The precedence table:
```cpp
int getTokPrecedence() {
  switch (static_cast<char>(lexer.getCurToken())) {
    case '-': return 20;
    case '+': return 20;
    case '*': return 40;  // higher = binds tighter
    default:  return -1;  // not an operator
  }
}
```

**The rule:** Only consume the next operator if it binds at least as tightly as the current precedence threshold. If the next operator is tighter, recurse into it first (it becomes a child node).

**Trace for `a + b * c`:**

```
parseBinOpRHS(exprPrec=0, lhs=Var("a"))
  current token: '+' (precedence 20)
  20 >= 0? YES → consume '+'
  rhs = parsePrimary() → Var("b")

  peek next token: '*' (precedence 40)
  40 > 20? YES → '*' binds tighter, so recurse:
    rhs = parseBinOpRHS(exprPrec=21, lhs=Var("b"))
      current token: '*' (precedence 40)
      40 >= 21? YES → consume '*'
      rhs = parsePrimary() → Var("c")

      peek next token: ';' (precedence -1)
      -1 >= 40? NO → stop recursion
      return BinaryExpr('*', Var("b"), Var("c"))

  lhs = BinaryExpr('+', Var("a"), BinaryExpr('*', Var("b"), Var("c")))

  peek next token: ';' (precedence -1)
  -1 >= 0? NO → stop
  return BinaryExpr('+', Var("a"), BinaryExpr('*', Var("b"), Var("c")))
```

**Result:** `a + (b * c)` — mathematically correct! `*` ended up as a child of `+` because it binds tighter.

The algorithm in code:
```cpp
std::unique_ptr<ExprAST> parseBinOpRHS(int exprPrec, std::unique_ptr<ExprAST> lhs) {
  while (true) {
    int tokPrec = getTokPrecedence();

    // If this operator binds less tightly than our threshold, we're done
    if (tokPrec < exprPrec)
      return lhs;

    // Save the operator and consume it
    int binOp = lexer.getCurToken();
    lexer.consume(Token(binOp));

    // Parse the right-hand side (primary expression)
    auto rhs = parsePrimary();

    // If the NEXT operator binds tighter, let it take our rhs
    int nextPrec = getTokPrecedence();
    if (tokPrec < nextPrec) {
      rhs = parseBinOpRHS(tokPrec + 1, std::move(rhs));
    }

    // Merge lhs and rhs into a BinaryExprAST
    lhs = std::make_unique<BinaryExprAST>(loc, binOp, std::move(lhs), std::move(rhs));
  }
}
```

### `parseTensorLiteralExpr()` — nested array parsing

This handles tensor literals like `[[1, 2, 3], [4, 5, 6]]`. It's recursive:

```
'[' → start a new nesting level
  '[' → start another nesting level
    1, 2, 3 → parse numbers
  ']' → close inner level
  ',' → separator
  '[' → another inner level
    4, 5, 6 → parse numbers
  ']' → close inner level
']' → close outer level
```

After parsing, it validates that all inner arrays have the same dimensions (uniform shape).

The resulting `LiteralExprAST` stores:
- `dims = [2, 3]` (2 rows, 3 columns)
- `values = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]` (flattened, as `NumberExprAST` nodes)

### Error handling

```cpp
template <typename R, typename T, typename U = const char *>
std::unique_ptr<R> parseError(T &&expected, U &&context = "") {
  llvm::errs() << "Parse error (" << lexer.getLastLocation().line << ", "
               << lexer.getLastLocation().col << "): expected '" << expected
               << "' " << context << " but has Token " << curToken;
  return nullptr;
}
```

Errors return `nullptr` which propagates up the call chain. Each caller checks for `nullptr` and bails out. Simple but effective — no exceptions, no recovery. The parser stops at the first error.

### What the parser does NOT do

The parser in Chapter 1 performs **no semantic checks**:
- You can reference undefined variables: `var x = y;` (y never declared) — parses fine
- You can call undefined functions — parses fine
- Shape mismatches — not caught here

Semantic analysis (type checking, shape inference, scope resolution) comes in Chapter 4.

---

## Part 5: The AST Dumper — Pretty Printing the Tree

> Source file: `Ch1/parser/AST.cpp`

This file implements `dump(ModuleAST &)` — the function that prints the AST in the indented format we see in the output.

Key design patterns:

### RAII indentation

```cpp
struct Indent {
  Indent(int &level) : level(level) { ++level; }
  ~Indent() { --level; }
  int &level;
};
```

When entering a nested node, create an `Indent` object. When leaving (scope exit), the destructor decreases indentation automatically. No manual indent/dedent tracking needed.

### TypeSwitch for dispatch

```cpp
void ASTDumper::dump(ExprAST *expr) {
  llvm::TypeSwitch<ExprAST *>(expr)
      .Case<BinaryExprAST, CallExprAST, LiteralExprAST, NumberExprAST,
            PrintExprAST, ReturnExprAST, VarDeclExprAST, VariableExprAST>(
          [&](auto *node) { this->dump(node); })
      .Default([&](ExprAST *) { /* unknown */ });
}
```

LLVM's `TypeSwitch` is like a Java switch on `instanceof` — it tries each type in order and calls the lambda when one matches. Under the hood it uses the `classof` RTTI we saw earlier.

---

## Part 6: The Driver — Wiring It Together

> Source file: `Ch1/toyc.cpp`

Only 72 lines. The flow:

```cpp
// 1. Read file into memory buffer
llvm::ErrorOr<std::unique_ptr<llvm::MemoryBuffer>> fileOrErr =
    llvm::MemoryBuffer::getFileOrSTDIN(filename);

// 2. Create lexer from buffer
LexerBuffer lexer(buffer.begin(), buffer.end(), std::string(filename));

// 3. Create parser, give it the lexer
Parser parser(lexer);

// 4. Parse the whole module
auto moduleAST = parser.parseModule();

// 5. If --emit=ast, dump it
switch (emitAction) {
  case Action::DumpAST:
    dump(*moduleAST);
    return 0;
}
```

Uses LLVM's `cl::opt` for command-line argument parsing:
- `inputFilename` — the `.toy` file to compile
- `--emit=ast` — what output to produce (only AST dump in Ch1)

---

## Part 7: Seeing It in Action

### Building

```bash
cd 02-basic-compilers/projects/mlir-toy-compiler/src/toy-reference/Ch1
cmake -S . -B build -G Ninja -DCMAKE_CXX_COMPILER=clang++
cmake --build build
```

### Running

```bash
./build/toyc-ch1 ../../tests/toy-tests/Ch1/ast.toy -emit=ast
```

### Output for the example program

```
Module:
  Function
    Proto 'multiply_transpose' @ast.toy:4:1
    Params: [a, b]
    Block {
      Return
        BinOp: * @ast.toy:5:25
          Call 'transpose' [ @ast.toy:5:10
            var: a @ast.toy:5:20
          ]
          Call 'transpose' [ @ast.toy:5:25
            var: b @ast.toy:5:35
          ]
    } // Block
  Function
    Proto 'main' @ast.toy:8:1
    Params: []
    Block {
      VarDecl a<> @ast.toy:11:3
        Literal: <2, 3>[ <3>[ 1, 2, 3], <3>[ 4, 5, 6]] @ast.toy:11:11
      VarDecl b<2, 3> @ast.toy:15:3
        Literal: <6>[ 1, 2, 3, 4, 5, 6] @ast.toy:15:17
      VarDecl c<> @ast.toy:19:3
        Call 'multiply_transpose' [ @ast.toy:19:11
          var: a @ast.toy:19:30
          var: b @ast.toy:19:33
        ]
      ...
    } // Block
```

### Operator precedence demo

Input:
```
def main() {
  var a = [1, 2, 3];
  var b = [4, 5, 6];
  var d = a + b * a;
  print(d);
}
```

Output for `var d = a + b * a;`:
```
VarDecl d<>
  BinOp: +
    var: a
    BinOp: *        ← * binds tighter, becomes child of +
      var: b
      var: a
```

`a + b * a` correctly parsed as `a + (b * a)` because `*` (precedence 40) > `+` (precedence 20).

---

## Key Takeaways

1. **Lexer design:** One-character lookahead, ASCII trick for single-char tokens, keywords recognized after reading the full identifier word.

2. **AST design:** Base class with enum discriminator + LLVM-style RTTI (`classof`/`dyn_cast` instead of `instanceof`/`dynamic_cast`). Tree ownership via `unique_ptr` (no GC in C++).

3. **Parser design:** Recursive descent where grammar rules map 1-to-1 to methods. Precedence climbing for binary operators via `parseBinOpRHS()`.

4. **Location tracking:** Baked in from the start — every token and AST node carries source location. MLIR requires this (unlike LLVM IR where it's optional).

5. **No semantic checks in Ch1:** The parser accepts syntactically valid programs even if they reference undefined variables or have shape mismatches. That's a later phase (Chapter 4).

6. **Clean separation:** Lexer knows nothing about grammar. Parser knows nothing about semantics. Each layer does one job. This is the classic compiler pipeline philosophy.

---

## What's Next

Chapter 2 takes this AST and **generates MLIR** from it. Instead of dumping a text tree, we'll walk the AST and create MLIR operations in a custom "Toy" dialect. That's where we enter the MLIR world.
