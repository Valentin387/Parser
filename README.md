# Parser
My first parser

INFORMATION ABOUT BRANCHES

*main
teacher example for a calculator

*desktopBranch01
it's the same as 'main' but with an update in "def factor()"

*McFly01
Prototype, intermediate for McFly02

*McFly02*
fully operational program, it reads a list os expressions, the list can be empty, I have to use some programming tricks but it works fine

Example for CMD:
Input: 1
1.0
Input: 2
2.0
Input:
Input:
Input:
Input:
Input: a=1
1.0
Input: b=2
2.0
Input: c=a+b
3.0
Input: d=-(4+1*(6/3-1))
-5.0
Input:

*cparserBranch01

example: python cparse.py text.mc

This one uses SLY, everything looks good, I only have to solve the infinite recursion problem

*AST01

First fully functional version at commit "finally the parser works"

*renderDesktop01

Thanks to professeur, the AST is starting to grow good

*grammar2_v01

The first light at the end of the tunnel

*laptop_Oct_26

I started to parse XD the Camila's version

This branch has the first fully functional lexer, parser, ast, render & checker
______________

* (FinalProject_v1)

I start to work in final delivery of the compiler

* (FinalProject_v2)
I created this branch after being successful with a first version of the interpreter
Point 1 and 2 successfully implemented:

1. operadores de asignacion: 
  +=, -=, *=, /=, %=

2. operadores de incremento (++) y decremento (--)
   Notacion: prefija y sufija

   prefijo:  var a = 12;
            var b = ++a;    // b = 13, a = 13

   postfijo  var a = 12;
             var b = a++;   // b = 12, a = 13 

* (FinalProject_v3)
Point 1, 2 and 3 successfully implemented:

    Incorporar las instrucciones break y continue
   Nota: Solo deben de aparecer dentro de un bucle
   
______________

* (FinalProject_v4)
