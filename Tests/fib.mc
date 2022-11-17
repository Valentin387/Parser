/*
fib.mc

calcula el n-esimo número de la secuencia de Fibonacci

main
for (var i = 1; i < 20; i = i + 1) {
  print(fib(i));
}

*/

fun fib(n){
  if (n <= 1){
    return 1;
  }else{
    return fib(n-1) + fib(n-2);
  }
  end_if
  //return 0;
}

for(var i = 0; i < 21; i=i+1){
  print(fib(i));
}
