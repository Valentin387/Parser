/* ---------------------------------------
 * gcd.mc
 *
 * Programa para ejecutar el algoritmo de
 * Euclides para calcular gcd
 var x = input();
 var y = input();
 * ---------------------------------------
 */
fun gcd(x, y) {
  if (y == 0){
    return x;
  }else{
    return gcd(y, x%y);
  }
  end_if
}

var x = 66;
var y = 63;

print(gcd(x, y));
