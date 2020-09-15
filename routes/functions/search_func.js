const Promise = require('bluebird');
const pool = require('../../config');
const jp = require('wanakana');
const validator = require('validator');
const { StringDecoder } = require('string_decoder');

exports.search = [
    async function (req, res, next) {
        let query = req.query;
        let keyword = validator.escape(query.keyword);
        let output = {};
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
            
            // Algorithm. 
            // First convert it to hiragana, then search for the word in kana table
            // once we find a list of matching words, we perform mapping on it in the reading_mapping table
            // once we have full list of words, we check what the user originally inputted, if its kanji we try and match
            // otherwise we show the ones we think its right in order of??
            
            // ! Case 1: First item in the list is the word
            split_char.forEach(function(word) {
                if (word.trim()) {
                    let query_word = word.trim();
                    let hiragana = jp.stripOkurigana(jp.toHiragana(query_word));
                    
                    let query = `SELECT * FROM kana WHERE reading LIKE $1;`;
                    Promise.all(
                        [pool.query(query, [hiragana])]
                    ).then (result => {
                        let rows = result[0].rows;
                        console.log(rows);
                        
                        if (rows.length == 0) {
                            // We need to perform another query search with front and back that includes this word
                    
                        } else {
                            // Need to construct the found query into readable query
                            let to_insert = {}
                            rows.forEach(ele => {

                                let id = ele.id;
                                let word_query = `SELECT * FROM reading_mappings WHERE kana_id = $1`;
                                Promise.all(
                                    [pool.query(word_query, [id])]
                                ).then (mapping_res => {
                                    
                                    try {
                                        let mapping = mapping_res[0].rows[0];
                                        console.log(mapping)
                                        if (mapping.length > 0) {
                                            let kanji_query = `SELECT * FROM kanji WHERE id = $1`;
                                            Promise.all(
                                                [pool.query(kanji_query, [mapping.kanji_id])]
                                            )
                                        }
                                        
                                    } catch (error) {
                                        console.log(error);
                                    }
                                    
                                });
                                
                            });
                        }     
                    })

                }
            });
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