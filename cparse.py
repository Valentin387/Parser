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
from render import DotRender


class Parser(sly.Parser):
    debugfile="minic.txt"
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

    @_("CLASS IDENT [ LT IDENT ] LBRACE { function } RBRACE ")
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

    @_("FOR LPAREN for_initialize [ expression ] SEMI [ expression ] RPAREN statement")
    def for_stmt(self, p):
        body = p.statement
        if p.expression1:
            if not isinstance(body, Block):
                body = Block([ body ])

            body.stmts.append(ExprStmt(p.expression1))
        body = WhileStmt(p.expression0 or Literal(True), body)
        body = Block([p.for_initializer, body])
        return body


    @_("FOR LPAREN SEMI [ expression ] SEMI [ expression ] RPAREN statement")
    def for_stmt(self, p):
        body = p.statement
        if p.expression1:
            if not isinstance(body, Block):
                body = Block([ body ])

            body.stmts.append(ExprStmt(p.expression1))
        body = WhileStmt(p.expression0 or Literal(True), body)
        return body

    @_("var_declaration",
        "expr_stmt")
    def for_initialize(self, p):
        return p[0]

    @_("IF LPAREN [ expression ] RPAREN statement [ ELSE statement ]  ")
    def if_stmt(self, p):
        return IfStmt(p.expression, p.statement0, p.statement1)

    @_("PRINT expression SEMI")
    def print_stmt(self, p):
        return Print(p.expression)

    @_("RETURN [ expression ] SEMI")
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
        lval = p.logic_and0
        for op, rval in p[1]:
            lval = Logical(op, lval, rval)
        return lval

    @_("equality { AND equality }")
    def logic_and(self, p):
        lval = p.equality0
        for op, rval in p[1]:
            lval = Logical(op, lval, rval)
        return lval

    @_("comparison { oper1 comparison }")
    def equality(self, p):
        lval = p.comparison0
        for op, rval in p[1]:
            lval = Logical(op, lval, rval)
        return lval

    @_("NE","EQ")
    def oper1(self, p):
        pass

    @_("term { oper2 term }")
    def comparison(self, p):
        lval = p.term0
        for op, rval in p[1]:
            lval = Logical(op, lval, rval)
        return lval

    @_("GT", "GE",  "LT", "LE")
    def oper2(self, p):
        pass

    @_("factor { oper3 factor }")
    def term(self, p):
        lval = p.factor0
        for op, rval in p[1]:
            lval = Logical(op, lval, rval)
        return lval

    @_("MINUS", "PLUS")
    def oper3(self, p):
        pass

    @_("unary { oper4 unary }")
    def factor(self, p):
        lval = p.unary0
        for op, rval in p[1]:
            lval = Logical(op, lval, rval)
        return lval

    @_("DIVIDE", "TIMES")
    def oper4(self, p):
        pass

    @_("oper5 unary")
    def unary(self, p):
        return Unary(p[0], p[1])

    @_("call")
    def unary(self, p):
        return p[0]

    @_("NOT", "MINUS")
    def oper5(self, p):
        pass

    @_("primary { oper6 }")
    def call(self, p):
        return Call(p.primary, p[1])

    @_("LPAREN [ arguments ] RPAREN", " POINT IDENT")
    def oper6(self, p):
        pass

    @_("TRUE", "FALSE", "NIL", "THIS", "REAL", "NUM", "STRING", "IDENT", "LPAREN expression RPAREN", "SUPER POINT IDENT")
    def primary(self, p):
        return Literal(p[0])

    @_("IDENT LPAREN [ parameters ] RPAREN block")
    def function(self, p):
        return FuncDeclaration(p.IDENT, p.parameters, p.block)

    @_("IDENT { COMMA IDENT }")
    def parameters(self, p):
        lval = p.IDENT0
        for op, rval in p[1]:
            lval = Logical(op, lval, rval)
        return lval

    @_("expression { COMMA expression }")
    def arguments(self, p):
        lval = p.expression0
        for op, rval in p[1]:
            lval = Logical(op, lval, rval)
        return lval

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

    #we'll start to build our AST
    ast = p.parse(
        l.tokenize(open(sys.argv[1], encoding='utf-8').read())
    )
    print(ast)
    #dot = DotRender.render(ast)
    #print(dot)
