let express = require('express');
let Datastore = require('nedb');

let app = express();

var useragent = require('express-useragent');

let database = new Datastore('database.db');
database.loadDatabase();

let server = app.listen(3001, () => {
	console.log("-----------------------------------------------------------------------------");
	console.log("Server running, listening at 3001...");
	console.log("-----------------------------------------------------------------------------");
});

app.use(express.static('public'));
app.use(express.json({
	limit: '100kb'
}));
app.use(useragent.express());

// Recieve data from Python via HTTP post request
app.post('/data', (req, res) => {
	let data = req.body;
	console.log("-----------------------------------------------------------------------------");
	console.log("Receiving data from python RPI");
	console.log(`Source: ${req.useragent.source}`);
	console.log(data);
	console.log("-----------------------------------------------------------------------------");
	data.type = "data"
	database.insert(data);
	res.json({
		status: "OK",
		data: data
	})
});

// Recieve settings from Web via HTTP post request
app.post('/settings', (req, res) => {
	let data = req.body;
	console.log("-----------------------------------------------------------------------------");
	console.log("Receiving settings from web");
	console.log(`Source: ${req.useragent.source}`);
	console.log(data);
	console.log("-----------------------------------------------------------------------------");
	data.type = "settings"
	database.insert(data);
	res.json({
		status: "OK",
		data: data
	})
});

// Send the data corresponding to the last ten minutes temperatures
app.get('/tenmin', (req, res) => {
	console.log("-----------------------------------------------------------------------------");
	console.log("Sending 10min info to web plotter");
	console.log(`Source: ${req.useragent.source}`);
	console.log("-----------------------------------------------------------------------------");
	let response = res;
	findAndSend(10, response);
})

// Send the data corresponding to the last hour temperatures
app.get('/onehour', (req, res) => {
	console.log("-----------------------------------------------------------------------------");
	console.log("Sending 1 hour info to web plotter");
	console.log(req.useragent);
	console.log(`Source: ${req.useragent.source}`);
	console.log("-----------------------------------------------------------------------------");
	let response = res;
	findAndSend(60, response);
})

// Send the data corresponding to the last day temperatures
app.get('/oneday', (req, res) => {
	console.log("-----------------------------------------------------------------------------");
	console.log("Sending 1 day info to web plotter");
	console.log(`Source: ${req.useragent.source}`);
	console.log("-----------------------------------------------------------------------------");
	let response = res;
	findAndSend(1440, response);
})

// Send the data corresponding to the last week temperatures
app.get('/week', (req, res) => {
	console.log("-----------------------------------------------------------------------------");
	console.log("Sending 1 week info to web plotter");
	console.log(`Source: ${req.useragent.source}`);
	console.log("-----------------------------------------------------------------------------");
	let response = res;
	findAndSend(10080, response);
})

// Send the data corresponding to the last 15 days temperatures
app.get('/fortnight', (req, res) => {
	console.log("-----------------------------------------------------------------------------");
	console.log("Sending 15 day info to web plotter");
	console.log(`Source: ${req.useragent.source}`);
	console.log("-----------------------------------------------------------------------------");
	let response = res;
	findAndSend(21600, response);
})

// Send the last settings
app.get('/settings', (req, res) => {
	database.find({ "type": "settings" }).sort({ timestamp: -1 }).exec(function (err, docs) {
		if (err) {
			console.error(err);
			res.end();
		} else {
			console.log("-----------------------------------------------------------------------------");
			console.log(`Sending the last settings to ${req.useragent.source}`)
			console.log("-----------------------------------------------------------------------------");
			// console.log(docs[0])
			res.json(docs[0]);
		}
	});
})

// Send the last data
app.get('/data', (req, res) => {
	database.find({ "type": "data" }).sort({ timestamp: -1 }).exec(function (err, docs) {
		if (err) {
			console.error(err);
			res.end();
		} else {
			console.log("-----------------------------------------------------------------------------");
			console.log(`Sending the last data to ${req.useragent.source}`)
			// console.log(docs[0])
			console.log("-----------------------------------------------------------------------------");
			res.json(docs[0]);
		}
	});
})

// Send the last status
app.get('/status', (req, res) => {
	// 
	database.find({ "type": "settings" }).sort({ timestamp: -1 }).exec(function (err, docs) {
		if (err) {
			console.error(err);
			res.end();
		} else {
			console.log("-----------------------------------------------------------------------------");
			console.log(`Sending the last status to ${req.useragent.source}`)
			// console.log(docs[0])
			console.log("-----------------------------------------------------------------------------");
			res.json(docs[0]);
		}
	});
})

// Reduce an array from n(Input) to l  
function reduceArray(input, l) {
	let len = input.length
	let div = Math.floor(len / l);
	let result = [];
	if (len > l) {
		for (let i = 0; i < len; i = i + div) {
			result.push(input[i])
		}
	}
	else {
		for (let i = 0; i < len; i++) {
			result.push(input[i])
		}
	}
	return result
};

function findAndSend(gap_, res) {
	const gap = gap_
	const now = Date.now();
	const last = now - (gap * 60 * 1000)
	database.find({
		$and: [{
			"type": "data"
		}, {
			"timestamp": { $gt: last }
		}]
	}).sort({ timestamp: 1 }).exec(function (err, docs) {
		if (err) {
			console.error(err);
			res.end();
		} else {
			let toSend = reduceArray(docs, 100);
			// console.log(toSend)
			res.json(toSend);
		}
	});
};

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
