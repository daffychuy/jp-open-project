const server = require("./server").default;

const port = 7771;

const instance = server.listen(port, () => {
	console.log(`Server running at http://localhost:${port}/`);
});

module.exports = { server: instance };
