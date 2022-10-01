// Imprime los numeros primos entre 2-100
// print "Numeros primos: \n"

fun isprime(n) {
  var factor=2;
  while (factor * factor <= n) {
      if (n / factor == 0) {
          return false;
      }
      var factor = factor + 1;
  }
      return true;
}

for (n=2; n <= 10; n=n+1) {
    if (isprime(n)) {
        print n;
    }
}
