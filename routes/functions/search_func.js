var Promise = require('bluebird');

exports.search = [
    async function (req, res, next) {
        let keyword = req.query.keyword;
        
        console.log("API passed through")
        console.log(req.query)
    }
]