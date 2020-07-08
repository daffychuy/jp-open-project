import json
import copy
from tqdm import tqdm

JMDICT = 'JMdict_e.json'

def Load_JSON():
    with open(JMDICT) as f:
        file = json.load(f)
        return file['words']

def Parse_JMdict():
    NEW = []
    for data in tqdm(iter(Load_JSON())):
        JAP = []
        new_data = {}
        new_data.setdefault("JMdict_id", data['id'])
        for i in data['kana']:
            if i['appliesToKanji'] == ["*"]:
                reading = i['text']
                if not data['kanji']:
                    JAP.append({"kanji": None, "kana": reading, "kanji_common": None, "kana_common": i['common']})
                for kanji in data['kanji']:
                    JAP.append({"kanji": kanji['text'], "kana": reading, "kanji_common": kanji['common'], "kana_common": i['common']})
            elif i['appliesToKanji'] == []:
                JAP.append({"kanji": None, "kana": i['text'], "kanji_common": None, "kana_common": i['common']})
            else:
                for k in i['appliesToKanji']:
                    for kanji in data['kanji']:
                        if kanji == k:
                            JAP.append({"kanji": k, "kana": i['text'], "kanji_common": kanji['common'], "kana_common": i['common']})
        new_data.setdefault("Japanese", JAP)
        new_data.setdefault("sense", data['sense'])
        NEW.append(new_data)

    return NEW


def xml_to_json():
    """ Convert xml to json and save to file """
    file = open("Finalize_JMdict_e.json", "w", encoding="utf8")
    print("Beginning organizing JMdict file to desired output")
    json.dump(Parse_JMdict(), file, indent=2, ensure_ascii=False)
    print("Conversion finished")
    print("Saving to file...")
    file.close()

if __name__ == "__main__":
    xml_to_json()
