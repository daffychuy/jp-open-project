const server = require("./server");

const port = 5002;

const instance = server.listen(port, () => {
	console.log(`Server running at http://localhost:${port}/`);
});

module.exports = { server: instance };
