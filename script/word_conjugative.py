from japaneseverbconjugator.src import JapaneseVerbFormGenerator as japaneseVerbFormGenerator
from japaneseverbconjugator.src.Utils import generate_nai_form
from japaneseverbconjugator.src.constants.EnumeratedTypes import VerbClass, Tense, Polarity, Formality
import romkan
import json
import time
from datetime import datetime
from tqdm import tqdm
import re

class verb:
    def __init__(self):
        self.group = {
            1: [],
            2: [],
            3: []
        }
        self.verb_tag = ['iv', 'v1', 'v1-s', 'v2a-s', 'v4h', 'v4r', 'v5aru', 'v5b', 'v5g', 'v5k', 'v5k-s', 'v5m', 'v5n', 'v5r', 'v5r-i', 'v5s', 'v5t', 'v5u', 'v5u-s', 'v5uru', 'vz', 'vi', 'vk', 'vn', 'vr', 'vs', 'vs-c', 'vs-s', 'vs-i', 'vt', 'v-unspec', 'v4k', 'v4g', 'v4s', 'v4t', 'v4n', 'v4b', 'v4m', 'v2k-k', 'v2g-k', 'v2t-k', 'v2d-k', 'v2h-k', 'v2b-k', 'v2m-k', 'v2y-k', 'v2r-k', 'v2k-s', 'v2g-s', 'v2s-s', 'v2z-s', 'v2t-s', 'v2d-s', 'v2n-s', 'v2h-s', 'v2b-s', 'v2m-s', 'v2y-s', 'v2r-s', 'v2w-s']
        self.parse_potential_verb("JMdict Kanjidic files/JMdict/JMdict_header.xml")
    
    def parse_potential_verb(self, file_name):
        with open(file_name, 'r') as f:
            for line in f:
                if re.search("^<!ENTITY .*>$", line):
                    data = re.search("^<!ENTITY (.*) \"(.*)\">$", line).groups()
                    if any(v in data[0] for v in self.verb_tag):
                        if "irregular" in data[1].lower() or any(v2 == data[0] for v2 in ["vs-s", "vk", "vs", "vs-c"]):
                            self.group[3].append(data[1])
                        elif "ichidan" in data[1].lower():
                            self.group[2].append(data[1])
                        elif "godan" in data[1].lower():
                            self.group[1].append(data[1])
                        else:
                            print(f"Group: {data[0]} | Meaning: {data[1]}")



class conjugative:
    
    def __init__(self):
        self.jvfg = japaneseVerbFormGenerator.JapaneseVerbFormGenerator()
        self.verb = verb()

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
    # jap = words("JMdict Kanjidic files/JMdict/Finalize_JMdict_e.json", "JMdict Kanjidic files/JMdict/JMdict_with_conjugative.json")
    # jap.parse_file()
    conjugative()