'''
topdown.py

Analizador Descendente Recursivo para la siguiente gramatica

assign ::= 'IDEN' '=' expr

expr ::= term '+' expr
       | term '-' expr
       | term


term ::= factor '*' term
       | factor '/' term
       | factor '%' term
       | factor


factor ::= NUMBER
         | '-' factor
         | '(' expr ')'
'''
from dataclasses import dataclass

import re

# =====================================================================
# Analisis Lexico
# =====================================================================
@dataclass
class Token:
    '''
    Representacion de un Simbol Terminal
    '''
    type  : str
    value : str or float
    lineno: int = 1


class Tokenizer:

    tokens = [
        (r'\s+', None),
        (r'\d+(\.\d+)?(E[-+]?\d+)?', lambda s,tok: Token('NUMBER', float(tok))),
        (r'[a-zA-Z_]\w*',            lambda s,tok: Token('IDENT', tok)),
        (r'\+',                      lambda s,tok: Token('+', tok)),
        (r'-',                       lambda s,tok: Token('-', tok)),
        (r'\*',                      lambda s,tok: Token('*', tok)),
        (r'/',                       lambda s,tok: Token('/', tok)),
        (r'%',                       lambda s,tok: Token('%', tok)),
        (r'=',                       lambda s,tok: Token('=', tok)),
        (r'\(',                       lambda s,tok: Token('(', tok)),
        (r'\)',                       lambda s,tok: Token(')', tok)),
        (r'.',                       lambda s,tok: print(f"Error: Caracter ilegal '{tok}'"))]

    def tokenize(self, txt):
        scanner = re.Scanner(self.tokens)
        result, _ = scanner.scan(txt)
        return iter(result)


# =====================================================================
# Analizador Descendente Recursivo
# =====================================================================
class RecursiveDescendentParser:
    '''
    Implementacion de un Analizador Descendente Recursivo.  Cada
    metodo implementa una sola regla de la gramatica.

    Use el metodo `._accept()` para aprobar y aceptar el token
    actualmente leido.
    Use el metodo `._expect()` para coincidir y descartar exactamente
    el token siguiente en la entrada (o levantar un SystAXError si no
    coincide).

    El atributo `.tok` contiene el ultimo token aceptado. El atributo
    `.nexttok` contiene el siguiente toekn leido.
    '''
    def assign(self):
        '''
        assign ::= IDENT '=' expr
        '''
        if self._accept('IDENT'):
            name = self.tok.value
            self._expect('=')
            mem[name] = self.expr()
            return mem[name]
        else:
            raise SyntaxError("Esperando 'IDENT'")

    def expr(self):
        '''
        expr ::= term { ( '+' | '-' ) term }
        '''
        expr = self.term()
        while self._accept('+') or self._accept('-'):
            oper  = self.tok.value
            if oper == '+':
                expr += self.term()
            else:
                expr -= self.term()
        return expr

    def term(self):
        '''
        term ::= factor { ( '*' | '/' | '%' ) factor }
        '''
        term = self.factor()
        while self._accept('*') or self._accept('/') or self._accept('%'):
            oper  = self.tok.value
            if oper == '*':
                term *= self.factor()
            elif oper == '/':
                term /= self.factor()
            else:
                term %= self.factor()

        return term

    def factor(self):
        '''
        factor ::= '-'? ( IDENT | NUMBER | '(' expr ')' )
        '''

        if self._accept('-'):
            if self._accept('IDENT'): #it works
                return -1*mem[self.tok.value]
            elif self._accept('NUMBER'): #it works
                return -1*self.tok.value
            elif self._accept('('):
                expr = self.expr()
                self._expect(')')
                return expr
            else:
                raise SyntaxError("Esperando IDENT, NUMBER o (")

        elif self._accept('IDENT'):
            return mem[self.tok.value]
        elif self._accept('NUMBER'):
            return self.tok.value
        elif self._accept('('):
            expr = self.expr()
            self._expect(')')
            return expr
        else:
            raise SyntaxError("Esperando IDENT, NUMBER o (")

    # -----------------------------------------------------------------
    # Funciones de Utilidad. No debe cambiar nada

    def _advanced(self):
        'Avanza el tokenizer en un simbol'
        self.tok, self.nexttok = self.nexttok, next(self.tokens, None)

    def _accept(self, toktype):
        'Consume el siguiente token si coincide con el tipo esperado'
        if self.nexttok and self.nexttok.type == toktype:
            self._advanced()
            return True
        else:
            return False

    def _expect(self, toktype):
        'Consume o descarta el siguiente token o raise SyntaxError'
        if not self._accept(toktype):
            raise SyntaxError(f"Se esperaba '{toktype}")


    def start(self):
        'Punto de entrada al parser'
        self._advanced()
        return self.assign()

    def parse(self, tokens):
        'Punto de entrada'
        self.tok = None             # Ultimo simbol consumido
        self.nexttok = None         # Siguiente simbol tokinizado
        self.tokens = tokens
        return self.start()

# Tabla de simbolos (memoria)
mem = {}

lex   = Tokenizer()
parser= RecursiveDescendentParser()

while True:
    try:
        text = input("Calc ")
        print(parser.parse(lex.tokenize(text)))
    except KeyError:
        break
