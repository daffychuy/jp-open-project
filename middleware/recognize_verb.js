import * as Conjugator from "./jp-verb-deconjugator/index";

const recognize_verb = async (word) => {
	console.log(Conjugator.unconjugate(word));
};

module.exports = {
	recognize_verb,
};
