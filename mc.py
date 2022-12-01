#import docopt
#from argparse import ArgumentParser
from context2 import Context
from rich import print
from render import DotRender
#from rich import print
from tabulate import tabulate

"""
    print("optional arguments:")
    print("-h, --help             show this help message and exit")
    print("-d, --debug            Generate assembly with extra information (for debugging purposes)")
    print("-o OUT, --out OUT      File name to store generated executable")
    print("-l, --lex              Store output of lexer")
    print("-a, --AST              Display AST")
    print("-D, --dot              Generate AST graph as DOT format")
    print("-p, --png              Generate AST graph as png format")
    print("-I, --ir               Dump the generated Intermediate representation")
    print("--sym                  Dump the symbol table") #the Checker one
    print("-S, --asm              Store the generated assembly file")
    print("-R, --exec             Execute the generated program")
"""
def menu():
    print("\t\t\t\n ################################ Valentin's MiniC Compiler ################################  \n")
    print("usage: mc.py [-h] [-d] [-o OUT] [-l] [-a] [-D] [-p] [-I] [--sym] [-S] [-R] input\n")

    print("Compiler for MiniC programs\n")

    print("positional arguments:")
    print("input MiniC            program file to compile\n")

    print("optional arguments:")
    print("-h, --help             show this help message and exit")
    print("-l, --lex              display tokens from lexer")
    print("-a, --AST              Display AST")
    print("-D, --dot              Generate AST graph as DOT format")
    #print("-p, --png              Generate AST graph as png format")
    print("--sym                  Dump the symbol table") #the Checker one
    print("-R, --exec             Execute the generated program")


def main(argv):
    if len(argv) == 2:
        menu()
        raise SystemExit()

    print("\t\t\t\n ################################ Valentin's MiniC Compiler ################################  \n")
    ctxt = Context()
    if len(argv) > 2:
        source = ""
        with open(argv[2]) as file:
            source = file.read()
        ctxt.parse(source)
        if not ctxt.have_errors:
            if argv[1] in ["-h","--help"]:
                menu()
                #raise SystemExit()
            elif argv[1] in ["-l","--lex"]:
                print("\n\n\t\t********** TOKENS ********** \n\n")
                tokens = ctxt.lexer.tokenize(source)
                table=[["Type","Value","At line"]]
                for tok in tokens:
                    row=[]
                    row.append(tok.type)
                    row.append(tok.value)
                    row.append(tok.lineno)
                    table.append(row)
                print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
            elif argv[1] in ["-a","--AST"]:
                print("\n\n\t\t********** AST ********** \n\n")
                print(ctxt.ast)
            elif argv[1] in ["-D","--dot"]:
                print("\n\n DOT LANGUAGE \n")
                dot = DotRender.render(ctxt.ast) #render
                print(dot)
            elif argv[1] in ["-s","--sym"]:
                print(ctxt.interp.env)
            elif argv[1] in ["-R", "--exec"]:
                print("\n CHECKER + INTERPRETER \n")
                ctxt.run()
            else:
                print("Not defined action")
                op = int(input("Do you need help? 1:yes/2:no :: "))
                if op == 1:
                    menu()
    else:
        try:
            while True:
                source = input("mc > ") #This one works for very simple one line stuff, but the environments of neither Checker or Interpret work properly.
                ctxt.parse(source)
                if ctxt.have_errors: continue
                for stmt in ctxt.ast.decl:
                    ctxt.ast = stmt
                    ctxt.run()

        except EOFError:
            pass

if __name__ == "__main__":
    from sys import argv
    main(argv)
