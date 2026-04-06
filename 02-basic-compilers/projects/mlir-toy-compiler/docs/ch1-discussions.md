# Chapter 1: Discussions & Project Analysis

Insights from working through Chapter 1 — project structure, design decisions, and things that weren't obvious at first.

---

## The Frontend is Always First

Every compiler starts with the frontend. You can't optimize or generate machine code if you haven't read the source code first. The pipeline is always: **Frontend → Middle-end → Backend**. Chapter 1 builds just the frontend.

---

## C++ Project Structure 

The Ch1 project has this layout:

```
Ch1/
├── include/toy/       ← Header files (.h)
│   ├── Lexer.h           Complete lexer (interface + implementation)
│   ├── AST.h             AST node type definitions (data classes)
│   └── Parser.h          Complete parser (interface + implementation)
│
├── parser/
│   └── AST.cpp        ← AST pretty-printer (the dump() function)
│
└── toyc.cpp           ← main() entry point — the compiler executable
```

### Header-only implementation — is that allowed?

Yes. Lexer.h and Parser.h contain the **full implementation** right inside the header, not just declarations. This is called **header-only** design.

The C++ compiler doesn't care whether code is in `.h` or `.cpp` — headers are literally copy-pasted into `.cpp` files by the preprocessor (`#include`). It's all text substitution.

This is actually very common in C++:
- The entire C++ Standard Template Library (STL) — `vector`, `map`, `string` — is header-only
- Most LLVM utilities are header-only
- Boost (huge C++ library) — mostly header-only

**When you do it:** Small-to-medium classes, template code (templates *must* be in headers), code that's only included by one or two `.cpp` files.

**When you don't:** Large implementations that would slow down compilation if every file including the header had to recompile all that code.

So it's not a shortcut or hack — it's a deliberate, common C++ design choice. The Toy project is small enough that header-only works perfectly for Lexer and Parser.

### Why is AST.cpp the only separate implementation file?

The dump logic in AST.cpp uses heavy LLVM utilities (`TypeSwitch`, `Twine`, etc.). Putting that in the header would slow down compilation since every file that includes `AST.h` would also compile all that printing logic.

**Java analogy:** Think of it like having `Lexer.java`, `Parser.java`, `AST.java` where all the logic is in those files, and then a separate `ASTPrinter.java` utility class.

---

## What Each File Actually Is

| File | What it is | Needed for compilation? |
|------|-----------|------------------------|
| `Lexer.h` | Characters → Tokens (full implementation) | Yes — core compiler component |
| `AST.h` | Data class definitions for tree nodes | Yes — the data model |
| `Parser.h` | Tokens → AST tree (full implementation) | Yes — core compiler component |
| `AST.cpp` | Pretty-printer to visualize the AST | No — debugging/testing only |
| `toyc.cpp` | `main()` — wires everything together | Yes — entry point |

### AST.h is structure, not implementation

AST.h defines **what the tree nodes look like** — their fields, constructors, and getters. There's no algorithm or logic. It's a passive data model.

```java
// Java equivalent of what AST.h does — just data classes
class BinaryExprAST {
    char op;
    ExprAST lhs, rhs;
    BinaryExprAST(char op, ExprAST lhs, ExprAST rhs) { ... }
    char getOp() { return op; }
}
```

The **parser** creates these objects. The AST nodes themselves are just containers.

### What dump() does (AST.cpp)

`dump()` is a pretty-printer that walks the AST tree and prints it in a human-readable indented format. That's the output you see when you run `toyc-ch1 --emit=ast`.

**Is it just printing?** Yes. **Is it needed for the compiler?** No — later chapters walk the AST to generate MLIR instead. But it's crucial for:

1. **Learning** — you can see what the parser actually built. Without this, the AST is invisible (just objects in memory).
2. **Debugging** — when the parser has a bug, dump the AST to see what went wrong.
3. **Testing** — the test files have `CHECK:` lines that verify the dump output matches expected output.

Every real compiler has something like this: GCC has `-fdump-tree-all`, Clang has `-ast-dump`, Java's `javac` has `-Xprint`. Standard practice.

---

## The Compiler vs The Code Being Compiled

This is a key mental model:

```
.toy files (Toy language)  →  toyc-ch1 (our compiler)  →  Output (AST dump, later MLIR)
```

The `.cpp` files **are** the compiler. The `.toy` files are what gets compiled.

| | Java world | Our world |
|---|---|---|
| The compiler | `javac` | `toyc-ch1` (built from .cpp/.h files) |
| Source code being compiled | `Main.java` | `ast.toy`, `playground.toy` |
| Output | `Main.class` (bytecode) | AST dump (Ch1), MLIR (Ch2+) |

The `tests/` folder serves two purposes:
1. **Playground** — write Toy programs to experiment with
2. **Test suite** — verify the compiler produces correct output

Everything in `src/` is the compiler itself — the tool that reads and processes `.toy` files.

### How the files connect — visual summary

```
You write this:          Our compiler reads it:        And produces this:

  ast.toy  ───────────→  toyc.cpp (main)  ──────────→  AST dump
  (Toy language)           │
                           ├── creates Lexer (from Lexer.h)
                           ├── creates Parser (from Parser.h)
                           ├── parser uses AST node types (from AST.h)
                           └── calls dump() (from AST.cpp) to print
```

### What toyc.cpp does (the driver)

`toyc.cpp` is the **compiler executable** — the `main()` function that wires all the components together. It is NOT test code and it contains NO compiler logic. It just orchestrates the pipeline:

```
1. Read a .toy file from disk into a memory buffer
2. Create a Lexer — feed it the file contents
3. Create a Parser — give it the lexer
4. Call parser.parseModule() → get back an AST
5. If user passed --emit=ast → call dump() to print the AST
```

Think of it like your `Main.java` with `public static void main(String[] args)`. It doesn't implement lexing or parsing — it just calls the components in order. All the real work happens inside Lexer.h, Parser.h, and AST.h.

It also uses LLVM's `cl::opt` for command-line argument parsing:
- Positional argument → the `.toy` file path
- `--emit=ast` → what output to produce (only AST dump in Ch1, more options added in later chapters)

---

## Build Notes

### CMakeLists.txt for standalone build

The original LLVM CMakeLists uses internal macros (`add_toy_chapter`). Our standalone version:
- Uses `find_package(LLVM)` and `find_package(MLIR)` with `NO_DEFAULT_PATH` to avoid picking up system LLVM
- Points to our local LLVM 19.1.0 source build at `external/llvm-project/build/install/`
- Adds `-fno-rtti` flag to match LLVM's build settings (LLVM disables C++ RTTI for performance)

### The -fno-rtti gotcha

LLVM is built without C++ Run-Time Type Information. If your code uses default RTTI but links against LLVM libraries built without it, you get linker errors about `typeinfo`. The fix: add `-fno-rtti` to your build. This is also why LLVM uses its own `classof`/`dyn_cast` RTTI system instead of `dynamic_cast`.

### Building and running

```bash
cd src/toy-reference/Ch1
cmake -S . -B build -G Ninja -DCMAKE_CXX_COMPILER=clang++
cmake --build build

# Run on a test file
./build/toyc-ch1 ../../../tests/toy-tests/Ch1/ast.toy -emit=ast
```
