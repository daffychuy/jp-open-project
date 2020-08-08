const Promise = require('bluebird');
const jp = require('wanakana');
const validator = require('validator');

exports.search = [
    async function (req, res, next) {
        let query = req.query;
        let keyword = validator.escape(query.keyword);
        console.log(keyword)
        if (jp.isJapanese(keyword)) {
            // Gotta split accordingly
        } else {
            // Need to process the word, and convert into japanaese character first
            let converted_keyword = jp.toHiragana(keyword)

        }
        res.status(200).send({"RESULT": jp.isJapanese(keyword)})
    }
]

function search_hiragana(word) {
    let query = "SELECT * FROM "
}
// ! Not used
function recognize_lang(ch) {
    // 0 : Punctuation
    // 1 : Hiragana
    // 2 : Ktakana
    // 3 : Full-Width Roman / Half-width Katakana
    // 4 : CJK : Common & uncommon kanji
    // 5 : CJK Ext. Rare Kanji
    let jp = /[\u3000-\u303f\u3040-\u309f\u30a0-\u30ff\uff00-\uff9f\u4e00-\u9faf\u3400-\u4dbf]/
    //      0            1            2            3            4            5
    return jp.test(ch)
}