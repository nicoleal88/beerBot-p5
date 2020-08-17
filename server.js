let express = require('express');
let socket = require('socket.io');
let Datastore = require('nedb');

let app = express();
let database = new Datastore('database.db');
database.loadDatabase();

let server = app.listen(3001, () => {
	console.log("Server running, listening at 3001...");
});

let io = socket(server);

app.use(express.static('public'));
app.use(express.json({limit: '100kb'}));


// If there is a new connection, execute newConnection function
io.sockets.on('connection', newConnection);

function newConnection(socket){
	console.log("New connection: " + socket.id);
	// If we recieve a message called "clickDate", execute the message function
	socket.on('clickDate', message);
	function message(data){
		// Adding the socket.id to the message sended by the client
		data['userID'] = socket.id;
		database.insert(data);
		console.log(data);
		// Here we should store this data into a db
	}
	setInterval(timer, 3000);
	function timer(){
	let d = "lala";
	socket.emit('status',d);
	}
}

app.post('/data', (req, res) => {
    console.log(req);
    res.json({status: "OK",
                    data: req.body})

});
