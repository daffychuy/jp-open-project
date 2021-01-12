from japaneseverbconjugator.src import JapaneseVerbFormGenerator as japaneseVerbFormGenerator
from japaneseverbconjugator.src.Utils import generate_nai_form
from japaneseverbconjugator.src.constants.EnumeratedTypes import VerbClass, Tense, Polarity, Formality
import romkan
import json
import time
from datetime import datetime
from tqdm import tqdm

class verb:
    def __init__(self):
        self.ichidan = ["Ichidan verb",
        "Ichidan verb - kureru special class",
        "Ichidan verb - zuru verb (alternative form of -jiru verbs)",

        ]

        # <!ENTITY v2a-s "Nidan verb with 'u' ending (archaic)">
        # <!ENTITY v4h "Yodan verb with `hu/fu' ending (archaic)">
        # <!ENTITY v4r "Yodan verb with `ru' ending (archaic)">
        # <!ENTITY v5aru "Godan verb - -aru special class">
        # <!ENTITY v5b "Godan verb with `bu' ending">
        # <!ENTITY v5g "Godan verb with `gu' ending">
        # <!ENTITY v5k "Godan verb with `ku' ending">
        # <!ENTITY v5k-s "Godan verb - Iku/Yuku special class">
        # <!ENTITY v5m "Godan verb with `mu' ending">
        # <!ENTITY v5n "Godan verb with `nu' ending">
        # <!ENTITY v5r "Godan verb with `ru' ending">
        # <!ENTITY v5r-i "Godan verb with `ru' ending (irregular verb)">
        # <!ENTITY v5s "Godan verb with `su' ending">
        # <!ENTITY v5t "Godan verb with `tsu' ending">
        # <!ENTITY v5u "Godan verb with `u' ending">
        # <!ENTITY v5u-s "Godan verb with `u' ending (special class)">
        # <!ENTITY v5uru "Godan verb - Uru old class verb (old form of Eru)">
        # <!ENTITY vi "intransitive verb">
        # <!ENTITY vk "Kuru verb - special class">
        # <!ENTITY vn "irregular nu verb">
        # <!ENTITY vr "irregular ru verb, plain form ends with -ri">
        # <!ENTITY vs "noun or participle which takes the aux. verb suru">
        # <!ENTITY vs-c "su verb - precursor to the modern suru">
        # <!ENTITY vs-s "suru verb - special class">
        # <!ENTITY vs-i "suru verb - included">

class conjugative:
    
    def __init__(self):
        self.jvfg = japaneseVerbFormGenerator.JapaneseVerbFormGenerator()

    def generate_all_conjugative(self, kana, kanji):
        type_class = self.recognize_type(romkan.to_roma(kana))
        if not type_class:
            return
        if kanji:
            return {
                "kana": self.generate_specified_type(kana, type_class),
                "kanji": self.generate_specified_type(kanji, type_class)
            }
        return {
            "kana": self.generate_specified_type(kana, type_class),
            "kanji": None
        }

    def recognize_type(self, word):
        if word.endswith(("suru", "kuru")):
            return VerbClass.IRREGULAR
        elif word.endswith(("iru", "eru")):
            return VerbClass.ICHIDAN
        elif word.endswith(("u")):
            return VerbClass.GODAN
        return

    def generate_specified_type(self, word, type_class):
        self.verbclass = type_class
        type_string = ""
        if type_class == VerbClass.IRREGULAR:
            type_string = "Group 3"
        elif type_class == VerbClass.GODAN:
            type_string = "Group 1"
        else:
            type_string = "Godan 2"
        try:
            return {
                "type": type_string,
                "Positive": {
                    "Present": self.jvfg.generate_plain_form(word, self.verbclass, Tense.NONPAST, Polarity.POSITIVE),
                    "Past": self.jvfg.generate_plain_form(word, self.verbclass, Tense.PAST, Polarity.POSITIVE),
                    "Te-form": self.jvfg.generate_te_form(word, self.verbclass),
                    "Conditional": self.jvfg.generate_conditional_form(word, self.verbclass, Formality.PLAIN, Polarity.POSITIVE),
                    "Volitional": self.jvfg.generate_volitional_form(word, self.verbclass, Formality.PLAIN, Polarity.POSITIVE),
                    "Potential": self.jvfg.generate_potential_form(word, self.verbclass, Formality.PLAIN, Polarity.POSITIVE),
                    "Imperative": self.jvfg.generate_imperative_form(word, self.verbclass, Formality.PLAIN, Polarity.POSITIVE),
                    "Provisional": self.jvfg.generate_provisional_form(word, self.verbclass, Formality.PLAIN ,Polarity.POSITIVE),
                    "Casuative": self.jvfg.generate_causative_form(word, self.verbclass, Formality.PLAIN,Polarity.POSITIVE),
                    "Passive": self.jvfg.generate_passive_form(word, self.verbclass, Formality.PLAIN, Polarity.POSITIVE),
                },
                "Negative": {
                    "Present": self.jvfg.generate_plain_form(word, self.verbclass, Tense.NONPAST, Polarity.NEGATIVE),
                    "Past": self.jvfg.generate_plain_form(word, self.verbclass, Tense.PAST, Polarity.NEGATIVE),
                    "Te-form": self.jvfg.generate_te_form(word, self.verbclass),
                    "Conditional": self.jvfg.generate_conditional_form(word, self.verbclass, Formality.PLAIN, Polarity.NEGATIVE),
                    "Volitional": self.jvfg.generate_volitional_form(word, self.verbclass, Formality.PLAIN, Polarity.NEGATIVE),
                    "Potential": self.jvfg.generate_potential_form(word, self.verbclass, Formality.PLAIN, Polarity.NEGATIVE),
                    "Imperative": self.jvfg.generate_imperative_form(word, self.verbclass, Formality.PLAIN, Polarity.NEGATIVE),
                    "Provisional": self.jvfg.generate_provisional_form(word, self.verbclass, Formality.PLAIN ,Polarity.NEGATIVE),
                    "Casuative": self.jvfg.generate_causative_form(word, self.verbclass, Formality.PLAIN,Polarity.NEGATIVE),
                    "Passive": self.jvfg.generate_passive_form(word, self.verbclass, Formality.PLAIN, Polarity.NEGATIVE),
                },
                "Masu": {
                    "Present": self.jvfg.generate_polite_form(word, self.verbclass, Tense.NONPAST, Polarity.POSITIVE),
                    "Past": self.jvfg.generate_polite_form(word, self.verbclass, Tense.PAST, Polarity.POSITIVE),
                    "Conditional": self.jvfg.generate_conditional_form(word, self.verbclass, Formality.POLITE, Polarity.POSITIVE),
                    "Volitional": self.jvfg.generate_volitional_form(word, self.verbclass, Formality.POLITE, Polarity.POSITIVE),
                    "Potential": self.jvfg.generate_potential_form(word, self.verbclass, Formality.POLITE, Polarity.POSITIVE),
                    "Imperative": self.jvfg.generate_imperative_form(word, self.verbclass, Formality.POLITE, Polarity.POSITIVE),
                    "Provisional": self.jvfg.generate_provisional_form(word, self.verbclass, Formality.POLITE ,Polarity.POSITIVE),
                    "Casuative": self.jvfg.generate_causative_form(word, self.verbclass, Formality.POLITE,Polarity.POSITIVE),
                    "Passive": self.jvfg.generate_passive_form(word, self.verbclass, Formality.POLITE, Polarity.POSITIVE),
                },
                "Masu-Negative": {
                    "Present": self.jvfg.generate_polite_form(word, self.verbclass, Tense.NONPAST, Polarity.NEGATIVE),
                    "Past": self.jvfg.generate_polite_form(word, self.verbclass, Tense.PAST, Polarity.NEGATIVE),
                    "Conditional": self.jvfg.generate_conditional_form(word, self.verbclass, Formality.POLITE, Polarity.NEGATIVE),
                    "Volitional": self.jvfg.generate_volitional_form(word, self.verbclass, Formality.POLITE, Polarity.NEGATIVE),
                    "Potential": self.jvfg.generate_potential_form(word, self.verbclass, Formality.POLITE, Polarity.NEGATIVE),
                    "Imperative": self.jvfg.generate_imperative_form(word, self.verbclass, Formality.POLITE, Polarity.NEGATIVE),
                    "Provisional": self.jvfg.generate_provisional_form(word, self.verbclass, Formality.POLITE ,Polarity.NEGATIVE),
                    "Casuative": self.jvfg.generate_causative_form(word, self.verbclass, Formality.POLITE,Polarity.NEGATIVE),
                    "Passive": self.jvfg.generate_passive_form(word, self.verbclass, Formality.POLITE, Polarity.NEGATIVE),
                },
            }
        except Exception as e:
            return
        
        

class words:
    def __init__(self, file_name, to_write):
        self.file_name = file_name
        self.conjugative = conjugative()
        self.write_to = open(to_write, 'w')

    def Load_JSON(self, file):
        print("Attemping to load json file to program")
        with open(file) as f:
            file = json.load(f)
            return file

    def parse_file(self):
        start_time = time.time()
        new_data = []
        with open("Log", "w") as f:
            for data in tqdm(iter(self.Load_JSON(self.file_name))):
                new_data.append(self.generate_conjugative(data, f))
            to_log = f"{datetime.now()} | Dumping file to json"
            print(to_log)
            f.write(to_log + "\n")
            json.dump(new_data, self.write_to, indent=2, ensure_ascii=False)
            to_log = f"{datetime.now()} | Finished dumping and executing"
            print(to_log)
            f.write(to_log + "\n")
            f.write(f"Total Time Taken: {time.time() - start_time}")
            
    def generate_conjugative(self, japanese, log):
        new_json = japanese
        new_json.setdefault("conjugative", [])
        for data in japanese['Japanese']:
            to_log = f"{datetime.now()} | Writing word kanji: {data['kanji']}, kana: {data['kana']}"
            tqdm.write(to_log)
            log.write(to_log + "\n")
            conj = self.conjugative.generate_all_conjugative(data['kana'], data['kanji'])
            if conj:
                new_json['conjugative'].append(self.conjugative.generate_all_conjugative(data['kana'], data['kanji']))
        return new_json

if __name__ == "__main__":
    jap = words("JMdict Kanjidic files/JMdict/Finalize_JMdict_e.json", "JMdict Kanjidic files/JMdict/JMdict_with_conjugative.json")
    jap.parse_file()