/* ---------------------------------------
 * Program to print prime factors
 *
 * A function to print all prime factors
 * of a given number n.
 * ---------------------------------------
 */

fun prime_factors(n) {

	// Print number of two's that divide n
	while (n % 2 == 0) {
		print(2);
		n = n / 2;
	}

	// n must be odd at this point
	// so a skip of 2 ( i = i + 2) can be used
	for(var i = 3; i * i <= n; i = i + 2) {

		// while i divides n , print i and divide n
		while (n % i == 0) {
			print(i);
			n = n / i;
		}
	}

	// Condition if n is a prime
	// number greater than 2
	if (n > 2) {
		print(n);
	}end_if

}

var n = 315;
prime_factors(n);
