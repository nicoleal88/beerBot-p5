var path = "/home/nicolas/GitHub/beerBot/";
var test = 0;
// gui params

// gui Position
var gui_x = 966;
var gui_y = 236;

var f1_x = 168; //Linea en x del ferm 1
var f2_x = 465; //Linea en x del ferm 2
var f3_x = 762; //Linea en x del ferm 3

var ev_y = 282; // Linea en y de las electrovalvulas
var label_y = 505; // linea en y de las etiquetas
var temp_y = 590; //Linea en y de las temperaturas
var sp_y = 680; // Línea en y de los setpoints

var buttons_x = 966; // Linea en x de los botones

var setpoint1;
var setpoint2;
var setpoint3;

var spMin = 1;
var spMax = 30;

var label1;
var label2;
var label3;

// Fonts
var labelsSize = 24;
var spSize = 36;
var tempsSize = 48;

// Data input
var status = [];
var buttons = [];
var temps = [21.3, 22.4, 23.5, 24.6];
var temp1;
var temp2;
var temp3;
var tempAmb;

var SPs = [21, 22, 23, 24];
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

// Ferm objects
var ferm1;
var ferm2;
var ferm3;

function preload() {
    bImg = loadImage('images/FERMENTADORES.png');
    setMySettings();
    setMyData();
  }

function setup() {
  // socket = io.connect('http://ec2-13-58-79-243.us-east-2.compute.amazonaws.com:3001/');
	// if we recieve a message with a label 'status', execute the function readStatus()
	// socket.on('status', readStatus);

  console.log("preloading DONE");
  createCanvas(1200, 900);
  // console.log(test);

  // Ferm Objects
  ferm1 = new Fermentador(f1_x, 01);
  ferm2 = new Fermentador(f2_x, 02);
  ferm3 = new Fermentador(f3_x, 03);

  //Button creation
  button = createButton('Send Data');
  button.position(buttons_x, 595);
  button.class("button");
  button.mousePressed(sendData);

  tenMinButton = createButton("Plot 10 min");
  tenMinButton.position(buttons_x, 620);
  tenMinButton.class("button");
  tenMinButton.mousePressed(tenmin)

  hourButton = createButton("Plot 1 hr");
  hourButton.position(buttons_x, 645);
  hourButton.class("button");
  hourButton.mousePressed(onehour)

  dayButton = createButton("Plot 1 day");
  dayButton.position(buttons_x, 670);
  dayButton.class("button");
  dayButton.mousePressed(oneday)

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
var obj = {
  setpoint1: ferm1.sp,
  setpoint2: ferm2.sp,
  setpoint3: ferm3.sp,
  label1: ferm1.label,
  label2: ferm2.label,
  label3: ferm3.label,
}
sliderRange(spMin, spMax, 1);
gui.addObject(obj);

// Don't loop automatically
noLoop();
}

function draw() {
  background(bImg);
  // console.log(test);

  // temp1 = temps[0];

  // temp2 = temps[1];
  // temp3 = temps[2];
  tempAmb = temps[3];
  
  ferm1.showLabel(label1);
  ferm1.showTemp(nf(temp1, 0, 1));
  ferm1.showSP(setpoint1);
  ferm1.showEV();
  
  ferm2.showLabel(label2);
  ferm2.showTemp(nf(temp2, 0, 1));
  ferm2.showSP(setpoint2);
  
  ferm3.showLabel(label3);
  ferm3.showTemp(nf(temp3, 0, 1));
  ferm3.showSP(setpoint3);
  // ellipse(mouseX, mouseY, 80, 80);
}

// check for keyboard events
function keyPressed() {
  switch(key) {
    // type [F1] to hide / show the GUI
    case '+':
      visible = !visible;
      if(visible) gui.show(); else gui.hide();
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
	timestamp : d,
	sp1: setpoint1,
	sp2: setpoint2,
	sp3: setpoint3,
	label1: label1,
	label2: label2,
	label3: label3
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

async function setMyData(){
  const data = await getData('/data');
  if(data){
    console.log(data);
    temp1 = data.t1;
    temp2 = data.t2;
    temp3 = data.t3;
  }
  else{
    temp1 = -999;
    temp2 = -999;
    temp3 = -999;
  }
}

async function setMySettings(){
  const settings = await getData('/settings');
  if(settings){
  console.log(settings);
  setpoint1 = settings.sp1;
  setpoint2 = settings.sp2;
  setpoint3 = settings.sp3;

  label1 = settings.label1;
  label2 = settings.label2;
  label3 = settings.label3;
  }
  else{
    setpoint1 = 20;
    setpoint2 = 20;
    setpoint3 = 20;
  
    label1 = "label 1";
    label2 = "label 2";
    label3 = "label 3";
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
