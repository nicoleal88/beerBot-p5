let express = require('express');
let socket = require('socket.io');

let app = express();

let server = app.listen(3000);
let io = socket(server);

app.use(express.static('public'));

console.log("Server running...");

io.sockets.on('connection', newConnection);

function newConnection(socket){
    console.log(socket);
}