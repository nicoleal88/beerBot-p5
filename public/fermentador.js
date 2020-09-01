class Fermentador{
    // position
    // isFull?
    // label
    // cooling?
    // id
    // temperatire
    // setpoint

    constructor(x, id){
       this.x = x;
       this.id = id;
       this.button = 1;
       this.control = 1;
    //    this.label = label;
    }
    
    showLabel(l) {
    // draw a label below the shape
      push();
      noStroke();
      fill(0);
      textSize(labelsSize);
      textStyle(BOLD);
      textAlign(CENTER, CENTER);
      text(l, this.x, label_y);
      pop();
    }

    showTemp(t) {
      // draw a label below the shape
      push();
      noStroke();
      fill(0);
      textSize(tempsSize);
      textStyle(BOLD);
      textAlign(CENTER, CENTER);
      text(t + " °C", this.x, temp_y);
      pop();
      }
      
    showSP(sp) {
      // draw a label below the shape
      push();
      noStroke();
      fill(100);
      textSize(spSize);
      textStyle(ITALIC);
      textAlign(CENTER, CENTER);
      text(sp + " °C", this.x, sp_y);
      pop();
    }

    showEV() {
      // draw a label below the shape
      push();
      noStroke();
      fill(this.getColor());
      circle(this.x, ev_y, 40);
      pop();
    }
    
    getColor = function(button, control) {
      if(this.button == 1 && this.control == 1){
        return color('green');
      }
      else{
        return color('red');
      }
    }
}