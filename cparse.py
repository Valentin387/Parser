
from clex import Lexer
import sly
from cast import *

class Parser(sly.Parser):
    debugfile="minic.txt"
    # La lista de tokens se copia desde Lexer
    tokens = Lexer.tokens

    def __init__(self, ctxt):
        self.ctxt=ctxt

    # preceencia de operadores
    precedence = (
        ('right', PLUSPLUS),
        ('right', MINUSMINUS),
        ('right', ADDEQ),
        ('right', MINEQ),
        ('right', TIMESEQ),
        ('right', DIVIDEEQ),
        ('right', MODULEEQ),
        ('right', ASSIGN),     # menor precedencia
        ('left', OR),
        ('left', AND),
        ('left', EQ, NE),
        ('left', LT, LE, GT, GE),
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE, MODULE),
        ('right', UNARY),
    )

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

    @_("CLASS IDENT [ LPAREN LT IDENT RPAREN ] LBRACE { function } RBRACE ")
    def class_declaration(self, p):
        return ClassDeclaration(p.IDENT0, p.IDENT1, p.function)

    @_("FUN function")
    def func_declaration(self, p):
        return p[1]

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
        #pass

    @_("FOR LPAREN for_initialize [ expression ] SEMI [ expression ] RPAREN statement")
    def for_stmt(self, p):
        return ForStmt(p.for_initialize,p.expression0,p.expression1,p.statement)

    @_("FOR LPAREN SEMI [ expression ] SEMI [ expression ] RPAREN statement")
    def for_stmt(self, p):
        return ForStmt(None,p.expression0,p.expression1,p.statement)

    @_("var_declaration",
        "expr_stmt")
    def for_initialize(self, p):
        return p[0]
#########################################
    @_("IF LPAREN [ expression ] RPAREN statement [ ELSE statement ] END_IF")
    def if_stmt(self, p):
        return IfStmt(p.expression, p.statement0, p.statement1)

#########################################
    @_("PRINT LPAREN expression RPAREN SEMI")
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

    @_("expression ASSIGN expression",
       "expression ADDEQ expression",
       "expression MINEQ expression",
       "expression TIMESEQ expression",
       "expression DIVIDEEQ expression",
       "expression MODULEEQ expression")
    def expression(self, p):
        if isinstance(p.expression0, Variable):
            return Assign(p[1], p.expression0.name, p.expression1)
        elif isinstance(p.expression0, Get):
            return Set(p.expression0.obj, p.expression0.name, p.expression1)
        else:
            raise SyntaxError(f"{p.lineno}: PARSER ERROR, it was impossible to assign {p.expression0}")

##################################################################################################
    @_("expression PLUSPLUS",
       "expression MINUSMINUS")
    def expression(self, p):
        return Assign(p[1], p.expression.name, Literal(1))

    @_("PLUSPLUS expression",
       "MINUSMINUS expression")
    def expression(self, p):
        return Assign(p[0], p.expression.name, Literal(1))

##################################################################################################

    @_("expression OR  expression",
       "expression AND expression")
    def expression(self, p):
        return Logical(p[1], p.expression0, p.expression1)

    @_("expression PLUS expression",
       "expression MINUS expression",
       "expression TIMES expression" ,
       "expression DIVIDE expression" ,
       "expression MODULE expression" ,
       "expression LT  expression" ,
       "expression LE  expression" ,
       "expression GT  expression" ,
       "expression GE  expression" ,
       "expression EQ  expression" ,
       "expression NE  expression")
    def expression(self, p):
        return Binary(p[1], p.expression0, p.expression1)

    @_("factor")
    def expression(self, p):
        return p.factor

    @_("REAL", "NUM", "STRING")
    def factor(self, p):
        return Literal(p[0])

    @_("TRUE", "FALSE")
    def factor(self, p):
        return Literal(p[0] == 'true')

    @_("NIL")
    def factor(self, p):
        return Literal(None)

    @_("THIS")
    def factor(self, p):
        return This()

    @_("IDENT")
    def factor(self, p):
        return Variable(p.IDENT)

    @_("SUPER POINT IDENT")
    def factor(self, p):
        return Super(p.IDENT)

    @_("factor POINT IDENT")
    def factor(self, p):
        return Get(p.factor, p.IDENT)

    @_("factor LPAREN [ arguments ] RPAREN ")
    def factor(self, p):
        return Call(p.factor, p.arguments)

    @_(" LPAREN expression RPAREN ")
    def factor(self, p):
        return Grouping(p.expression)

    @_("MINUS factor %prec UNARY",
       "NOT factor %prec UNARY")
    def factor(self, p):
        return Unary(p[0], p.factor)

    @_("IDENT LPAREN [ parameters ] RPAREN block")
    def function(self, p):
        return FuncDeclaration(p.IDENT, p.parameters, p.block)

    @_("IDENT { COMMA IDENT }")
    def parameters(self, p):
        return [ p.IDENT0 ] + p.IDENT1

    @_("expression { COMMA expression }")
    def arguments(self, p):
        return [ p. expression0 ] + p.expression1

    def error(self, p):
        if p:
            self.ctxt.error(p, f"PARSER ERROR, Syntax error in the Token {p.type} due to: {p}")
            # Just discard the token and tell the parser it's okay.
        else:
            self.ctxt.error(p, f"PARSER ERROR, Syntax Error in EOF. Check braces and semicolons ")
