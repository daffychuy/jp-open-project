var express = require('express');
var router = express.Router({ mergeParams: true, strict: false });

/* Redirect to API request file */
router.use('/search', require('./search'));

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

module.exports = router;
