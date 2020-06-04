from xml.etree import ElementTree as ET 
import re
import copy
import json
from tqdm import tqdm

FILE = '../kanjidic2.xml'
TEMPLATE = {
    "kanji": "",
    "strokes": 0,
    "freq": None,
    "jlpt": None,
    "grade": 0,
    "reading": {
        "kun": [],
        "on": []
    },
    "meaning": [],
    "name_reading": []

}
def parse_misc(elements, new):
    for ele in elements:
        if ele.tag.lower() == "grade":
            new['grade'] = ele.text
        elif ele.tag.lower() == 'stroke_count':
            new['strokes'] = ele.text
        elif ele.tag.lower() == 'freq':
            new['freq'] = ele.text
        elif ele.tag.lower() == "jlpt":
            new['jlpt'] = ele.text

def parse_literal(elements, new):
    new['kanji'] = elements.text

def parse_rmgroup(elements, new):
    for ele in elements:
        if ele.tag.lower() == "reading":
            if ele.attrib:
                if ele.attrib['r_type'] == "ja_on":
                    new['reading']['on'].append(ele.text)
                elif ele.attrib['r_type'] == "ja_kun":
                    new['reading']['kun'].append(ele.text)
        elif ele.tag.lower() == "meaning":
            if ele.attrib:
                if ele.attrib['m_lang'] == "en":
                    new["meaning"].append(ele.text)
            else:
                new['meaning'].append(ele.text)

def parse_readings(elements, new):
    for ele in elements:
        if ele.tag.lower() == "rmgroup":
            parse_rmgroup(ele, new)
        elif ele.tag.lower() == "nanori":
            new['name_reading'].append(ele.text)

def xml_parser():
    i = 0
    f = ET.iterparse(FILE)
    DATA = []
    for event, elements in tqdm(f):
        if event == 'end' and elements.tag == 'character':
            new_ele = copy.deepcopy(TEMPLATE)
            for ele in elements.iter():
                if ele.tag.lower() == "literal":
                    parse_literal(ele, new_ele)
                elif ele.tag.lower() == "reading_meaning":
                    parse_readings(ele, new_ele)
                elif ele.tag.lower() == "misc":
                    parse_misc(ele, new_ele)
            DATA.append(new_ele)
    return {"words": DATA}

def xml_to_json():
    """ Convert xml to json and save to file """
    file = open("Kanjidic.json", "w", encoding="utf8")
    print("Beginning conversion of Kanjidic")
    json.dump(xml_parser(), file, indent=2, ensure_ascii=False)
    print("Conversion finished")
    print("Saving to file...")
    file.close()

if __name__ == "__main__":
    xml_to_json()