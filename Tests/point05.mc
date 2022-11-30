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
fun len_f(){
  var cad = "abc d";
  var lon = len(cad);
  print(cad);
  print(format("longitud: %d",lon));
}

//input
fun input_f(){
  var a = input("Ingresa algo: ");
  print(a);
  print(a-1);
}

fun validation_f(){
  var a = input("ingrese un valor: ");

  if (isInteger(a) == true){
    print("It's int");
  }end_if

  if (isFloat(a) == true){
    print("It's float");
  }end_if

  if (isStr(a) == true){
    print("It's str");
  }end_if

}

//str()















//
