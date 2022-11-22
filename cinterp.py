# cinterp.py
'''
Tree-walking interpreter
'''
from collections import ChainMap
from cast    import *
from checker import Checker
from rich    import print

import math

# Veracidad en MiniC
def _is_truthy(value):
	if isinstance(value, bool): #If the object is already a boolean
		return value
	elif value is None: # if the object is empty
		return False
	else:
		return True #if the object is not empty

class ReturnException(Exception):
	def __init__(self, value):
		self.value = value	#it sets the value for exception

class MiniCExit(BaseException):
	pass

class CallError(Exception):
	pass

class AttributeError(Exception):
	pass

class Function:
	def __init__(self, node, env): #it receives the node and a context
		self.node = node
		self.env = env

	def __call__(self, interp, *args): #it receives the interpreter and a tuple
		if self.node.parameters is not None:
			if len(args) != len(self.node.parameters):
				raise CallError(f"Interp Error. Expected {len(self.node.parameters)} arguments")
		newenv = self.env.new_child() #we create a new environment
		if self.node.parameters is not None:
			for name, arg in zip(self.node.parameters, args):
				newenv[name] = arg

		oldenv = interp.env #we update the interpreter's environment
		interp.env = newenv
		try:
			interp.visit(self.node.stmts)
			result = None
		except ReturnException as e:
			result = e.value
		finally:
			interp.env = oldenv #we reset the last fully functional environment
		return result #returns Function exceptions

	def bind(self, instance): #I receive something called instance
		env = self.env.new_child() #I create a new environment
		env['this'] = instance #we add a new value for key 'this'
		return Function(self.node, env)


class Class:
	def __init__(self, name, sclass, methods): #this is a Class framework for any class
		self.name = name
		self.sclass = sclass
		self.methods = methods

	def __str__(self): #returns the string representation of the object
		return self.name

	def __call__(self, *args): #this class and can be called like a function.  Class()
		this = Instance(self)
		init = self.find_method('init')
		if init:
			init.bind(this)(*args) #I re-define the use for 'This'
		return this

	def find_method(self, name):
		meth = self.methods.get(name)
		if meth is None and self.sclass:
			return self.sclass.find_method(name)
		return meth

class Instance:
	def __init__(self, klass):
		self.klass = klass
		self.data = { }

	def __str__(self):
		return self.klass.name + " instance"

	def get(self, name):
		if name in self.data:
			return self.data[name]
		method = self.klass.find_method(name)
		if not method:
			raise AttributeError(f'interp Error, Not defined property {name}')
		return method.bind(self)

	def set(self, name, value):
		self.data[name] = value


class Interpreter(Visitor): #This is a visitor
	def __init__(self, ctxt):
		self.ctxt = ctxt 				#receives a Context (the project's manager)
		self.env  = ChainMap()			#generates ChainMap

	def _check_numeric_operands(self, node, left, right):
		if isinstance(left, (int, float)) and isinstance(right, (int, float)):
			return True
		else:
			self.error(node, f"Interp Error. In '{node.op}' the operands must be numerical type")

	def _check_numeric_operand(self, node, value):
		if isinstance(value, (int, float)):
			return True
		else:
			self.error(node, f"Interp Error. In '{node.op}' the operand must be numerical type")

	def error(self, position, message):
		self.ctxt.error(position, message)
		raise MiniCExit()

	# Punto de entrada alto-nivel
	def interpret(self, node):
		try:
			Checker.check(node, self.ctxt) #First, you must call the Checker
			if not self.ctxt.have_errors:
				print("Starting interptreting \n")
				self.visit(node)
				print("\nInterpreting finished")
			else:
				print("\n The interpreter could not start because the Checker returned errors")
		except MiniCExit as e:
			pass

	def visit(self, node: Block):
		#self.env = self.env.new_child() #think about it as a typewriter, it advances one row
										#and then you have to reset the pointer
		for stmt in node.stmts:
			self.visit(stmt)
		#self.env = self.env.parents		#you "reset" the pointer

	def visit(self, node: Program):
		#self.env = self.env.new_child()
		for d in node.decl:
			self.visit(d)
		#self.env = self.env.parents

	def visit(self, node: ClassDeclaration):
		if node.sclass:
			sclass = self.visit(node.sclass)
			env = self.env.new_child()
			env['super'] = sclass			#we accommodate this framework for any User-made class
		else:
			sclass = None
			env = self.env
		methods = { }
		for meth in node.methods:
			methods[meth.name] = Function(meth, env)
		cls = Class(node.name, sclass, methods)
		self.env[node.name] = cls

	def visit(self, node: FuncDeclaration):

		func = Function(node, self.env)
		self.env[node.name] = func

	def visit(self, node: VarDeclaration):
		if node.expr:
			expr = self.visit(node.expr)
		else:
			expr = None
		self.env[node.name] = expr

	def visit(self, node: Print):
		print(self.visit(node.expr))

	def visit(self, node: WhileStmt):
		while _is_truthy(self.visit(node.cond)):
			self.visit(node.body)

	def visit(self, node: ForStmt):
		self.visit(node.for_init)
		while _is_truthy(self.visit(node.for_cond)):
			self.visit(node.for_body)
			self.visit(node.for_increment)

	def visit(self, node: IfStmt):
		test = self.visit(node.cond)
		if _is_truthy(test):
			self.visit(node.cons)
		elif node.altr:
			self.visit(node.altr)

	def visit(self, node: Return):
		raise ReturnException(self.visit(node.expr))

	def visit(self, node: ExprStmt):
		self.visit(node.expr)

	def visit(self, node: Literal):
		return node.value

	def visit(self, node: Binary):
		left  = self.visit(node.left)
		right = self.visit(node.right)
		if node.op == '+':
			(isinstance(left, str) and isinstance(right, str)) or self._check_numeric_operands(node, left, right)
			return left + right
		elif node.op == '-':
			self._check_numeric_operands(node, left, right)
			return left - right
		elif node.op == '*':
			self._check_numeric_operands(node, left, right)
			return left * right
		elif node.op == '/':
			self._check_numeric_operands(node, left, right)
			return left / right
		elif node.op == '%':
			self._check_numeric_operands(node, left, right)
			return left % right
		elif node.op == '==':
			return left == right
		elif node.op == '!=':
			return left != right
		elif node.op == '<':
			self._check_numeric_operands(node, left, right)
			return left < right
		elif node.op == '>':
			self._check_numeric_operands(node, left, right)
			return left > right
		elif node.op == '<=':
			self._check_numeric_operands(node, left, right)
			return left <= right
		elif node.op == '>=':
			self._check_numeric_operands(node, left, right)
			return left >= right
		else:
			raise NotImplementedError(f"Interp Error. Wrong Operator {node.op}")

	def visit(self, node: Logical):
		left = self.visit(node.left)
		if node.op == '||':
			return left if _is_truthy(left) else self.visit(node.right)
		if node.op == '&&':
			return self.visit(node.right) if _is_truthy(left) else left
		raise NotImplementedError(f"Interp Error. Wrong Operator {node.op}")

	def visit(self, node: Unary):
		expr = self.visit(node.expr)
		if node.op == "-":
			self._check_numeric_operand(node, expr)
			return - expr
		elif node.op == "!":
			return not _is_truthy(expr)
		else:
			raise NotImplementedError(f"Interp Error. Wrong Operator {node.op}")

	def visit(self, node: Grouping):
		return self.visit(node.expr)

	def visit(self, node: Assign):
		expr = self.visit(node.expr)
		self.env[node.name] = expr

	def visit(self, node: Call):
		callee = self.visit(node.func)
		if not callable(callee):
			self.error(node.func, f'Interp Error {self.ctxt.find_source(node.func)!r} is not callable')

		if node.args is not None:
			args = [ self.visit(arg) for arg in node.args ]
		else:
			args = []
		try:
			return callee(self, *args)
		except CallError as err:
			self.error(node.func, str(err))

	def visit(self, node: Variable):
		return self.env[node.name]

	def visit(self, node: Set):
		obj = self.visit(node.obj)
		val = self.visit(node.expr)
		if isinstance(obj, Instance):
			obj.set(node.name, val)
			return val
		else:
			self.error(node.obj, f'Interp Error{self.ctxt.find_source(node.obj)!r} is not an instance')

	def visit(self, node: Get):
		obj = self.visit(node.obj)
		if isinstance(obj, Instance):
			try:
				return obj.get(node.name)
			except AttributeError as err:
				self.error(node.obj, str(err))
		else:
			self.error(node.obj, f'Interp Error{self.ctxt.find_source(node.obj)!r}  is not an instance')

	def visit(self, node: This):
		return self.env['this']

	def visit(self, node: Super):
		distance = self.localmap[id(node)]
		sclass = self.env.maps[distance]['super']
		this = self.env.maps[distance-1]['this']
		method = sclass.find_method(node.name)
		if not method:
			self.error(node.object, f'Interp Error. Not defined property {node.name!r}')
		return method.bind(this)
