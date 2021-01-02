// Japanese conversions
import * as jp from "wanakana";
// Validation tool
import * as validator from "validator";
// Database
const JMDict = require("../../models/JMDict");
const v8 = require("v8");
const GLOBAL = require("../../models/global");
// Everything Kuroshiro related for translating Japanese to ___
// import Kuroshiro from "kuroshiro";
// import KuromojiAnalyzer from "kuroshiro-analyzer-kuromoji";
// const kuroshiro = new Kuroshiro();
// kuroshiro.init(new KuromojiAnalyzer());

const search = async (req, res) => {
	let keyword = validator.escape(req.query.keyword);
	// First convert everything to hiragana
	let hiragana = jp.toHiragana(keyword);
	let new_result = [];
	// Case of when the whole thing is japanese
	if (jp.isJapanese(hiragana)) {
		if (jp.isHiragana(hiragana)) {
			Promise.all([
				JMDict.find({
					"Japanese.kana": { $regex: `^${hiragana}$`, $options: "m" },
				}).sort({
					"Japanese.kana": "asc",
				}),
				JMDict.find({
					"Japanese.kana": {
						$regex: `^${hiragana}.+$`,
						$options: "m",
					},
					"Japanese.kana_common": true,
				})
					.sort({ "Japanese.kana": "asc" })
					.limit(10),
			]).then(async ([singleResult, rest]) => {
				let res1 = await format_related(singleResult, hiragana, "kana");
				let res2 = await format_related(rest, hiragana, "kana");
				if (!res1 && !res2) {
					// Need to skip and give another kind of response
					res.status(404).send();
				} else {
					// Need to process slug here
					for (let i of res1) {
						i.slug =
							typeof i.Japanese[0].kanji !== "undefined"
								? i.Japanese[0].kanji
								: i.Japanese[0].kana;
					}
					for (let i of res2) {
						i.slug =
							typeof i.Japanese[0].kanji !== "undefined"
								? i.Japanese[0].kanji
								: i.Japanese[0].kana;
					}
					res2.sort(function (a, b) {
						// ASC  -> a.length - b.length
						// DESC -> b.length - a.length
						return a.slug.length - b.slug.length;
					});
					new_result = res1.concat(res2);

					res.status(200).send(new_result);
				}
			});
		}
	}
};

const format_related = async (datas, query, source) => {
	if (!datas) return [];
	let out = [];
	let word = [];
	for (let data of datas) {
		let temp = v8.deserialize(v8.serialize(GLOBAL.JAP));
		if (data.JMdict_id) temp.attribution.jmdict = true;

		for (let jap of data.Japanese) {
			switch (source) {
				case "kana":
					if (!jap.kana) break;
					if (
						jap.kana.includes(query) ||
						jap.kana.includes(jp.toKatakana(query))
					) {
						temp.Japanese.push(jap);
						if (jap.kanji_common || jap.kana_common)
							temp.is_common = true;
						delete jap.kanji_common;
						delete jap.kana_common;
						word.push(jap.kana);
					}
					break;
				case "kanji":
					if (!jap.kanji) break;
					if (jap.kanji.includes(query)) {
						temp.Japanese.push(jap);
						if (jap.kanji_common || jap.kana_common)
							temp.is_common = true;
						delete jap.kanji_common;
						delete jap.kana_common;
						word.push(jap.kanji);
					}
					break;
				default:
					break;
			}
		}
		for (let sense of data.sense) {
			if (
				sense.appliesToKanji.includes("*") ||
				sense.appliesToKana.includes("*")
			) {
				delete sense.appliesToKana;
				delete sense.appliesToKanji;
				temp.sense.push(sense);
			} else {
				console.log(word);
				switch (source) {
					case "kana":
						for (let kana of sense.appliesToKana) {
							if (word.includes(kana)) {
								delete sense.appliesToKana;
								delete sense.appliesToKanji;
								temp.sense.push(sense);
							}
						}
						break;
					case "kanji":
						for (let kanji of sense.appliesToKanji) {
							if (word.includes(kanji)) {
								delete sense.appliesToKana;
								delete sense.appliesToKanji;
								temp.sense.push(sense);
							}
						}
						break;
				}
			}
		}
		out.push(temp);
	}
	return out;
};
module.exports = {
	search,
};
