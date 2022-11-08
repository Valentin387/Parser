# mc.py
'''
usage: mc.py [-h] [-d] [-o OUT] [-l] [-D] [-p] [-I] [--sym] [-S] [-R] input

Compiler for MiniC programs

positional arguments:
  input              MiniC program file to compile

optional arguments:
  -h, --help         show this help message and exit
  -d, --debug        Generate assembly with extra information (for debugging
                     purposes)
  -o OUT, --out OUT  File name to store generated executable
  -l, --lex          Store output of lexer
  -D, --dot          Generate AST graph as DOT format
  -p, --png          Generate AST graph as png format
  -I, --ir           Dump the generated Intermediate representation
  --sym              Dump the symbol table
  -S, --asm          Store the generated assembly file
  -R, --exec         Execute the generated program
'''
import docopt

from argparse import ArgumentParser
from context2 import Context
from rich import print


def main(argv):
    if len(argv) > 2:
        raise SystemExit(f'usage: mc.py filename')

    ctxt = Context()
    if len(sys.argv) == 2:
        with open(argv[1], enconding='utf-8') as file:
            source = file.read()
        ctxt.parse(source)
        print("\n\n\t\t********** AST ********** \n\n")
        print(ctxt.parser.ast)
        print("\n\n")
        dot = DotRender.render(ast) #render
        print(dot)
        print("\n")

        ctxt.run()

    else:
        try:
            while True:
                source = input("mc > ")
                ctxt.parse(source)
                if ctxt.have_errors: continue
                for stmt in ctxt.ast.stmts:
                    ctxt.ast = stmt
                    ctxt.run()

        except EOFError:
            pass

if __name__ == "__main__":
    from sys import argv

    main(argv)
