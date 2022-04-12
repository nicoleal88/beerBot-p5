let Datastore = require('nedb');
let database = new Datastore('database_copy.db');
database.loadDatabase();

let fullStatus = {
	avg: 0,
	days: 0,
	}

ferm = "label2"

function getSettings(ferm) {
	database.find({ "type": "settings" }).sort({ timestamp: -1 }).exec(function (err, docs) {
		if (err) {
			console.error(err);
			// res.end();
		} else {
			ferm = ferm
			let label = docs[0][ferm]
			console.log(label)
			database.find({ "type": "settings", "label2": label }).sort({ timestamp: 1 }).exec(function (err, docs) {
				if (err) {
					console.error(err);
					// res.end();
				} else {
					// console.log(docs[0])
					var ts = docs[0].timestamp
					var date = new Date(ts);
					var now = Date.now()
					var days = Math.ceil(Math.abs(now - date) / (1000 * 60 * 60 * 24));
					// console.log(days)

					database.find({ $and: [{ "type": "data"	}, { "timestamp": { $gt: ts } }] }).sort({ timestamp: 1 }).exec(function (err, docs) {
						if (err) {
							console.error(err);
						} else {
							// console.log(docs)
							let toSend = reduceArray(docs, 100);
							var total = 0;
							for(var i = 0; i < toSend.length; i++) {
								total += toSend[i].t2;
								}
							var avg = total / toSend.length;
							// console.log(avg)
							fullStatus.avg = avg
							fullStatus.days = days
							console.log(fullStatus)

				}
			})
		}
	})}
})}


// Send the data corresponding to the last ten minutes temperatures
function getData () {
	database.find({ "type": "data" }).sort({ timestamp: -1 }).exec(function (err, docs) {
		if (err) {
			console.error(err);
			// res.end();
		} else {
			console.log(docs[0])
			// res.json(docs[0]);
		}
	})}

// Send the data corresponding to the last ten minutes temperatures

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

// function getAverage(text) {
// 	database.find({ "type": "settings", "label1": text }).sort({ timestamp: 1 }).exec(function (err, docs) {
// 		if (err) {
// 			console.error(err);
// 			// res.end();
// 		} else {
// 			let ts = docs[0].timestamp
// 			const first = ts
// 			console.log(first)
// 			console.log(Date.now())
// 			database.find({
// 				$and: [{
// 					"type": "data"
// 				}, {
// 					"timestamp": { $gt: first }
// 				}]
// 			}).sort({ timestamp: 1 }).exec(function (err, docs) {
// 				if (err) {
// 					console.error(err);
// 				} else {
// 					// console.log(docs)
// 					let toSend = reduceArray(docs, 100);
// 					console.log(toSend)
// 					var total = 0;
// 					for(var i = 0; i < toSend.length; i++) {
// 					total += toSend[i].t1;
// 					}
// 					var avg = total / toSend.length;
// 					console.log(avg)
		
// 					// res.json(toSend);
// 				}
// 			})
// 		}
// 	})
// }


// getData()
getSettings(ferm)
// let t = "label"
// getStatus(t)
// getAverage(t)
// getStatus()
// console.log(fullStatus)

/*
F1
- Buscar data (ultima temp)
- Buscar label
	- Buscar primer dato con ese label = calcular dias en fermentación
	- Buscar datos desde el primer día  (type=data, timestamp > primer dato), reducirlos (?) y promediarlos (dato.t1)
*/
