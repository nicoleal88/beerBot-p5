const express = require("express");
const Datastore = require("nedb");
const useragent = require("express-useragent");

const app = express();

const PORT = process.env.PORT || 3001;
const DB_NAME = process.env.DB_NAME || "database.db";

const database = new Datastore(DB_NAME);
database.loadDatabase();

app.use(express.static("public"));

app.use(
  express.json({
    limit: "100kb",
  })
);
app.use(useragent.express());

// Receive data from Python via HTTP post request
app.post("/data", async (req, res) => {
  try {
    let data = req.body;
    if (!data || typeof data !== "object") {
      return res.status(400).json({ error: "Invalid data format" });
    }

    data.type = "data";
    await database.insert(data);

    logRequest(req, "Receiving data from python RPI...");
    console.log(data);

    res.json({
      status: "OK",
      data: data,
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

// Receive settings from Web via HTTP post request
app.post("/settings", async (req, res) => {
  try {
    let data = req.body;
    if (!data || typeof data !== "object") {
      return res.status(400).json({ error: "Invalid settings format" });
    }

    data.type = "settings";
    await database.insert(data);

    logRequest(req, "Receiving settings from web...");
    console.log(data);

    res.json({
      status: "OK",
      data: data,
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

// Send the data corresponding to the last ten minutes temperatures
function createTimeHandler(minutes, description) {
  return async (req, res) => {
    try {
      logRequest(req, `Sending ${description} info to web plotter...`);
      await findAndSend(minutes, res);
    } catch (err) {
      console.error(err);
      res.status(500).json({ error: "Internal Server Error" });
    }
  };
}

app.get("/tenmin", createTimeHandler(10, "10min"));
app.get("/onehour", createTimeHandler(60, "1 hour"));
app.get("/oneday", createTimeHandler(1440, "1 day"));
app.get("/week", createTimeHandler(10080, "1 week"));
app.get("/fortnight", createTimeHandler(21600, "15 day"));

// Send the last settings
app.get("/settings", async (req, res) => {
  try {
    const docs = await database
      .find({ type: "settings" })
      .sort({ timestamp: -1 })
      .limit(1)
      .exec();

    if (docs.length === 0) {
      return res.status(404).json({ error: "No settings found" });
    }

    logRequest(req, "Sending the last settings...");
    res.json(docs[0]);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

// Send the last data
app.get("/data", async (req, res) => {
  try {
    const docs = await database
      .find({ type: "data" })
      .sort({ timestamp: -1 })
      .limit(1)
      .exec();

    if (docs.length === 0) {
      return res.status(404).json({ error: "No data found" });
    }

    logRequest(req, "Sending the last data...");
    res.json(docs[0]);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

// Send the last status
app.get("/status", async (req, res) => {
  try {
    const docs = await database
      .find({ type: "settings" })
      .sort({ timestamp: -1 })
      .limit(1)
      .exec();

    if (docs.length === 0) {
      return res.status(404).json({ error: "No status found" });
    }

    logRequest(req, "Sending the last status...");
    res.json(docs[0]);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

// Reduce an array from n(Input) to l
function reduceArray(input, l) {
  const len = input.length;
  if (len <= l) return input;

  const step = len / l;
  return Array.from({ length: l }, (_, i) => input[Math.floor(i * step)]);
}

async function findAndSend(gap_, res) {
  try {
    const gap = gap_;
    const now = Date.now();
    const last = now - gap * 60 * 1000;
    const docs = await database
      .find({
        $and: [{ type: "data" }, { timestamp: { $gt: last } }],
      })
      .sort({ timestamp: 1 })
      .exec();

    let toSend = reduceArray(docs, 100);
    res.json(toSend);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Internal Server Error" });
  }
}

function logRequest(req, description) {
  console.log(
    "-----------------------------------------------------------------------------"
  );
  console.log(description);
  console.log(
    `Device data: ${req.useragent.browser} ${req.useragent.version}, ${req.useragent.os} - ${req.useragent.platform}`
  );
  console.log(
    "-----------------------------------------------------------------------------"
  );
}

app.listen(PORT, () => {
  console.log(`Server running, listening at ${PORT}...`);
});
