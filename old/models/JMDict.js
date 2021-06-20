import mongoose from "mongoose";

const JMDict = new mongoose.Schema({
	_id: mongoose.Schema.ObjectId,
	JMdict_id: String,
	Japanese: Array,
	sense: Array,
});

module.exports = mongoose.model("JMDict", JMDict, "JMDict");
