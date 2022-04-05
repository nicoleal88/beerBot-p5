// let express = require('express');
let Datastore = require('nedb');

// let app = express();
let database = new Datastore('database.db');
database.loadDatabase();

// let server = app.listen(3001, () => {
// 	console.log("Server running, listening at 3001...");
// });

let lastData = await getLastData();
let lastSettings = getLastSettings();

console.log(lastData)
console.log(lastSettings)


// let f1 = {
// 	temp: lastData.t1,
// 	label: lastSettings.label1,
// 	status: 0,
// 	alarm: 0
// }

// console.log(f1)

// app.use(express.static('public'));
// app.use(express.json({
// 	limit: '100kb'
// }));


// We recieve data from Python via HTTP post request
// app.post('/data', (req, res) => {
// 	let data = req.body;
// 	console.log(data);

// 	// Ejecutar funcion de alarmas
// 	data.type = "data"
// 	database.insert(data);
// 	res.json({
// 		status: "OK",
// 		data: data
// 	})
// });

// We recieve settings from Web via HTTP post request
// app.post('/settings', (req, res) => {
// 	let data = req.body;
// 	console.log(data);
// 	data.type = "settings"
// 	database.insert(data);
// 	res.json({
// 		status: "OK",
// 		data: data
// 	})
// });

// Send the data corresponding to the last ten minutes temperatures
// app.get('/tenmin', (req, res) => {
// 	let response = res;
// 	findAndSend(10, response);
// })

// // Send the data corresponding to the last hour temperatures
// app.get('/onehour', (req, res) => {
// 	let response = res;
// 	findAndSend(60, response);
// })

// // Send the data corresponding to the last ten minutes temperatures
// app.get('/oneday', (req, res) => {
// 	let response = res;
// 	findAndSend(1440, response);
// })

// // Send the data corresponding to the last ten minutes temperatures
// app.get('/week', (req, res) => {
// 	let response = res;
// 	findAndSend(10080, response);
// })

// app.get('/fortnight', (req, res) => {
// 	let response = res;
// 	findAndSend(21600, response);
// })

// // Send the data corresponding to the last ten minutes temperatures
// app.get('/settings', (req, res) => {
// 	database.find({ "type": "settings" }).sort({ timestamp: -1 }).exec(function (err, docs) {
// 		if (err) {
// 			console.error(err);
// 			res.end();
// 		} else {
// 			console.log(docs[0])
// 			res.json(docs[0]);
// 		}
// 	});
// })

// // Send the data corresponding to the last ten minutes temperatures
// app.get('/data', (req, res) => {
// 	database.find({ "type": "data" }).sort({ timestamp: -1 }).exec(function (err, docs) {
// 		if (err) {
// 			console.error(err);
// 			res.end();
// 		} else {
// 			console.log(docs[0])
// 			res.json(docs[0]);
// 		}
// 	});
// })


// function reduceArray(input, l) {
// 	let len = input.length
// 	let div = Math.floor(len / l);
// 	let result = [];
// 	if (len > l) {
// 		for (let i = 0; i < len; i = i + div) {
// 			result.push(input[i])
// 		}
// 	}
// 	else {
// 		for (let i = 0; i < len; i++) {
// 			result.push(input[i])
// 		}
// 	}
// 	return result
// };

// function findAndSend(gap_, res) {
// 	const gap = gap_
// 	const now = Date.now();
// 	const last = now - (gap * 60 * 1000)
// 	database.find({
// 		$and: [{
// 			"type": "data"
// 		}, {
// 			"timestamp": { $gt: last }
// 		}]
// 	}).sort({ timestamp: 1 }).exec(function (err, docs) {
// 		if (err) {
// 			console.error(err);
// 			res.end();
// 		} else {
// 			let toSend = reduceArray(docs, 100);
// 			console.log(toSend)
// 			res.json(toSend);
// 		}
// 	});
// };

async function getLastData(){
    database.find({ "type": "data" }).sort({ timestamp: -1 }).exec(function (err, docs) {
		if (err) {
			console.error(err);
		} else {
			console.log(docs[0])
			return docs[0];
		}
	});
}

function getLastSettings(){
    database.find({ "type": "settings" }).sort({ timestamp: -1 }).exec(function (err, docs) {
		if (err) {
			console.error(err);
		} else {
			console.log(docs[0])
			return docs[0];
		}
	});
}

// function checkAlarms(){
	// data = dataFromDB
	// settings = settingsFromDB
	// f1 = {
		// t = data.t1

	// }
	// t1 = data.t1
	// s1 = settings.t1
// }

// myArray = [];
// let ind;
// for (ind = 0; ind < 12120; ind++){
//   myArray.push(ind)
// }
// let div = Math.floor(myArray.length / 50);

// let result = [];

// for (let i = 0; i < myArray.length; i = i + div){
//   result.push(myArray[i])
// }


// getDataDB();

// function getDataDB() {
// 	database.find({
// 		$and: [{
// 			"type": "data"
// 		}, {
// 			"timestamp": { $gt: 5 }
// 		}]
// 	}, function (err, docs) {
// 		if (err) {
// 			console.error(err);
// 		} else {
// 			console.log(docs)
// 			return docs;
// 		}
// 	});
// }
// ########################################################## //

// let socket = require('socket.io');
// let io = socket(server);

// If there is a new connection, execute newConnection function
// io.sockets.on('connection', newConnection);

// function newConnection(socket) {
// 	console.log("New connection: " + socket.id);
// 	// If we recieve a message called "clickDate", execute the message function
// 	socket.on('clickDate', message);

// 	function message(data) {
// 		// Adding the socket.id to the message sended by the client
// 		data['userID'] = socket.id;
// 		database.insert(data);
// 		console.log(data);
// 		// Here we should store this data into a db
// 	}
// 	setInterval(timer, 3000);

// 	function timer() {
// 		let d = "lala";
// 		socket.emit('status', d);
// 	}
// }
