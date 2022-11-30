//clock
fun clock_f(){
  var start = clock(1);
  for (var i=1; i<=10000;i++){
    var a=1;
  }
  var stop = clock(1);

  print(format("Time: %.2f seconds",stop-start));
}

//len
var cad = "abc d";
var lon = len(cad);
print(cad);
print(format("longitud: %d",lon));

//
