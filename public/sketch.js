var path = "/home/nicolas/GitHub/beerBot/";
var test = 0;
// gui params

// gui Position
var gui_x = 933;
var gui_y = 200;

var f1_x = 768; //Linea en x del ferm 1
var f2_x = 528; //Linea en x del ferm 2
var f3_x = 288; //Linea en x del ferm 3

var ev_y = 225; // Linea en y de las electrovalvulas
var label_y = 404; // linea en y de las etiquetas
var temp_y = 472; //Linea en y de las temperaturas
// var sp_y = 544; // Línea en y de los setpoints

var buttons_x = gui_x; // Linea en x de los botones

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
var lastTimestamp;

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
  setMySettings();
  setMyData();

  bImg = loadImage("images/Ferm_background_720.png");
}

const minutes = 1;
const interval = minutes * 60 * 1000;

setInterval(function () {
  // catch all the errors
  setMySettings().catch(console.log);
  setMyData().catch(console.log);
  showLastUpdate();
}, interval);

function setup() {
  frameRate(5);
  console.log("preloading DONE");
  createCanvas(1280, 720);
  // console.log(test);

  // lastUpdateDate = new Date(Number(lastTimestamp));

  showLastUpdate();

  //Button creation
  button = createButton("Enviar datos");
  button.position(buttons_x, 412);
  button.class("button");
  button.mousePressed(sendData);

  hourButton = createButton("Gráfico 1 hora");
  hourButton.position(buttons_x, 442);
  hourButton.class("button");
  hourButton.mousePressed(onehour);

  dayButton = createButton("Gráfico 1 día");
  dayButton.position(buttons_x, 472);
  dayButton.class("button");
  dayButton.mousePressed(oneday);

  dayButton = createButton("Gráfico 7 días");
  dayButton.position(buttons_x, 502);
  dayButton.class("button");
  dayButton.mousePressed(week);

  fortnightButton = createButton("Gráfico 15 días");
  fortnightButton.position(buttons_x, 532);
  fortnightButton.class("button");
  fortnightButton.mousePressed(fortnight);

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
  };
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
  push();
  textSize(labelsSize);
  textStyle(BOLD);
  fill(230);
  textAlign(CENTER);
  if (tempAmb == "null.0") {
    text("T° amb.: ---", 1032, 175);
  } else {
    text("T° amb.: " + tempAmb + " °C", 1032, 175);
  }
  pop();

  showLastUpdate();

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
    case "+":
      visible = !visible;
      if (visible) gui.show();
      else gui.hide();
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
    label3: ferm3.label,
  };
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  };

  const confirm_message = `Desea enviar estos labels?\nLabel1: ${data.label1}\nLabel2: ${data.label2}\nLabel3: ${data.label3}`;

  if (confirm(confirm_message)) {
    const response = await fetch("/settings", options);
    const json = await response.json();
    console.log("Envío de settings autorizado");
    console.log(json);
  } else {
    console.log("Envío de settings cancelado");
  }
}

async function getData(route) {
  const response = await fetch(route);
  const data = await response.json();
  // console.log(data);
  return data;
}

async function setMyData() {
  const data = await getData("/data");
  if (data) {
    console.log(data);
    ferm1.temp = nf(data.t1, 0, 1);
    ferm2.temp = nf(data.t2, 0, 1);
    ferm3.temp = nf(data.t3, 0, 1);
    tempAmb = nf(data.t0, 0, 1);
    lastTimestamp = data.timestamp;
  } else {
    ferm1.temp = -999;
    ferm2.temp = -999;
    ferm3.temp = -999;
  }
}

async function setMySettings() {
  const settings = await getData("/settings");
  if (settings) {
    console.log(settings);
    // ferm1.sp = settings.sp1;
    // ferm2.sp = settings.sp2;
    // ferm3.sp = settings.sp3;

    ferm1.label = settings.label1;
    ferm2.label = settings.label2;
    ferm3.label = settings.label3;
  } else {
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

function week() {
  window.open("week.html");
}

function fortnight() {
  window.open("fortnight.html");
}

function showLastUpdate() {
  push();
  fill(200);
  noStroke();
  textSize(12);
  textAlign(CENTER);

  var timestamp = lastTimestamp;
  var date = new Date(timestamp);

  text("Último dato: " + date.toLocaleString("es-AR"), width / 2, height - 4);
  pop();
  // const point = AMIGA_Map.latLngToPixel(elt.lat, elt.lng);
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
