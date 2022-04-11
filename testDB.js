let Datastore = require('nedb');

let database = new Datastore('database_copy.db');
database.loadDatabase();

function getSettings(req, res) {
	database.find({ "type": "settings" }).sort({ timestamp: -1 }).exec(function (err, docs) {
		if (err) {
			console.error(err);
			res.end();
		} else {
			console.log(docs[0])
			res.json(docs[0]);
		}
	})}

// Send the data corresponding to the last ten minutes temperatures
function getData (req, res) {
	database.find({ "type": "data" }).sort({ timestamp: -1 }).exec(function (err, docs) {
		if (err) {
			console.error(err);
			res.end();
		} else {
			console.log(docs[0])
			res.json(docs[0]);
		}
	})}

// Send the data corresponding to the last ten minutes temperatures
function getStatus (req, res) {
	// 
	database.find({ "type": "settings" }).sort({ timestamp: -1 }).exec(function (err, docs) {
		if (err) {
			console.error(err);
			res.end();
		} else {
			console.log(docs[0])
			res.json(docs[0]);
		}
	})}

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
			console.log(toSend)
			res.json(toSend);
		}
	});
};

getData()
getSettings()
getStatus()
