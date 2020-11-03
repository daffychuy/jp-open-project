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
                    
                    search_hiragana(hiragana);

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

async function search_hiragana(word) {
    const query = `SELECT * FROM kana WHERE reading Like $1;`;
    

    const kana = await Promise.resolve(pool.query(query, [word]));
    const reading_mapping = []
    // First catching to see if there are results given the current input word (Exact Match)
    if (kana.rows.length > 0) {
        kana.rows.forEach(ele => {
            const kana_id = ele.id;
            const kana_reading = ele.reading;
            const mapping = `SELECT * FROM reading_mappings WHERE kana_id = $1`;
            reading_mapping.push(Promise.resolve(pool.query(mapping, [kana_id])));
        });
        // We have to wait for all the outputs
        await Promise.all(reading_mapping);
        
        // From reading_mapping, get the kanji
    }
    console.log(reading_mapping);
}

async function search_hiragana_OLD(word) {
    let query = `SELECT * FROM kana WHERE reading LIKE $1;`;
    
    let res_query = Promise.all(
        [pool.query(query, [word])]
    ).then ((result, res_query) => {
        let rows = result[0].rows;
        let to_insert = []
        if (rows.length == 0) {
            // We need to perform another query search with front and back that includes this word
    
        } else {
            // ! WE'RE ONLY TRACKING THAT IT HAS KANJI FROM KANA 
            // Need to construct the found query into readable query
            // let to_insert = []
            let to_insert2 = []
            rows.forEach(ele => {
                
                let id = ele.id;
                let word_query = `SELECT * FROM reading_mappings WHERE kana_id = $1`;
                
                let s = Promise.all(
                    [pool.query(word_query, [id])]
                ).then (mapping_res => {
                    let temp_query = {}
                    try {
                        // Getting the basic kana info to add to kanji query
                        temp_query['reading'] = ele.reading;
                        temp_query['is_common'] = ele.is_common;
                        temp_query['jlpt_level_kana'] = ele.jlpt_lvl;
                        temp_query['kana_id'] = ele.id;

                        let mapping = mapping_res[0].rows[0];
                        // console.log(mapping)
                        if (mapping) {
                            let kanji_query = `SELECT * FROM kanji WHERE id = $1`;
                            Promise.all(
                                [pool.query(kanji_query, [mapping.kanji_id])]
                            ).then (result2 => {
                                let rows2 = result2[0].rows;
                                // console.log(rows2);
                                temp_query['kanji'] = rows2['slug']
                                temp_query['kanji_common'] = rows2['is_common']
                                temp_query['jlpt_level_kanji'] = rows['jlpt_lvl']
                            });
                        }
                        return temp_query
                        
                    } catch (error) {
                        console.log(error);
                    }
                    
                });
                to_insert2.push(s)
                
            });
            return to_insert2
        }     
    })
    console.log(res_query)
}