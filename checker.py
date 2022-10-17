# checker.py

from cast import *

# ---------------------------------------------------------------------
#  Tabla de Simbolos
# ---------------------------------------------------------------------

class Symtab:
    '''
    Una tabla de símbolos.  Este es un objeto simple que sólo
    mantiene una hashtable (dict) de nombres de simbolos y los
    nodos de declaracion o definición de funciones a los que se
    refieren.
    Hay una tabla de simbolos separada para cada elemento de
    código que tiene su propio contexto (por ejemplo cada función,
    clase, tendra su propia tabla de simbolos). Como resultado,
    las tablas de simbolos se pueden anidar si los elementos de
    código estan anidados y las búsquedas de las tablas de
    simbolos se repetirán hacia arriba a través de los padres
    para representar las reglas de alcance léxico.
    '''
    class SymbolDefinedError(Exception):
        '''
        Se genera una excepción cuando el código intenta agregar
        un simbol a una tabla donde el simbol ya se ha definido.
        Tenga en cuenta que 'definido' se usa aquí en el sentido
        del lenguaje C, es decir, 'se ha asignado espacio para el
        simbol', en lugar de una declaración.
        '''
        pass

    class SymbolConflitError(Exception):
        '''
        Se genera una excepción cuando el código intenta agregar
        un símbol a la tabla donde el simbol ya existe y su tipo
        difiere del existente anteriormente
        '''
        pass

    def __init__(self, parent=None):
        '''
        Crea una tabla de símbolos vacia con la tabla de
        simbolos padre dada.
        '''
        self.entries = {}
        self.parent = parent
        if self.parent:
            self.parent.children.append(self)
        self.children = []

    def add(self, name, value):
        '''
        Agrega un simbol con el valor dado a la tabla de simbolos.
        El valor suele ser un nodo AST que representa la declaración
        o definición de una función, variable (por ejemplo, Declaración
        o FuncDeclaration)
        '''
        if name in self.entries:
            raise Symtab.SymbolDefinedError()
        self.entries[name] = value

    def get(self, name):
        '''
        Recupera el símbol con el nombre dado de la tabla de
        simbol, recurriendo hacia arriba a traves de las tablas
        de simbol principales si no se encuentra en la actual.
        '''
        if name in self.entries:
            return self.entries[name]
        elif self.parent:
            return self.parent.get(name)
        return None

class Checker(Visitor):
    '''
    Visitante que crea y enlaza tablas de simbolos al AST
    '''
    def push_symtab(self, node):
        '''
        Inserta una nueva tabla de símbolos en la pila de
        tablas de símbolos del visitante y adjunta esta tabla
        de símbolos al nodo dado.  Esto se usa cada vez que
        se encuentra un nuevo ámbito léxico, por lo que el
        nodo suele ser un objeto Statements.
        '''
        self.curr_symtab = Symtab(self.curr_symtab)
        node.symtab = self.curr_symtab

    def pop_symtab(self):
        '''
        Saca una tabla de símbolos de la pila de tablas de
        símbolos del visitante.  Esto se usa cada vez que
        se sale de un nuevo ámbito léxico.
        '''
        self.curr_symtab = self.curr_symtab.parent

    def _add_symbol(self, node):
        '''
        Intenta agregar un símbolo para el nodo dado a
        la tabla de símbolos actual, capturando cualquier
        excepción que ocurra e imprimiendo errores si es
        necesario.
        '''
        try:
            self.curr_symtab.add(node.name, node)
        except Symtab.SymbolDefinedError:
            self.error(f"Simbol '{node.name}' esta definido.")
        except Symtab.SymbolConflictError:
            self.error("Simbol '{node.name}' tiene multiples declaraciones diferentes.")

    @classmethod
    def check(cls, model, env: Symtab):
        checker = cls()
        model.accept(checker, env)
        return checker

    # nodos de Declaration

    def visit(self, node: ClassDeclaration, env: Symtab):
        '''
		1. Agregar el nombre de la clase a la tabla de simbolos actual
		2. Si esta definida la superclass, buscarla. Si no se encuentra,
		   especificar un error.
		3. Crear una nueva tabla de simbolos (contexto)
		4. Visitar la definicion de metodos de la clase.
		'''
        pass

    def visit(self, node: FuncDeclaration, env: Symtab):
        '''
		1. Agregar el nombre de la función a la tabla de simbolos actual
		2. Crear una nueva tabla de simbolos (contexto)
		3. Agregamos los parametros a la nueva tabla de simbolos
		4. Visitar cada una de las instrucciones del cuerpo de la funcion
		'''
        pass

    def visit(self, node: VarDeclaration, env: Symtab):
        '''
		1. Agregar el nombre de la variable a la tabla de simbolos actual
		2. Visitar la expresion, si esta definida
		'''
        pass

    # Statement

    def visit(self, node: Block, env: Symtab):
        '''
		1. Visitar cada una de las instrucciones
		'''
        pass

    def visit(self, node: Print, env: Symtab):
        '''
		1. Visitar expresion
		'''
        pass

    def visit(self, node: IfStmt, env: Symtab):
        '''
		1. Visitar la condicion
		2. Visitar las instrucciones del then
		3. Visitar las instrucciones del opt, si esta definido
		'''
        pass

    def visit(self, node: WhileStmt, env: Symtab):
        '''
		1. Visitar la condicion
		2. Visitar las instrucciones del cuerpo
		Nota : ¿Generar un nuevo contexto?
		'''
        pass

    def visit(self, node: Return, env: Symtab):
        '''
		1. Visitar expresion
		'''
        pass

    def visit(self, node: ExprStmt, env: Symtab):
        '''
		1. Visitar expresion
		'''
        pass


    # Expression

    def visit(self, node: Literal, env: Symtab):
        '''
		No se hace nada
		'''
        pass

    def visit(self, node: Binary, env: Symtab):
        '''
		1. Visitar el hijo izquierdo
		2. Visitar el hijo derecho
		'''
        pass

    def visit(self, node: Logical, env: Symtab):
        '''
		1. Visitar el hijo izquierdo
		2. Visitar el hijo derecho
		'''
        pass

    def visit(self, node: Unary, env: Symtab):
        '''
		1. Visitar expresion
		'''
        pass

    def visit(self, node: Grouping, env: Symtab):
        '''
        1. Visita Expresion
        '''
        pass

    def visit(self, node: Variable, env: Symtab):
        '''
		1. Buscar nombre en la tabla de simbolos (contexto actual)
		'''
        pass

    def visit(self, node: Assign, env: Symtab):
        '''
		1. Visitar el hijo izquierdo (OJO)
		2. Visitar el hijo derecho
		'''
        pass

    def visit(self, node: Call, env: Symtab):
        '''
        1. Buscar la funcion en la tabla de simbolos
        2. Validar el numero de argumentos pasados
        3. Visitar las expr de los argumentos
		'''
        pass

    def visit(self, node: Get, env: Symtab):
        '''
		1. Buscar objeto en la tabla de simbolos (contexto actual)
		2. Buscar nombre en la tabla de simbolos (contexto actual)
		'''
        pass

    def visit(self, node: Set, env: Symtab):
        '''
		1. Buscar objeto en la tabla de simbolos (contexto actual)
		2. Buscar nombre en la tabla de simbolos (contexto actual)
		3. Visitar expresion
		'''
        pass

    def visit(self, node: This, env: Symtab):
        '''
		No hacemos nada (debe de estar en un contexto de una clase)
		'''
        pass

    def visit(self, node: Super, env: Symtab):
        '''
		1. Buscar nombre en la tabla de simbolos (contexto actual)
		Debe de estar en el contexto de una clase
		'''
        pass
checker.py
Mostrando checker.py.
