var express = require('express');
var router = express.Router({ mergeParams: true, strict: false });
const search = require('./functions/search_func')

router.route("/")
    .get(search.search)

module.exports = router;
