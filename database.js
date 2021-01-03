require("dotenv").config();
import { connect, connection } from "mongoose";

try {
	connect(
		`mongodb://${process.env.DB_USER}:${process.env.DB_PASS}@${process.env.DB_HOST}:${process.env.DB_PORT}/${process.env.DB_NAME}`,
		{ useNewUrlParser: true, useUnifiedTopology: true },
		function (err) {
			if (err) throw err;
			else
				switch (connection.readyState) {
				case 0:
					console.log("Mongodb Disconnected");
					break;
				case 1:
					console.log("Connected to mongodb");
					break;
				case 2:
					console.log("Connecting to mongodb");
					break;
				case 3:
					console.log("Disconnecting from Mongodb");
					break;
				case 4:
					console.log("Authentication Error");
					break;
				}
		},
	);
} catch (err) {
	console.error(err);
}
