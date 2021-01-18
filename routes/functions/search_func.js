// Japanese conversions
import * as jp from "wanakana";
// Validation tool
import * as validator from "validator";
// Database
import JMDict from "../../models/JMDict";
import v8 from "v8";
import * as GLOBAL from "../../models/global";
import * as recognizer from "../../middleware/recognize_verb";
// Everything Kuroshiro related for translating Japanese to ___
import Kuroshiro from "kuroshiro";
import KuromojiAnalyzer from "kuroshiro-analyzer-kuromoji";
const kuroshiro = new Kuroshiro();
kuroshiro.init(new KuromojiAnalyzer());

const search = async (req, res) => {
	let new_result = {
		meta: {
			status: 200,
			next_page: false,
		},
		data: [],
	};
	if (!req.query.keyword) {
		new_result.meta.status = GLOBAL.INVALID;
		return res.status(GLOBAL.INVALID).send(new_result);
	}
	let keyword = validator.escape(req.query.keyword);
	let page = 1;
	if (req.query.page) {
		let temp_page = validator.escape(req.query.page);
		if (validator.isInt(temp_page)) page = temp_page;
	}
	recognizer.recognize_verb(keyword);
	// First convert everything to hiragana
	let hiragana = jp.toHiragana(keyword);

	// Case of when the whole thing is japanese
	if (jp.isJapanese(hiragana)) {
		if (jp.isHiragana(hiragana)) {
			return search_hiragana(hiragana, page, new_result, res);
		} else if (jp.isKanji(hiragana)) {
			return search_kanji(keyword, hiragana, new_result, res, page);
		}
	}
};

const search_hiragana = async (hiragana, page, new_result, res) => {
	if (page > 1) {
		Promise.all([
			JMDict.find({
				"Japanese.kana": { $regex: `^${hiragana}.+$`, $options: "m" },
			})
				.sort({ "Japanese.kana": "asc" })
				.limit(11)
				.skip(page * 10),
		]).then(async ([rest]) => {
			if (rest.length > 10) {
				new_result.meta.next_page = true;
				rest = rest.slice(0, 10);
			}
			let res2 = await format_related(rest, hiragana, "kana");
			if (!res2) {
				// Need to skip and give another kind of response
				res.status(GLOBAL.SUCCESS).send();
			} else {
				// Need to process slug here
				for (let i of res2) {
					i.slug = typeof i.Japanese[0].kanji !== "undefined" ? i.Japanese[0].kanji : i.Japanese[0].kana;
				}
				res2.sort(function (a, b) {
					// ASC  -> a.length - b.length
					// DESC -> b.length - a.length
					return a.slug.length - b.slug.length;
				});
				new_result.data = res2;

				res.status(GLOBAL.SUCCESS).send(new_result);
			}
		});
	} else {
		Promise.all([
			JMDict.find({ "Japanese.kana": { $regex: `^${hiragana}$`, $options: "m" } }).sort({
				"Japanese.kana": "asc",
			}),
			JMDict.find({
				"Japanese.kana": { $regex: `^${hiragana}.+$`, $options: "m" },
			})
				.sort({ "Japanese.kana": "asc" })
				.limit(11),
		]).then(async ([singleResult, rest]) => {
			if (rest.length > 10) {
				new_result.meta.next_page = true;
				rest = rest.slice(0, 10);
			}
			let res1 = await format_related(singleResult, hiragana, "kana");
			let res2 = await format_related(rest, hiragana, "kana");
			if (!res1 && !res2) {
				// Need to skip and give another kind of response
				res.status(GLOBAL.SUCCESS).send();
			} else {
				// Need to process slug here
				for (let i of res1) {
					i.slug = typeof i.Japanese[0].kanji !== "undefined" ? i.Japanese[0].kanji : i.Japanese[0].kana;
				}
				for (let i of res2) {
					i.slug = typeof i.Japanese[0].kanji !== "undefined" ? i.Japanese[0].kanji : i.Japanese[0].kana;
				}
				res2.sort(function (a, b) {
					// ASC  -> a.length - b.length
					// DESC -> b.length - a.length
					return a.slug.length - b.slug.length;
				});
				new_result.data = res1.concat(res2);

				res.status(GLOBAL.SUCCESS).send(new_result);
			}
		});
	}
};

const search_kanji = async (keyword, hiragana, new_result, res, page) => {
	// const kanji_to_hiragana = await kuroshiro.convert(keyword, { to: "hiragana" });
	if (page > 1) {
		// TO_IMPLEMENT
	} else {
		Promise.all([
			JMDict.find({ "Japanese.kanji": { $regex: `^${hiragana}$`, $options: "m" } }).sort({
				"Japanese.kanji": "asc",
			}),
			JMDict.find({
				"Japanese.kanji": { $regex: `^${hiragana}.+$`, $options: "m" },
			})
				.sort({ "Japanese.kanji": "asc" })
				.limit(11),
		]).then(async ([singleResult, rest]) => {
			if (rest.length > 10) {
				new_result.meta.next_page = true;
				rest = rest.slice(0, 10);
			}
			let res1 = await format_related(singleResult, hiragana, "kanji");
			let res2 = await format_related(rest, hiragana, "kanji");
			if (!res1 && !res2) {
				// Need to skip and give another kind of response
				res.status(GLOBAL.SUCCESS).send();
			} else {
				// Need to process slug here
				for (let i of res1) {
					i.slug = typeof i.Japanese[0].kanji !== "undefined" ? i.Japanese[0].kanji : i.Japanese[0].kana;
				}
				for (let i of res2) {
					i.slug = typeof i.Japanese[0].kanji !== "undefined" ? i.Japanese[0].kanji : i.Japanese[0].kana;
				}
				res2.sort(function (a, b) {
					// ASC  -> a.length - b.length
					// DESC -> b.length - a.length
					return a.slug.length - b.slug.length;
				});
				new_result = res1.concat(res2);

				res.status(GLOBAL.SUCCESS).send(new_result);
			}
		});
	}
};

const format_related = async (datas, query, source) => {
	if (!datas) return [];
	let out = [];
	let word = [];
	for (let data of datas) {
		let temp = v8.deserialize(v8.serialize(GLOBAL.JAP_TEMPLATE));
		if (data.JMdict_id) temp.attribution.jmdict = true;

		for (let jap of data.Japanese) {
			switch (source) {
			case "kana":
				if (!jap.kana) break;
				if (jap.kana.includes(query) || jap.kana.includes(jp.toKatakana(query))) {
					temp.Japanese.push(jap);
					if (jap.kanji_common || jap.kana_common) temp.is_common = true;
					delete jap.kanji_common;
					delete jap.kana_common;
					word.push(jap.kana);
				}
				break;
			case "kanji":
				if (!jap.kanji) break;
				if (jap.kanji.includes(query)) {
					temp.Japanese.push(jap);
					if (jap.kanji_common || jap.kana_common) temp.is_common = true;
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
			if (sense.appliesToKanji.includes("*") || sense.appliesToKana.includes("*")) {
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
