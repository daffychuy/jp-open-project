import * as Conjugator from "./jp-verb-deconjugator/index";

const recognize_verb = async (word) => {
	console.log(JSON.stringify(Conjugator.unconjugate(word), null, 2));
};

module.exports = {
	recognize_verb,
};
