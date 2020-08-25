// let socket;
//var path = "/home/pi/beerBot/";
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

var setpoint1 = 20;
var setpoint2 = 20;
var setpoint3 = 20;

var spMin = 1;
var spMax = 30;

var label1 = 'label 1';
var label2 = 'label 2';
var label3 = 'label 3';

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

function preload() {
    bImg = loadImage('images/FERMENTADORES.png');
    const settings = getData();
    console.log(settings);
    if(settings){
    setpoint1 = settings.sp1;
    setpoint2 = settings.sp2;
    setpoint3 = settings.sp3;

    label1 = settings.label1;
    label2 = settings.label2;
    label3 = settings.label3;
    }
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

  //Button creation
  button = createButton('Send Data to Server');
  button.position(1005, 650);
  button.mousePressed(sendData);

  tenMinButton = createButton("Plot 10 min");
  tenMinButton.position(f1_x, 750);
  tenMinButton.mousePressed(tenmin)


// Create Layout GUI
gui = createGui();
gui.setPosition(gui_x, gui_y);

// set slider range for setpoints
sliderRange(spMin, spMax, 1);
gui.addGlobals('setpoint1');

sliderRange(spMin, spMax, 1);
gui.addGlobals('setpoint2');

sliderRange(spMin, spMax, 1);
gui.addGlobals('setpoint3');

gui.addGlobals('label1', 'label2', 'label3',);

// Don't loop automatically
noLoop();
}

function draw() {
  background(bImg);
  // console.log(test);

  var temp1 = temps[0];
  var temp2 = temps[1];
  var temp3 = temps[2];
  var tempAmb = temps[3];
  
  ferm1.showLabel(label1);
  ferm1.showTemp(nf(temp1), 0, 2);
  ferm1.showSP(setpoint1);
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

async function getData() {
  const response = await fetch('/settings');
  const data = await response.json();
  // console.log(data);
  return data;
}

function tenmin() {
  window.location.href = "tenmin.html";
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
