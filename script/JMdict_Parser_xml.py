from xml.etree import ElementTree as ET 
import re
import copy
import json
from tqdm import tqdm

FILE = 'JMdict_e'
TEMPLATE = {
    "id": 0,
    "kanji": [],
    "kana": [],
    "sense": []
}

KANJI_TEMPLATE = {
    "common": False,
    "text": "",
    "tags": []
}

KANA_TEMPLATE = {
    "common": False,
    "text": "",
    "tags": [],
    "appliesToKanji": []
}

LANG_TEMPLATE = {
    "lang": "",
    "wasei": False,
    "text": None
}

GLOSS_TEMPLATE = {
    "lang": "eng",
    "type": None,
    "text": None
}

SENSE_TEMPLATE = {
    "partsOfSpeech": [],
    "appliesToKanji": [],
    "appliesToKana": [],
    "related": [],
    "antonym": [],
    "field": [],
    "dialect": [],
    "misc": [],
    "info": [],
    "languageSource": [],
    "gloss": []
}

COMMON_list = ['^news[1-2]{1}$', '^ichi[1-2]{1}$', '^spec[1-2]$', '^gal[1-2]$', '^nf[0-9]{2}$']
COMMON_regex = re.compile('|'.join(COMMON_list))

JAP_CHAR = '[\u3000-\u303f\u3040-\u309f\u30a0-\u30ff\uff00-\uff9f\u4e00-\u9faf\u3400-\u4dbf]'
JAP_regex = re.compile(JAP_CHAR)

class Error(Exception):
   """ Base class for other exceptions """
   pass

class CharacterInvalidError(Error):
    """ Raised when character did not pass a check when it should've """
    pass

def character_checker(char):
    """ Checks to see if its a japanesae character i.e. kana, kanji etc. """
    return bool(re.match(JAP_regex, char))


def parse_rele(elements, new):
    """ Fill in the information about kana """
    doNotAdd = False
    kana = copy.deepcopy(KANA_TEMPLATE)
    for ele in elements:
        # Checking to see if its common
        if ele.tag.lower() == "re_pri":
            # See if word is common
            if re.match(COMMON_regex, ele.text):
                kana['common'] = True
        elif ele.tag.lower() == "reb":
            # The kana itself
            kana['text'] = ele.text
            # ! Unfortunately there are some other characters we can't really check
            # if (character_checker(ele.text)):
            #     kana['text'] = ele.text
            # else:
            #     raise CharacterInvalidError("Invalid character was detected\nInvalid Character: " + ele.text)
        elif ele.tag.lower() == "re_inf":
            # Indicating unusual aspects of the reading
            kana['tags'].append(ele.text)
        elif ele.tag.lower() == "re_restr":
            # Restriction to whether this kana belongs to certain kanji
            kana["appliesToKanji"].append(ele.text)
        elif ele.tag.lower() == "re_nokanji":
            # Cannot be used to read, therefore don't add this entry
            doNotAdd = True
    # If nothing is in the list, it can apply to every kanji
    if not kana['appliesToKanji']:
        kana['appliesToKanji'] = ['*']
    if not doNotAdd:
        new["kana"].append(kana)


def parse_ent_seq(element, new):
    """ Sets the ent_seq number for the specified element """
    new["id"] = element.text


def parse_sense(elements, new):
    """ Parse the sense element in the xml data set """
    sense = copy.deepcopy(SENSE_TEMPLATE)
    for ele in elements:
        if ele.tag.lower() == "stagr":
            # TODO: Fix this part, where it needs to be a list
            sense['appliesToKana'].append(ele.text)
        elif ele.tag.lower() == "stagk":
            # TODO: Fix this part, where it needs to be a list
            sense['appliesToKanji'].append(ele.text)
        elif ele.tag.lower() == "pos":
            sense['partsOfSpeech'].append(ele.text)
        elif ele.tag.lower() == "xref":
            # Could use an extra split method between dot
            sense['related'].append(ele.text)
        elif ele.tag.lower() == "ant":
            # Could use an extra split method between dot
            sense['antonym'].append(ele.text)
        elif ele.tag.lower() == "field":
            sense['field'].append(ele.text)
        elif ele.tag.lower() == "misc":
            sense['misc'].append(ele.text)
        elif ele.tag.lower() == "s_inf":
            sense['info'].append(ele.text)
        elif re.match("^lsource.*$", ele.tag.lower()):
            LANG = copy.deepcopy(LANG_TEMPLATE)
            orig = ET.tostring(ele, encoding='unicode', method='xml')
            if re.search('xml:lang=".*"', orig):
                LANG["lang"] = re.search('".*"', re.search('xml:lang=".*"', orig).group(0)).group(0).strip('"')
            if re.search('>.*<', orig):
                LANG["text"] = re.search('>.*<', orig).group(0)[1:-1]
            if (re.search('ls_wasei=".*"', orig)):
                wasei_bool = re.search('".*"', re.search('ls_wasei=".*"', orig).group(0)).group(0).strip('"')
                LANG["wasei"] = True if wasei_bool == "y" else False
            sense["languageSource"].append(LANG)
        elif ele.tag.lower() == "dial":
            sense['dialect'].append(ele.text)
        elif re.match("^gloss.*$", ele.tag.lower()):
            GLOSS = copy.deepcopy(GLOSS_TEMPLATE)
            orig = ET.tostring(ele, encoding='unicode', method='xml')
            if re.search('xml:lang=".*"', orig):
                GLOSS["lang"] = re.search('".*"', re.search('xml:lang=".*"', orig).group(0)).group(0).strip('"')
            if re.search('>.*<', orig):
                GLOSS['text'] = re.search('>.*<', orig).group(0)[1:-1]
            if re.search('g_type=".*"', orig):
                GLOSS["type"] = re.search('".*"', re.search('g_type="\S+"', orig).group(0)).group(0).strip('"')
            sense["gloss"].append(GLOSS)
    if not sense['appliesToKanji']:
        sense['appliesToKanji'] = ['*']
    if not sense['appliesToKana']:
        sense['appliesToKana'] = ['*']
    new['sense'].append(sense)

def parse_kele(elements, new):
    kanji = copy.deepcopy(KANJI_TEMPLATE)
    for ele in elements:
        # Checking to see if its common
        if ele.tag.lower() == "ke_pri":
            if re.match(COMMON_regex, ele.text):
                kanji['common'] = True
        elif ele.tag.lower() == "keb":
            # The Kanji itself
            kanji['text'] = ele.text
            # ! Unfortunately there are some other characters we can't really check
            # # Must verify the kanji is a valid kanji
            # if (character_checker(ele.text)):
            #     kanji['text'] = ele.text
            # else:
            #     raise CharacterInvalidError("Invalid character was detected\nInvalid Character: " + ele.text)
        elif ele.tag.lower() == "ke_inf":
            # Indicating unusual aspects of the reading
            kanji['tags'].append(ele.text)
    new['kanji'].append(kanji)


def xml_parser():
    """ Parse the large XML file using generator to speed up load time """
    f = ET.iterparse(FILE)
    DATA = []
    # main_element = f.getroot()
    for event, elements in tqdm(f):
        if event == 'end' and elements.tag == 'entry':
            new_ele = copy.deepcopy(TEMPLATE)
            for ele in elements.iter():
                if ele.tag == "ent_seq":
                    parse_ent_seq(ele, new_ele)
                elif ele.tag == "r_ele":
                    parse_rele(ele, new_ele)
                elif ele.tag == "k_ele":
                    parse_kele(ele, new_ele)
                elif ele.tag == "sense":
                    parse_sense(ele, new_ele)
            DATA.append(new_ele)
    return {"words": DATA}

def xml_to_json():
    """ Convert xml to json and save to file """
    file = open("JMdict_e.json", "w", encoding="utf8")
    print("Beginning conversion of JMdict_e")
    json.dump(xml_parser(), file, indent=2, ensure_ascii=False)
    print("Conversion finished")
    print("Saving to file...")
    file.close()

if __name__ == "__main__":
    xml_to_json()