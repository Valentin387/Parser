from cast import *
import sly
from rich import print
from render import DotRender

from clex import Lexer
from cparse import Parser
from checker import Checker

def examples_sample():
    print("\t WELCOME \n")
    print("you can do the following tests in cmd:")
    print("(1) python context.py fib.mc")
    print("(2) python context.py primos.mc")
    print("\n\n")


if __name__ == '__main__':
    import sys

    #examples_sample()

    if len(sys.argv) != 2:
        print('Usage: python cparse.py filename')
        exit(0)

    l = Lexer()     # Analizador Lexico
    p = Parser()    # Analizador Sintactico

    #we'll start to build our AST
    ast = p.parse(
        l.tokenize(open(sys.argv[1], encoding='utf-8').read())
    )
    print("\n\n\t\t************ AST ************ \n\n")
    print(ast)
    print("\n\n")

    dot = DotRender.render(ast) #render
    print(dot)
    print("\n")

    Checker().check(ast) # Analizador semántico
