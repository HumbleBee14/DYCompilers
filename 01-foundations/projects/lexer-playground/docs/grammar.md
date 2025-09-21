# Grammar Notes

Document the grammars used for lexer and parser experiments. Include EBNF, token definitions, and any special handling rules.

## Arithmetic Grammar (Starter)
```
Expr   ::= Term (("+" | "-") Term)*
Term   ::= Factor (("*" | "/") Factor)*
Factor ::= NUMBER | IDENT | "(" Expr ")"
```
- Token set: NUMBER, IDENT, PLUS, MINUS, STAR, SLASH, LPAREN, RPAREN.
- Precedence/associativity: `*`/`/` > `+`/`-`, left associative.

## JSON Fragment (Optional)
```
Value ::= STRING | NUMBER | Object | Array | "true" | "false" | "null"
Object ::= "{" Members? "}"
Members ::= Pair ("," Pair)*
Pair ::= STRING ":" Value
Array ::= "[" Elements? "]"
Elements ::= Value ("," Value)*
```
- Token set: STRING, NUMBER, LBRACE, RBRACE, COLON, COMMA, LBRACKET, RBRACKET, TRUE, FALSE, NULL.

## TODO
- [ ] Add error-handling rules.
- [ ] Track reserved keywords vs identifiers.
- [ ] Document whitespace/comment treatment.
