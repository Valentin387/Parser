import math


class CallError(Exception):
	pass

class Format:
	def __call__(self, interp, *args):
		print(args[1:])
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
	'NAN':math.nan
}
