// Fibonacci iterativo

fun fib(i,j, n){
	for(var cont = 0; cont < n; cont=cont+1){
		if (i < j){
			print(j);
			i=i+j;
		}else{
			print(i);
			j=j+i;
		}end_if
	}
}

var a=0;
var b=1;
var c=20;

fib(a,b,c);
