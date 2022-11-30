import math
import time

class CallError(Exception):
	pass

class IsStr:
	def __call__(self, interp, *args):
		if len(args) != 1:
			raise CallError("'IsStr' only receives 1 argument")
		if isinstance(args[0], (str)):
			return True
		else:
			return False

	def __str__(self):
		return '<builtins: IsStr>'

class IsFloat:
	def __call__(self, interp, *args):
		if len(args) != 1:
			raise CallError("'IsFloat' only receives 1 argument")
		if isinstance(args[0], (float)):
			return True
		else:
			return False

	def __str__(self):
		return '<builtins: IsFloat>'

class IsInteger:
	def __call__(self, interp, *args):
		if len(args) != 1:
			raise CallError("'isInteger' only receives 1 argument")
		if isinstance(args[0], (int)):
			return True
		else:
			return False

	def __str__(self):
		return '<builtins: isInteger>'

class Input:
	def __call__(self, interp, *args):
		print(args[0], end="")
		information = input()
		try:
			information = int(information)
			return information #it is int
		except ValueError:
			try:
				information = float(information)
				return information #it's float
			except ValueError:
				return information #it's string

	def __str__(self):
		return '<builtins: input>'

class Len:
	def __call__(self, interp, *args):
		if not isinstance(args[0], (str)):
			raise CallError("'len' argument must be str type")
		if len(args) != 1:
			raise CallError("'len' only receives 1 argument")
		if isinstance(args[0], (str)):
			return len(args[0])-2

	def __str__(self):
		return '<builtins: Len>'

class Clock:
	def __call__(self, interp, *args):
		if not isinstance(args[0], (int)):
			raise CallError("'clock' argument must be int type")
		if len(args) != 1:
			raise CallError("'clock' only receives 1 argument")
		if args[0] == 0:
			return time.process_time()
		elif args[0] == 1:
			return time.perf_counter()
		else:
			raise CallError("'clock' only receives 1:perf_counter or 0:process_time")

	def __str__(self):
		return '<builtins: Clock>'
#(1) perf_counter() -> does include time elapsed during sleep
#(0) process_time() -> does NOT include time elapsed during sleep
#--sleep refers to dead time, like the system waiting a user input


class Format:
	def __call__(self, interp, *args):
		if not isinstance(args[0], (str)):
			raise CallError("'format' argument must be string type ")
		if args[0].count('%') != len(args[1:]):
			raise CallError("'format' mismatch in arguments ")
		#string formatting operator
		return args[0].replace('\\n','\n') % args[1:]

	def __str__(self):
		return '<builtins: Format>'
"""
%s - String (or any object with a string representation, like numbers)
%d - Integers
%f - Floating point numbers
%.<number of digits>f - Floating point numbers with a fixed amount of digits to the right of the dot.
%x/%X - Integers in hex representation (lowercase/uppercase)
"""
class ArcTang:
    def __call__(self, interp, *args):
        if len(args) != 1:
            raise CallError("Error in argument in 'atan' ")
        if not isinstance(args[0], (int, float)):
            raise CallError("'atan' argument must be number type ")
        return math.atan(args[0])

    def __str__(self):
        return '<builtins: atan>'

class Logarithm:
    def __call__(self, interp, *args):
        if len(args) != 1:
            raise CallError("Error in argument in 'log' ")
        if not isinstance(args[0], (int, float)):
            raise CallError("'atan' argument must be number type ")
        return math.log(args[0])

    def __str__(self):
        return '<builtins: log>'

stdlibFunctions = {

    'format':Format(),
    'atan':ArcTang(),
    'log':Logarithm(),
	'PI':math.pi,
	'EULER':math.e,
	'TAU':math.tau,
	'INF':math.inf,
	'NAN':math.nan,
	'clock':Clock(),
	'len':Len(),
	'input':Input(),
	'isInteger':IsInteger(),
	'isFloat':IsFloat(),
	'isStr':IsStr()
}
