require("dotenv").config();
import { connect } from "mongoose";

try {
	connect(`mongodb://${process.env.DB_USER}:${process.env.DB_PASS}@${process.env.DB_HOST}:${process.env.DB_PORT}/${process.env.DB_NAME}`, { useNewUrlParser: true, useUnifiedTopology: true });
} catch (err) {
	console.error(err);
}
