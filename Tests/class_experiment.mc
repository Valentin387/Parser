

class dog{

  setName(name){
    this.name=name;
    print(this.name);
  }

  getName(){
    print(this.name);
  }

  bark(){
    this.getName();
    print("barking");
  }

  run(){
    this.getName();
    print("running");
  }
}

var dog1 =  dog();
dog1.setName("Cuski");
dog1.bark();

var dog2 =  dog();
dog1.setName("Sultan");
dog2.run();
