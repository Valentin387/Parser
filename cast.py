'''
cast.py

Estructura del árbol de síntaxis abstracto
'''

from dataclasses import dataclass, field
from multimethod import multimeta
from typing import Any, List

#---------------------------------------------------------------
#clases abstractas
#---------------------------------------------------------------

@dataclass
class Visitor(metaclass=multimeta):

    def visit(self, node : ClassDeclaration):
        pass

    def visit(self, node : FuncDeclaration):
        pass

    def visit(self, node : Print):
        pass

    def visit(self, node : IfStmt):
        pass

    def visit(self, node : WhileStmt):
        pass

    def visit(self, node : Return):
        pass

    def visit(self, node : ExprStmt):
        pass

    def visit(self, node : Block):
        pass

    def visit(self, node : Literal):
        pass

    def visit(self, node : Binary):
        pass

    def visit(self, node : Logical):
        pass

    def visit(self, node : Unary):
        pass

    def visit(self, node : Grouping):
        pass

    def visit(self, node : Variable):
        pass

    def visit(self, node : Assign):
        pass

    def visit(self, node : Call):
        pass

    def visit(self, node : Get):
        pass

    def visit(self, node : Set):
        pass

    def visit(self, node : This):
        pass

    def visit(self, node : Super):
        pass

    def visit(self, node : List):
        pass


#################################################
@dataclass
class Node:
    def accept(self, vis: Visitor, *args, **kwargs): #no son punteros como en C
        return vis.visit(self, *args, **kwargs)


@dataclass
class Statement(Node):
    pass

@dataclass
class Expression(Node):
    pass

@dataclass
class Declaration(Statement):
    pass




#---------------------------------------------------------------
#  Nodos del Tipo Declaration, son Statement especiales que declaran la existencia de algo
#---------------------------------------------------------------
@dataclass
class ClassDeclaration(Declaration):
    name   : str
    sclass : str
    methods: List[Statement] = field(default_factory=list)


@dataclass
class FuncDeclaration(Declaration):
    name   : str
    parameters: List[Expression] = field(default_factory=list)
    stmts  : List[Statement] = field(default_factory=list)

@dataclass
class VarDeclaration(Declaration):
    name   : str
    expr   : Expression


#---------------------------------------------------------------
# Statement representan acciones sin valores asociados
#---------------------------------------------------------------

@dataclass
class Program(Statement):
    decl   : List[Statement] = field(default_factory=list)

@dataclass
class Print(Statement):
    expr   : Expression

@dataclass
class IfStmt(Statement):
    cond   : Expression
    cons   : List [Statement]=field(default_factory=list) #el consecuente
    altr   : List [Statement]=field(default_factory=list)

@dataclass
class WhileStmt(Statement):
    cond  : Expression
    body  : List[Statement]=field(default_factory=list)

@dataclass
class Return(Statement):
    expr  : Expression

@dataclass
class ExprStmt(Statement):
    expr  : Expression

@dataclass
class Block(Statement):
    stmts :  List[Statement] = field(default_factory=list)

#---------------------------------------------------------------
# Expression representan valores
#---------------------------------------------------------------

@dataclass
class Literal(Expression):
    #todo lo de primary
    value  : Any

@dataclass
class Binary(Expression): #tiene un hijo izquierdo y un hijo derecho, o sea, suma, resta, multiplicación y división
    op     : str
    left   : Expression
    right  : Expression


@dataclass
class Logical(Expression):
    op     : str            # <, <=, >, >=, ==, !=, && , ||
    left   : Expression
    right  : Expression


@dataclass
class Unary(Expression):
    op     : str           # -, !
    expr   : Expression

@dataclass
class Grouping(Expression): # no es obligatorio
    expr  : Expression


@dataclass
class Variable(Expression):
    name   : str

@dataclass
class Assign(Expression):
    name   : str
    expr   : Expression

@dataclass
class Call(Expression):
    func  : Expression
    args  : List[Expression]=field(default_factory=list)


@dataclass
class Set(Expression):
    obj   : str
    name  : str
    expr  : Expression


@dataclass
class Get(Expression):
    obj   : str
    name  : str


@dataclass
class Super(Expression):
    name   : str


@dataclass
class This(Expression):
    pass


#---------------------------------------------------------------
#---------------------------------------------------------------

#más aelante usaremos el Visitor para imprimir el AST de forma bonita usando tree.py
#repositorio de rich en github, el archivo tree
