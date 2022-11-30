import math

class Format:
    def __call__(self, interp, *args):

        return args[0]

    def __str__(self):
        return '<builtins: Format>'

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
    'log':Logarithm()
}
