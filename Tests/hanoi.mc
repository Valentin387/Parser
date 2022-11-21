// Tower of hanoi game
// line 6: print("move " + src);

fun hanoi(n, src, dest, spare) {
	if (n == 1) {
		print("move ");
		print(src);
		print(src);
		print(" to ");
		print(dest);
		print("\n");
	}
	else {
		hanoi(n-1,src,spare,dest);
		hanoi(1,src,dest,spare);
		hanoi(n-1,spare,dest,src);
	}end_if
}

var n = 4;
print("Towers of hanoi.\n");
// print "Enter number of rings : ";
hanoi(n,1,3,2);
