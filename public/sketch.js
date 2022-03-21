var path = "/home/nicolas/GitHub/beerBot/";
var test = 0;
// gui params

// gui Position
var gui_x = 934;
var gui_y = 267;

var f1_x = 768; //Linea en x del ferm 1
var f2_x = 528; //Linea en x del ferm 2
var f3_x = 288; //Linea en x del ferm 3

var ev_y = 225; // Linea en y de las electrovalvulas
var label_y = 404; // linea en y de las etiquetas
var temp_y = 472; //Linea en y de las temperaturas
// var sp_y = 544; // Línea en y de los setpoints

var buttons_x = 934; // Linea en x de los botones

// var setpoint1;
// var setpoint2;
// var setpoint3;

// var spMin = 1;
// var spMax = 30;

var label1;
var label2;
var label3;

// Fonts
var labelsSize = 20;
// var spSize = 28;
var tempsSize = 38;

// Data input
var status = [];
var buttons = [];
var temps = [21.3, 22.4, 23.5, 24.6];
var temp1;
var temp2;
var temp3;
var tempAmb;

// var SPs = [21, 22, 23, 24];
// float[] temps = {0.0, 0.0, 0.0, 0.0};
// int[] status = {0, 0, 0, 0};
// int[] buttons = {0, 0, 0, 0};

// Data output
// p5.PrintWriter outputSPs;
// PrintWriter label1;
// PrintWriter label2;
// PrintWriter label3;

// gui
var visible = true;
var gui;
var obj;

// Ferm objects
var ferm1;
var ferm2;
var ferm3;

function preload() {
  // Ferm Objects
  ferm1 = new Fermentador(f1_x, 01);
  ferm2 = new Fermentador(f2_x, 02);
  ferm3 = new Fermentador(f3_x, 03);

  bImg = loadImage('images/Ferm_background_720.png');
  setMySettings();
  setMyData();
}

function setup() {
  // socket = io.connect('http://ec2-13-58-79-243.us-east-2.compute.amazonaws.com:3001/');
  // if we recieve a message with a label 'status', execute the function readStatus()
  // socket.on('status', readStatus);

  frameRate(5);
  console.log("preloading DONE");
  createCanvas(1280, 720);
  // console.log(test);

  //Button creation
  button = createButton('Enviar datos');
  button.position(buttons_x, 476);
  button.class("button");
  button.mousePressed(sendData);

  hourButton = createButton("Gráfico 1 hora");
  hourButton.position(buttons_x, 496);
  hourButton.class("button");
  hourButton.mousePressed(onehour)

  dayButton = createButton("Gráfico 1 día");
  dayButton.position(buttons_x, 516);
  dayButton.class("button");
  dayButton.mousePressed(oneday)

  fortnightButton = createButton("Gráfico 15 días");
  fortnightButton.position(buttons_x, 536);
  fortnightButton.class("button");
  fortnightButton.mousePressed(fortnight)

  // Create Layout GUI
  gui = createGui();
  gui.setPosition(gui_x, gui_y);

  // set slider range for setpoints
  // sliderRange(spMin, spMax, 1);
  // gui.addGlobals('setpoint1');

  // sliderRange(spMin, spMax, 1);
  // gui.addGlobals('setpoint2');

  // sliderRange(spMin, spMax, 1);
  // gui.addGlobals('setpoint3');

  // gui.addGlobals('label1', 'label2', 'label3',);
  obj = {
    // setpoint1: ferm1.sp,
    // setpoint2: ferm2.sp,
    // setpoint3: ferm3.sp,
    label1: ferm1.label,
    label2: ferm2.label,
    label3: ferm3.label,
  }
  // sliderRange(spMin, spMax, 1);
  gui.addObject(obj);

  // Don't loop automatically
  // noLoop();
}

function draw() {
  background(bImg);
  // console.log(test);

  // temp1 = temps[0];

  // temp2 = temps[1];
  // temp3 = temps[2];
  push()
  textSize(labelsSize)
  fill(230)
  textAlign(RIGHT)
  text("T. amb.: " + tempAmb + " C", 1115, 217);
  pop()

  // ferm1.sp = obj.setpoint1;
  // ferm2.sp = obj.setpoint2;
  // ferm3.sp = obj.setpoint3;
  ferm1.label = obj.label1;
  ferm2.label = obj.label2;
  ferm3.label = obj.label3;

  ferm1.update();
  ferm2.update();
  ferm3.update();

  // ferm1.showLabel(label1);
  // ferm1.showTemp(nf(temp1, 0, 1));
  // ferm1.showSP(setpoint1);
  // ferm1.showEV();

  // ferm2.showLabel(label2);
  // ferm2.showTemp(nf(temp2, 0, 1));
  // ferm2.showSP(setpoint2);

  // ferm3.showLabel(label3);
  // ferm3.showTemp(nf(temp3, 0, 1));
  // ferm3.showSP(setpoint3);
  // ellipse(mouseX, mouseY, 80, 80);
}

// check for keyboard events
function keyPressed() {
  switch (key) {
    // type [F1] to hide / show the GUI
    case '+':
      visible = !visible;
      if (visible) gui.show(); else gui.hide();
      break;
  }
}

function mousePressed() {
  console.log(mouseX, mouseY);
  // loadStrings('test.txt', pickString);
  // loadtxt('buttoStatus.txt');
}

/*function pickString(output) {
  test = output;
  console.log(test);// background(200);
  text(test, mouseX, mouseY, 80, 80);
  test = 0;
}
*/

async function sendData() {
  let d = Date.now();

  // Creating the data object
  let data = {
    timestamp: d,
    // sp1: ferm1.sp,
    // sp2: ferm2.sp,
    // sp3: ferm3.sp,
    label1: ferm1.label,
    label2: ferm2.label,
    label3: ferm3.label
  }
  const options = {
    method: 'POST',
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  }
  const response = await fetch('/settings', options);
  const json = await response.json();
  console.log(json);
}

async function getData(route) {
  const response = await fetch(route);
  const data = await response.json();
  // console.log(data);
  return data;
}

async function setMyData() {
  const data = await getData('/data');
  if (data) {
    console.log(data);
    ferm1.temp = nf(data.t1, 0, 1);
    ferm2.temp = nf(data.t2, 0, 1);
    ferm3.temp = nf(data.t3, 0, 1);
    tempAmb = nf(data.t0, 0, 1);
  }
  else {
    ferm1.temp = -999;
    ferm2.temp = -999;
    ferm3.temp = -999;
  }
}

async function setMySettings() {
  const settings = await getData('/settings');
  if (settings) {
    console.log(settings);
    // ferm1.sp = settings.sp1;
    // ferm2.sp = settings.sp2;
    // ferm3.sp = settings.sp3;

    ferm1.label = settings.label1;
    ferm2.label = settings.label2;
    ferm3.label = settings.label3;
  }
  else {
    // ferm1.sp = 20;
    // ferm2.sp = 20;
    // ferm3.sp = 20;

    ferm1.label = "label 1";
    ferm2.label = "label 2";
    ferm3.label = "label 3";
  }
}

function tenmin() {
  window.open("tenmins.html");
}

function onehour() {
  window.open("onehour.html");
}

function oneday() {
  window.open("oneday.html");
}

function fortnight() {
  window.open("fortnight.html");
}
// Scheme:

// User inputs:
// Setpoints
// Labels

// Load Files
// buttonStatus.txt
// controlFile.txt
// tempFile.txt

// Write files:
// SPs.txt

// function loadtxt(path) {
//   console.log("loading");
//   loadStrings(path, parsing);
// }

// function parsing(result) {
// let lista;
// if (result.length != 0) {
//   lista = float(split(lista[0], '\t'));
// }
// console.log("parsing");
// console.log(lista);
// }

// function readStatus(data){
// console.log(data);
// }
