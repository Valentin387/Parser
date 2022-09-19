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
from rich import print
from cast import *


class Parser(sly.Parser):
    # La lista de tokens se copia desde Lexer
    tokens = Lexer.tokens

    # Definimos las reglas en BNF (o en EBNF)
    @_("{ declaration }")
    def program(self, p):
        return Program(p.declaration)

    @_("class_declaration",
       "func_declaration",
       "var_declaration",
       "statement")
    def declaration(self, p):
        return p[0]

    @_("CLASS IDENT [ LT IDENT ] LBRACE { function } RBRACE")
    def class_declaration(self, p):
        return ClassDeclaration(p.IDENT0, p.IDENT1, p.function)

    @_("FUN function")
    def func_declaration(self, p):
        return p[0]

    @_("VAR IDENT [ ASSIGN expression ] SEMI")
    def var_declaration(self, p):
        return VarDeclaration(p.IDENT, p.expression)

    @_("expr_stmt",
       "for_stmt",
       "if_stmt",
       "print_stmt",
       "return_stmt",
       "while_stmt",
       "block")
    def statement(self, p):
        return p[0]

    @_("expression SEMI")
    def expr_stmt(self, p):
        return ExprStmt(p.expression)

    @_("FOR LPAREN for_initialize SEMI [ expression ] SEMI [ expression ] RPAREN statement")
    def for_stmt(self, p):
        return WhileStmt(p.expresion0, p.statement)

    @_("FOR LPAREN SEMI [ expression ] SEMI [ expression ] RPAREN statement")
    def for_stmt(self, p):
        return WhileStmt(p.expresion0, p.statement)

    @_("var_declaration",
        "expr_stmt")
    def for_initialize(self, p):
        return p[0]

    @_("IF LPAREN [ expression ] RPAREN statement [ ELSE statement ]  ")
    def if_stmt(self, p):
        return IfStmt(p.expression, p.statement0, p.statement1)

    @_("PRINT expression")
    def print_stmt(self, p):
        return Print(p.expression)

    @_("RETURN [ expression ]")
    def return_stmt (self, p):
        return Return(p.expression)

    @_("WHILE LPAREN expression RPAREN statement")
    def while_stmt(self, p):
        return WhileStmt(p.expression, p.statement)

    @_("LBRACE { declaration } RBRACE")
    def block(self, p):
        return Block(p.declaration)

    @_("assignment")
    def expression(self, p):
        return p[0]

    @_("[ call POINT ] IDENT ASSIGN expression")
    def assignment(self, p):
        return Assign(p.IDENT, p.expression)

    @_("logic_or")
    def assignment(self, p):
        return p[0]

    @_("logic_and { OR logic_and }")
    def logic_or(self, p):
        return Logical(p.OR, p.logic_and0, p.logic_and1)

    @_("equality { AND equality }")
    def logic_and(self, p):
        return Logical(p.AND, p.equality0, p.equality1)

    @_("comparison { '(' NE '|' EQ ')' comparison }")
    def equality(self, p):
        return Logical(p[1], p.comparison0, p.comparison1)

    @_("term { '(' GT '|' GE '|' LT '|' LE ')' term }")
    def comparison(self, p):
        return Logical(p[1], p.term0, p.term1)

    @_("factor { '(' MINUS '|' PLUS ')' factor }")
    def term(self, p):
        return Binary(p[1], p.factor0, p.factor1)

    @_("unary { '(' DIVIDE '|' TIMES ')' unary }")
    def factor(self, p):
        return Binary(p[1], p.unary0, p.unary1)

    @_("'(' NOT '|' MINUS ')' unary '|' call")
    def unary(self, p):
        return Unary(p[0], p[1])

    @_("primary { LPAREN [ arguments ] RPAREN '|' POINT IDENT }")
    def call(self, p):
        return Call(p.primary, p[1])

    @_("TRUE '|' FALSE '|' NIL '|' THIS '|' REAL '|' NUM '|' STRING '|' IDENT '|' LPAREN expression RPAREN '|' SUPER POINT IDENT")
    def primary(self, p):
        return Literal(p[0])

    @_("IDENT LPAREN [ parameters ] RPAREN block")
    def function(self, p):
        return FunDeclaration(p.IDENT, p.parameters, p.block)

    @_("IDENT { COMMA IDENT }")
    def parameters(self, p):
        return ExprStmt(p[0])

    @_("expression { COMMA expression }")
    def arguments(self, p):
        return ExprStmt(p[0])

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

    ast = p.parse( #we'll start to build our AST
        l.tokenize(open(sys.argv[1], encoding='utf-8'))
    )

    print(ast)
