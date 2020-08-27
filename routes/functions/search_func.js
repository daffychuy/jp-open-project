const Promise = require('bluebird');
const jp = require('wanakana');
const validator = require('validator');

exports.search = [
    async function (req, res, next) {
        let query = req.query;
        let keyword = validator.escape(query.keyword);
        console.log("Keyword: " + keyword);
        console.log("isRomaji: " + jp.isRomaji(keyword));
        console.log("isJapanese: " + jp.isJapanese(keyword));
        console.log("isMixed: " + jp.isMixed(keyword));
        console.log("Strip Okurigana: " + jp.stripOkurigana(keyword));
        console.log("Tokenize: " + jp.tokenize(keyword));
        console.log("toRomaji: " + jp.toRomaji(keyword));
        if (jp.isJapanese(keyword)) {
            // Gotta split accordingly
            let split_char = jp.tokenize(keyword)
        } else {
            // Need to process the word, and convert into japanaese character first
            let converted_keyword = jp.toHiragana(keyword)

        }
        res.status(200).send({
            "Keyword": keyword,
            "isRomaji": jp.isRomaji(keyword),
            "isJapanese": jp.isJapanese(keyword),
            "isMixed": jp.isMixed(keyword),
            "Strip Okurigana": jp.stripOkurigana(keyword),
            "Stripped Letters": jp.tokenize(keyword),
            "toRomaji": jp.toRomaji(keyword)
        });
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