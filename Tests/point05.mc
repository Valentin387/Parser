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
fun str_f(){
  var a = "hola";
  if (isStr(a)==1){
    print("a es Str");
  }else{
    print("a no es Str");
  }end_if

  var aStr = str(a);

  if (isStr(aStr)==1){
    print("aStr es Str");
  }else{
    print("aStr no es Str");
  }end_if

}

//funciones matemáticas

fun funciones_mat(){
  var angulo = PI/4; //RAD
  print(format("log de %.3f = %.3f", EULER, log(EULER)));

  print(format("sin de %.3f = %.3f", angulo, sin(angulo)));
  print(format("cos de %.3f = %.3f", angulo, cos(angulo)));
  print(format("tan de %.3f = %.3f", angulo, tan(angulo)));
  print(format("%.3f rad is: %.3f deg", angulo, radToDeg(angulo)));
  print(format("%.3f deg is: %.3f rad", radToDeg(angulo), degToRad(radToDeg(angulo)) ) );

  var valor = 0.707106781;
  print(format("asin de %.3f = %.3f", valor, radToDeg(asin(valor))));
  print(format("acos de %.3f = %.3f", valor, radToDeg(acos(valor))));
  print(format("atan de %.3f = %.3f", valor, radToDeg(atan(valor))));
}

funciones_mat();












//
