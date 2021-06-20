const express = require("express");
const router = express.Router({ mergeParams: true, strict: false });
const search = require("./functions/search_func.js");

router.get("/words", search.search);

module.exports = router;
