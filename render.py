# render.py
from cast import *
from graphviz import Digraph


class DotRender(Visitor):
    node_default = {
        'shape' : 'box',
        'color' : 'deepskyblue',
        'style' : 'filled',
    }
    edge_defaults = {
        'arrowhead' : 'none',
    }
    color = 'chartreuse'

    def __init__(self):
        self.dot = Digraph('AST')
        self.dot.attr('node', **self.node_default)
        self.dot.attr('edge', **self.edge_defaults)
        self.program = False
        self.seq = 0

    def __repr__(self):
        return self.dot.source

    def __str__(self):
        return self.dot.source

    @classmethod
    def render(cls, model):
        dot = cls()
        model.accept(dot)
        return dot.dot

    def name(self):
        self.seq +=1
        return f'n{self.seq:02d}'

    # nodos de Declaration

    def visit(self, node : ClassDeclaration):
        name = self.name()
        self.dot.node(name, label=f"ClassDeclaration\nname='{node.name}' - {node.sclass}")
        for meth in node.methods:
            self.dot.edge(name, meth.accept(self))
        return name

    def visit(self, node : FuncDeclaration):
        name = self.name()
        self.dot.node(name,
            label=f"FuncDeclaration\nname:'{node.name}'\nparams: {node.params}",
            color=self.color)
        self.dot.edge(name, node.stmts.accept(self))
        return name

    def visit(self, node : VarDeclaration):
        name = self.name()
        self.dot.node(name,
            label=f"VarDeclaration\nname={node.name}",
            color=self.color)
        if node.expr:
            self.dot.edge(name, self.visit(node.expr), label='init')
        return name

    # Statement

    def visit(self, node : Print):
        name = self.name()
        self.dot.node(name,
            label='Print',
            color=self.color)
        self.dot.edge(name, self.visit(node.expr))
        return name

    def visit(self, node : IfStmt):
        name = self.name()
        self.dot.node(name,
            label='IfStmt',
            color=self.color)
        self.dot.edge(name, node.test.accept(self), label='test')
        self.dot.edge(name, node.cons.accept(self), label='then')
        if node.altr:
            self.dot.edge(name, node.altr.accept(self), label='else')
        return name

    def visit(self, node : WhileStmt):
        name = self.name()
        self.dot.node(name,
            label='WhileStmt',
            color=self.color)
        self.dot.edge(name, self.visit(node.test), label='test')
        self.dot.edge(name, self.visit(node.body), label='body')
        return name

    def visit(self, node : Return):
        name = self.name()
        self.dot.node(name,
            label='Return',
            color=self.color)
        if node.expr:
            self.dot.edge(name, self.visit(node.expr))
        return name

    def visit(self, node : ExprStmt):
        name = self.name()
        self.dot.node(name,
            label='ExprStmt',
            color=self.color)
        self.dot.edge(name, self.visit(node.expr))
        return name

    def visit(self, node : Statement):
        name  = self.name()
        label = 'Statements'
        if not self.program:
            self.program = True
            label = 'Program'
        self.dot.node(name,
            label=label,
            color=self.color)
        for stmt in node.stmts:
            self.dot.edge(name, self.visit(stmt))
        return name

    # Expression

    def visit(self, node : Literal):
        name = self.name()
        value = node.value
        if node.value is None:
            value = "nil"
        elif node.value is True:
            value = "true"
        elif node.value is False:
            value = "false"
        self.dot.node(name, label=f"Literal\nvalue={value}")
        return name

    def visit(self, node : Binary):
        name = self.name()
        self.dot.node(name, label=f"'{node.op}'")
        self.dot.edge(name, self.visit(node.left))
        self.dot.edge(name, self.visit(node.right))
        return name

    def visit(self, node : Logical):
        name = self.name()
        self.dot.node(name, label=f"'{node.op}'")
        self.dot.edge(name, self.visit(node.left))
        self.dot.edge(name, self.visit(node.right))
        return name

    def visit(self, node: Unary):
        name = self.name()
        self.dot.node(name, label=f'{node.op}')
        self.dot.edge(name, self.visit(node.expr))
        return name

    def visit(self, node : Grouping):
        name = self.name()
        self.dot.node(name, label='Grouping')
        self.dot.edge(name, self.visit(node.expr))
        return name

    def visit(self, node : Variable):
        name = self.name()
        self.dot.node(name, label=f"{node.name}")
        return name

    def visit(self, node : Assign):
        name = self.name()
        self.dot.node(name, label=f"Assign\nname: '{node.name}'")
        self.dot.edge(name, self.visit(node.expr))
        return name

    def visit(self, node : Call):
        name = self.name()
        self.dot.node(name, label=f"Call")
        self.dot.edge(name, self.visit(node.func))
        for arg in node.args:
            self.dot.edge(name, self.visit(arg))
        return name

    """
    def visit(self, node : Bltin):
        name = self.name()
        self.dot.node(name, label=f"Bltin\nname: {node.name}")
        self.dot.edge(name, self.visit(node.expr))
        return name
    """
    def visit(self, node : Block):
        name = self.name()
        self.dot.node(name, label=f"Block\nname: {node.name}")
        self.dot.edge(name, self.visit(node.expr))
        return name

    def visit(self, node : Get):
        name = self.name()
        self.dot.node(name, label='')

        f'(get {self.visit(node.object)} {node.name})'
        return name

    def visit(self, node : Set):
        name = self.name()
        self.dot.node(name, label='')
        f'(set {self.visit(node.object)} {node.name} {self.visit(node.value)})'
        return name

    def visit(self, node : This):
        name = self.name()
        self.dot.node(name, label='this')
        return name

    def visit(self, node : Super):
        name = self.name()
        self.dot.node(name, label=f'super {node.name}')
        return name

    def visit(self, node : List):
        name = self.name()
        self.dot.node(name, label=f'super {node.name}')
        return name
