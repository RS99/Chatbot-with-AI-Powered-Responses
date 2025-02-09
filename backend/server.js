const { exec } = require("child_process");
const http = require("http");

// Start Flask backend automatically
const flaskProcess = exec("python backend/app.py", (error, stdout, stderr) => {
    if (error) {
        console.error(`Error starting Flask: ${error.message}`);
        return;
    }
    if (stderr) {
        console.error(`Flask Error: ${stderr}`);
        return;
    }
    console.log(`Flask started successfully: ${stdout}`);
});

// Create Node.js server for status check
const server = http.createServer((req, res) => {
    if (req.method === "GET" && req.url === "/api/status") {
        res.writeHead(200, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ status: "ready" }));
    } else {
        res.writeHead(404, { "Content-Type": "text/plain" });
        res.end("Not Found");
    }
});

// Start Node.js server
server.listen(5000, () => {
    console.log("Node.js server running at http://127.0.0.1:5000/");
});
