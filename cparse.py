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

    @_("CLASS IDENT [ LT IDENT ] LBRACE { function } RBRACE")
    def class_declaration(self, p):
        pass

    @_("FUN function")
    def func_declaration(self, p):
        pass

    @_("VAR IDENT [ ASSIGN expression ]")
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

    @_("expression SEMI")
    def expr_stmt(self, p):
        pass

    @_("FOR LPAREN for_initialize SEMI [ expression ] SEMI [ expression ] RPAREN statement")
    def for_stmt(self, p):
        pass

    @_("FOR LPAREN SEMI [ expression ] SEMI [ expression ] RPAREN statement")
    def for_stmt(self, p):
        pass

    @_("var_declaration", "expr_stmt")
    def for_initialize(self, p):
        pass

    @_("IF LPAREN [ expression ] RPAREN statement [ ELSE statement ]  ")
    def if_stmt(self, p):
        pass

    @_("PRINT expression")
    def print_stmt(self, p):
        pass

    @_("RETURN [ expression ]")
    def return_stmt (self, p):
        pass

    @_("WHILE LPAREN expression RPAREN statement")
    def while_stmt(self, p):
        pass

    @_("LBRACE { declaration } RBRACE")
    def block(self, p):
        pass

    @_("assignment")
    def expression(self, p):
        pass

    @_("[ call POINT ] IDENT ASSIGN expression")
    def assignment(self, p):
        pass

    @_("logic_or")
    def assignment(self, p):
        pass

    @_("logic_and { OR logic_and }")
    def logic_or(self, p):
        pass

    @_("equality { AND equality }")
    def logic_and(self, p):
        pass

    @_("comparison { ( NE | EQ ) comparison }")
    def equality(self, p):
        pass

    @_("term { ( GT | GE | LT | LE ) term }")
    def comparison(self, p):
        pass

    @_("factor { ( MINUS | PLUS ) factor }")
    def term(self, p):
        pass

    @_("unary { ( DIVIDE | TIMES ) unary }")
    def factor(self, p):
        pass

    @_("( NOT | MINUS ) unary | call")
    def unary(self, p):
        pass

    @_("primary { LPAREN [ arguments ] RPAREN | POINT IDENT }")
    def call(self, p):
        pass

    @_("TRUE | FALSE | NIL | THIS | REAL | NUM | STRING | IDENT | LPAREN expression RPAREN | SUPER POINT IDENT")
    def primary(self, p):
        pass

    @_("IDENT LPAREN [ parameters ] RPAREN block")
    def function(self, p):
        pass

    @_("IDENT { COMMA IDENT }")
    def parameters(self, p):
        pass

    @_("expression { COMMA expression }")
    def arguments(self, p):
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

    root = p.parse( #we'll start to build our AST
        l.tokenize(open(sys.argv[1], encoding='utf-8'))
    )
