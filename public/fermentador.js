class Fermentador{
    // position
    // isFull?
    // label
    // cooling?
    // id
    // temperatire
    // setpoint
    
    // tmin_critical = 15
    // tmin_warning = 16
    // 17, 18, 19, 20, 21, 22
    // tmax_warning = 23
    // tmax_critical = 24

    constructor(x, id){
       this.x = x;
       this.id = id;
      //  this.button = 0;
      //  this.control = 1;
       this.temp = 2;
      //  this.sp = 3;
       this.label = "label";
    }
    
    update(){
      this.showLabel();
      this.showTemp();
      // this.showSP();
      this.showEV();
    }

    showLabel() {
    // draw a label below the shape
      push();
      noStroke();
      fill(0);
      textSize(labelsSize);
      textStyle(BOLD);
      textAlign(CENTER, CENTER);
      text(this.label, this.x, label_y);
      pop();
    }

    showTemp() {
      // draw a label below the shape
      push();
      noStroke();
      fill(0);
      textSize(tempsSize);
      textStyle(BOLD);
      textAlign(CENTER, CENTER);
      if (this.temp == 'null.0'){
        text(this.temp, this.x, temp_y);
      }
      else{
        text(this.temp + " °C", this.x, temp_y);
      }
      pop();
      }
      
    // showSP() {
    //   // draw a label below the shape
    //   push();
    //   noStroke();
    //   fill(100);
    //   textSize(spSize);
    //   textStyle(ITALIC);
    //   textAlign(CENTER, CENTER);
    //   text(this.sp + " °C", this.x, sp_y);
    //   pop();
    // }

    showEV() {
      // draw a label below the shape
      push();
      noStroke();
      fill(this.getColor());
      circle(this.x, ev_y, 32);
      pop();
    }
    
    getColor = function(label, temp) {
      if(this.label.toLowerCase() == "vacio"){
        return color('grey');
      }
      else{
        if(this.temp < 15){
          return color('blue');
        }
        else if(this.temp > 24){
          return color('red');
        }
        else{
          return color('green');
        }
      }
    }
}