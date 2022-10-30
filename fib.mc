/*
fib.mc

calcula el n-esimo número de la secuencia de Fibonacci

*/

fun fib(n){
  if (n <= 1){
    return 1;
  }else{
    return fib(ni-1) + fib(no-2);
  }
  end_if
}

//main
for (var i = 1; i < 20; i = i + 1) {
  print(fin(m));
}
