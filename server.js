let express = require('express');
let Datastore = require('nedb');

let app = express();
let database = new Datastore('database.db');
database.loadDatabase();

let server = app.listen(3000, () => {
	console.log("Server running, listening at 3000...");
});

app.use(express.static('public'));
app.use(express.json({
	limit: '100kb'
}));


// We recieve data from Python via HTTP post request
app.post('/data', (req, res) => {
	let data = req.body;
	console.log(data);
	data.type = "data"
	database.insert(data);
	res.json({
		status: "OK",
		data: data
	})
});

// We recieve settings from Web via HTTP post request
app.post('/settings', (req, res) => {
	let data = req.body;
	console.log(data);
	data.type = "settings"
	database.insert(data);
	res.json({
		status: "OK",
		data: data
	})
});


// Send the data corresponding to the last ten minutes temperatures
app.get('/tenmin', (req, res) => {
	const gap = 10000000 // Ten minutes
	const now = Date.now(); 
	const last = now - (gap*60*1000) 
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
			console.log(docs)
			res.json(docs);
		}
	});
	// res.json({
	// 	1: 123,
	// 	2: 143,
	// 	3: 433,
	// 	4: 343,
	// 	5: 223,
	// });
})

// getDataDB();

function getDataDB() {
	database.find({
		$and: [{
			"type": "data"
		}, {
			"timestamp": { $gt: 5 }
		}]
	}, function (err, docs) {
		if (err) {
			console.error(err);
		} else {
			console.log(docs)
			return docs;
		}
	});
}
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