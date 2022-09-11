'''
program ::= declaration*                 { } - repeticion (0 o mas)
                                         [ ] - opcionalidad
Declaration ::= classDecl
  | funDecl
  | varDecl
  | statement

classDecl ::= 'class' IDENTIFIER ( '<' IDENTIFIER )?
  '{' function* '}'

funDecl ::= 'fun' function

varDecl ::= 'var' IDENTIFIER ( '=' expression )? ';'

statement ::= exprStmt
  | forStmt
  | ifStmt
  | printStmt
  | returnStmt
  | whileStmt
  | block

exprStmt ::= expression ';'

forStmt ::= 'for' '(' ( varDecl | exprStmt )? ';'
  expression? ';'
  expression? ')' statement

ifStmt ::= 'if' '(' expression ')' statement
  ( 'else' statement )?
printStmt ::= 'print' expression ';'

returnStmt ::= 'return' expression? ';'

whileStmt ::= 'while' '(' expression ')' statement

block ::= '{' declaration* '}'

expression ::= assignment

assignment ::= ( call '.' )? IDENTIFIER '=' expression
   | logic_or

logic_or ::= logic_and ( '||' logic_and )*

logic_and ::= equality ( '&&' equality )*

equality ::= comparison ( ( '!=' | '==' ) comparison )*

comparison ::= term ( ( '>' | '>=' | '<' | '<=' ) term )*

term ::= factor ( ( '-' | '+' ) factor )*

factor ::= unary ( ( '/' | '*' ) unary )*

unary ::= ( '!' | '-' ) unary | call

call ::= primary ( '(' arguments? ')' | '.' IDENTIFIER )*

primary ::= 'true' | 'false' | 'nil' | 'this'
   | NUMBER | STRING | IDENTIFIER | '(' expression ')'
   | 'super' '.' IDENTIFIER

function ::= IDENTIFIER '(' parameters? ')' block

parameters ::= IDENTIFIER ( ',' IDENTIFIER )*

arguments ::= expression ( ',' expression )*
'''
from clex import Lexer
import sly


class Parser(sly.Parser):
    # La lista de tokens se copia desde Lexer
    tokens = Lexer.tokens

    # Definimos las reglas en BNF (o en EBNF)
    @_("{ declaration }")
    def program(self, p):
        pass

    @_("class_declaration",
       "func_declaration",
       "var_declaration",
       "statement")
    def declaration(self, p):
        pass

    @_("CLASS IDENT [ LT IDENT ] '{' { function } '}'")
    def class_declaration(self, p):
        pass

    @_("FUN function")
    def func_declaration(self, p):
        pass

    @_("VAR IDENT [ '=' expression ]")
    def var_declaration(self, p):
        pass

    @_("expr_stmt",
       "for_stmt",
       "if_stmt",
       "print_stmt",
       "return_stmt",
       "while_stmt",
       "block")
    def statement(self, p):
        pass

    @_("expression ';'")
    def expr_stmt(self, p):
        pass

    def error(self, p):
        if p:
            print("Error de sintaxis en token", p.type)
            # Just discard the token and tell the parser it's okay.
            self.errok()
        else:
            print("Error de sintaxis en EOF")

if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        print('Usage: python cparse.py filename')
        exit(0)

    l = Lexer()     # Analizador Lexico
    p = Parser()    # Analizador Sintactico

    root = p.parse(
        l.tokenize(open(sys.argv[1], encoding='utf-8'))
    )
