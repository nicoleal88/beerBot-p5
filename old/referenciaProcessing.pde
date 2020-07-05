import controlP5.*;

ControlP5 cp5;

//String path = "/home/pi/beerBot/";
String path = "/home/nicolas/GitHub/beerBot/";

PrintWriter outputSPs;
PrintWriter label1;
PrintWriter label2;
PrintWriter label3;

float[] temps = {0.0, 0.0, 0.0, 0.0};
int[] status = {0, 0, 0, 0};
int[] buttons = {0, 0, 0, 0};

String t1;
String t2;
String t3;
String tAmb;

int spt1 = 20;
int spt2 = 20;
int spt3 = 20;

String nombreF1 = "F1";
String nombreF2 = "F2";
String nombreF3 = "F3";

PFont fTemp;
PFont fSP;
PFont fLabel;
PFont f4;

//Coordenadas
int f1x = 168; //Linea en x del ferm 1
int f2x = 465; //Linea en x del ferm 2
int f3x = 762; //Linea en x del ferm 3
int evy = 282; // Linea en y de las electrovalvulas
int labely = 512; // linea en y de las etiquetas
int tempy = 620; //Linea en y de las temperaturas
int spy = 708; // Línea en y de los setpoints
int contx = 1102;
int conty = 745;
int inputsx = 970;
int botonesx = 1100;

void setup() {
  size(1200, 900);

  fTemp = createFont("Quicksand Medium", 48, true);
  fSP = createFont("Quicksand Light", 32, true);
  fLabel = createFont("DejaVu Sans", 24, true);
  f4 = createFont("Piboto Condensed", 18, true);

  PImage botonPlay;

  botonPlay = loadImage(path + "SCADA/button_a.png");

  outputSPs = createWriter(path + "SPs.txt");

  label1 = createWriter(path + "Label1.txt");
  label2 = createWriter(path + "Label2.txt");
  label3 = createWriter(path + "Label3.txt");

  cp5 = new ControlP5(this);

  cp5.addTextfield("F1")
    .setPosition(inputsx, 460)
    .setSize(100, 50)
    .setFont(f4)
    .setLabel("Ferm. 1")
    .setAutoClear(false)
    ;
  cp5.addTextfield("F2")
    .setPosition(inputsx, 540)
    .setSize(100, 50)
    .setFont(f4)
    .setLabel("Ferm. 2")
    .setAutoClear(false)
    ;
  cp5.addTextfield("F3")
    .setPosition(inputsx, 620)
    .setSize(100, 50)
    .setFont(f4)
    .setLabel("Ferm. 3")
    .setAutoClear(false)
    ;

  cp5.addNumberbox("SPT1")
    .setPosition(inputsx, 260)
    .setSize(100, 20)
    .setFont(f4)
    .setScrollSensitivity(1.0)
    .setValue(spt1)
    .setLabel("Setpoint 1")
    .setMin(1)
    .setMax(30)
    ;
  cp5.addNumberbox("SPT2")
    .setPosition(inputsx, 320)
    .setSize(100, 20)
    .setFont(f4)
    .setScrollSensitivity(1.0)
    .setValue(spt2)
    .setLabel("Setpoint 2")
    .setMin(1)
    .setMax(30)
    ;
  cp5.addNumberbox("SPT3")
    .setPosition(inputsx, 380)
    .setSize(100, 20)
    .setFont(f4)
    .setScrollSensitivity(1.0)
    .setValue(spt3)
    .setLabel("Setpoint 3")
    .setMin(1)
    .setMax(30)
    ;

  cp5.addBang("SubmitF1")
    .setPosition(botonesx, 460)
    .setSize(50, 50)
    .setImage(botonPlay)
    ;
  cp5.addBang("SubmitF2")
    .setPosition(botonesx, 540)
    .setSize(50, 50)
    .setImage(botonPlay)
    ;
  cp5.addBang("SubmitF3")
    .setPosition(botonesx, 620)
    .setSize(50, 50)
    .setImage(botonPlay)
    ;

  cp5.addBang("SubmitSPs")
    .setPosition(botonesx, 305)
    .setSize(50, 50)
    .setImage(botonPlay)
    ;
}

void draw() {
  PImage fondo;
  fondo = loadImage(path + "SCADA/FERMENTADORES.png");
  background(fondo);
  //background(150);
  String[] temp = loadStrings(path + "tempFile.txt");
  String[] control = loadStrings(path + "controlFile.txt");
  String[] button = loadStrings(path + "buttonStatus.txt");


  if (temp.length != 0) {
    temps = float(split(temp[0], '\t'));
  }

  if (control.length != 0) {
    status = int(split(control[0], '\t'));
  }

  if (button.length != 0) {
    buttons = int(split(button[0], '\t'));
  }

  noStroke();

  if (buttons[0] == 1) {
    if (status[0] == 0) {
      fill(255, 0, 0, 100);
    } else {
      fill(0, 255, 0, 180);
    }
  } else {
    fill(0, 0, 0, 80);
  }
  circle(f1x, evy, 40);


  if (buttons[1] == 1) {
    if (status[1] == 0) {
      fill(255, 0, 0, 100);
    } else {
      fill(0, 255, 0, 180);
    }
  } else {
    fill(0, 0, 0, 80);
  }
  circle(f2x, evy, 40);

  if (buttons[2] == 1) {
    if (status[2] == 0) {
      fill(255, 0, 0, 100);
    } else {
      fill(0, 255, 0, 180);
    }
  } else {
    fill(0, 0, 0, 80);
  }
  circle(f3x, evy, 40);

  if (buttons[3] == 1) {
    if (status[3] == 0) {
      fill(255, 0, 0, 100);
    } else {
      fill(0, 255, 0, 200);
    }
  } else {
    fill(0, 0, 0, 80);
  }
  circle(contx, conty, 55);

  t1 = nf(temps[0], 0, 2) + " °C";
  t2 = nf(temps[1], 0, 2) + " °C";
  t3 = nf(temps[2], 0, 2) + " °C";
  tAmb = "T. Amb. = " + nf(temps[3], 0, 2) + " °C";


  fill(255);
  textFont(fTemp);   

  textAlign(CENTER);
  text(t1, f1x, tempy); 

  textAlign(CENTER);
  text(t2, f2x, tempy); 

  textAlign(CENTER);
  text(t3, f3x, tempy);

  fill(100);
  textFont(fSP);   

  textAlign(RIGHT);
  text(tAmb, 1180, 40);

  fill(150);  
  textFont(fSP);   

  textAlign(CENTER);
  text(str(spt1) + " °C", f1x, spy);
  textAlign(CENTER);
  text(str(spt2) + " °C", f2x, spy); 
  textAlign(CENTER);
  text(str(spt3) + " °C", f3x, spy);

  fill(255);
  textFont(fLabel);

  textAlign(CENTER);
  text(nombreF1, f1x, labely);

  textAlign(CENTER);
  text(nombreF2, f2x, labely);

  textAlign(CENTER);
  text(nombreF3, f3x, labely);
}

void SubmitF1() {
  //print();
  nombreF1=cp5.get(Textfield.class, "F1").getText();

  label1.println(nombreF1);
  label1.flush();

  cp5.get(Textfield.class, "F1").clear();
}

void SubmitF2() {
  //print();
  nombreF2=cp5.get(Textfield.class, "F2").getText();

  label2.println(nombreF2);
  label2.flush();

  cp5.get(Textfield.class, "F2").clear();
}

void SubmitF3() {
  //print();
  nombreF3=cp5.get(Textfield.class, "F3").getText();

  label3.println(nombreF3);
  label3.flush();

  cp5.get(Textfield.class, "F3").clear();
}

void SubmitSPs() {
  //print();
  spt1=int(cp5.get(Numberbox.class, "SPT1").getValue());
  spt2=int(cp5.get(Numberbox.class, "SPT2").getValue());
  spt3=int(cp5.get(Numberbox.class, "SPT3").getValue());

  outputSPs.println(spt1 + "\t" + spt2 + "\t" + spt3);
  outputSPs.flush();
  //outputSPs.close();
  //cp5.get(Textfield.class,"F1").clear();
}
