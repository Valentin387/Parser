// Imprime los numeros primos entre 2-100
// print "Numeros primos: \n"

fun isprime(n) {
  var factor=2;
  while (factor * factor <= n) {
      if (n % factor == 0) {
          return false;
      }end_if
      factor = factor + 1;
  }
      return true;
}

for (var n=2; n <= 1000; n=n+1) {
    if (isprime(n)) {
        print(n);
    }end_if
}
