import json
import copy
import psycopg2
import sys
from tqdm import tqdm

JMDICT = ''
try:
    conn = None
    conn = psycopg2.connect(database ="daffy-jp", user = "daffy", 
                        password = "daffychu0710", host = "daffychuy.io",  
                        port = "5432")
    cur = conn.cursor()
    print("Connected to database")
except (Exception, psycopg2.Error) as error:
    if not conn:
        raise Exception("Failed to conenct to database")    

def Load_JSON(file):
    print("Attemping to load json file to program")
    with open(file) as f:
        file = json.load(f)
        return file

def INSERT_Language():
    """
        ENG : 1
    """
    ENG = "INSERT INTO language (id, language) VALUES (1, 'eng')"
    cur.execute(ENG)
    conn.commit()
    return

def JMDict_db():
    FAILED = []
    inserted = 1
    file_name = "Finalize_JMdict_e.json"
    for data in tqdm(iter(Load_JSON(file_name))):
        KANJI_MAPPING, KANA_MAPPING = {}, {}
        sense_ids = []
        # * Getting JMDict id into the database first
        JMDict_id = data['JMdict_id']
        # ! JMDict_id table
        INSERT_ID = f"INSERT INTO JMDict_id (id) VALUES (%s)"
        cur.execute(INSERT_ID, (JMDict_id,))

        # Logging purpose
        sys.stdout.flush()
        sys.stdout.write(f" Inserting data # {inserted} with JMdict_id: {JMDict_id} --- Failed: \033[91m {len(FAILED)} \033[0m")

        # * Need to insert sense to allow relation between kanaji, kana and sense
        Senses = data['sense']
        sense_id = None
        # ! senses Table
        for i in range(len(Senses)):
            INSERT_SENSE = f"INSERT INTO sense VALUES (DEFAULT) RETURNING id"
            cur.execute(INSERT_SENSE)
            sense_id = cur.fetchall()[0][0]
            sense_ids.append(sense_id)
        
            
        # * Need to insert kanji and kana
        Japanese = data['Japanese']
        for d in Japanese:
            Kanji_id, Kana_id = 0, 0
            if d['kanji']:
                # ! kanji table
                INSERT_KANJI = f"INSERT INTO kanji (slug, is_common, JMDict_id) VALUES (%s, %s, %s) RETURNING id"
                cur.execute(INSERT_KANJI, (d['kanji'], d['kanji_common'], JMDict_id))
                Kanji_id = cur.fetchall()[0][0]
                KANJI_MAPPING.setdefault(d['kanji'], Kanji_id)
            if d['kana']:
                # ! kana table
                INSERT_KANA = f"INSERT INTO kana (reading, is_common, JMDict_id) VALUES (%s, %s, %s) RETURNING id"
                cur.execute(INSERT_KANA, (d['kana'], d['kana_common'], JMDict_id))
                Kana_id = cur.fetchall()[0][0]
                KANA_MAPPING.setdefault(d['kana'], Kana_id)
            if Kanji_id > 0 and Kana_id > 0:
                # ! reading_mappings table
                INSERT_READING_MAPPING = f"INSERT INTO reading_mappings (kanji_id, kana_id) VALUES (%s, %s)"
                cur.execute(INSERT_READING_MAPPING, (Kanji_id, Kana_id))

        for s in range(len(Senses)):
            sense_id = sense_ids[s]
            for speech in Senses[s]['partsOfSpeech']:
                INSERT_SPEECH = f"INSERT INTO partsOfSpeech (sense_id, expl) VALUES (%s, %s)"
                cur.execute(INSERT_SPEECH, (sense_id, speech))
            for applies in Senses[s]['appliesToKanji']:
                if KANJI_MAPPING:
                    if applies == "*":
                        for k_id in KANJI_MAPPING.values():
                            INSERT_RELATED = f"INSERT INTO Related_Kanji (kanji_id, sense_id) VALUES (%s, %s)"
                            cur.execute(INSERT_RELATED, (k_id, sense_id))
                    else:
                        try:
                            k_id = KANJI_MAPPING[applies]
                            INSERT_RELATED = f"INSERT INTO Related_Kanji (kanji_id, sense_id) VALUES (%s, %s)"
                            cur.execute(INSERT_RELATED, (k_id, sense_id))
                        except Exception as e:
                            FAILED.append(e)
            for applies in Senses[s]['appliesToKana']:
                if KANA_MAPPING:
                    if applies == "*":
                        for k_id in KANA_MAPPING.values():
                            INSERT_RELATED = f"INSERT INTO Related_kana (kana_id, sense_id) VALUES (%s, %s)"
                            cur.execute(INSERT_RELATED, (k_id, sense_id))
                    else:
                        try:
                            k_id = KANA_MAPPING[applies]
                            INSERT_RELATED = f"INSERT INTO Related_kana (kana_id, sense_id) VALUES (%s, %s)"
                            cur.execute(INSERT_RELATED, (k_id, sense_id))
                        except Exception as e:
                            FAILED.append(e)
            for related in Senses[s]['related']:
                # Need to call database to see what id it belongs to
                # is_kanji = 1
                # search = f"SELECT id FROM kanji WHERE slug = '{related}'"
                # cur.execute(search)
                # result = cur.fetchall()
                # if not result:
                #     search = f"SELECT id FROM kana WHERE slug = {related}"
                #     cur.execute(search)
                #     result = cur.fetchall()
                #     is_kanji = 0

                # result = result[0][0]
                INSERT_RELATED_TO = f"INSERT INTO Related_To (sense_id, slug) VALUES (%s, %s)"
                cur.execute(INSERT_RELATED_TO, (sense_id, related))
            for antonym in Senses[s]['antonym']:
                INSERT_ANTONYM = f"INSERT INTO antonym (sense_id, antonym) VALUES (%s %s)"
                cur.execute(INSERT_ANTONYM, (sense_id, antonym))
            for field in Senses[s]['field']:
                INSERT_FIELD = f"INSERT INTO field (sense_id, category) VALUES (%s, %s)"
                cur.execute(INSERT_FIELD, (sense_id, field))
            for misc in Senses[s]['misc']:
                INSERT_MISC = f"INSERT INTO misc (sense_id, misc) VALUES (%s, %s)"
                cur.execute(INSERT_MISC, (sense_id, misc))
            for info in Senses[s]['info']:
                INSERT_INFO = f"INSERT INTO info (sense_id, info) VALUES (%s, %s)"
                cur.execute(INSERT_INFO, (sense_id, info))
            for dialect in Senses[s]['dialect']:
                INSERT_DIALECT = f"INSERT INTO dialect (sense_id, dialect) VALUES (%s, %s)"
                cur.execute(INSERT_DIALECT, (sense_id, dialect))
            for source in Senses[s]['languageSource']:
                INSERT_LANG = f"INSERT INTO languageSource (sense_id, lang, wasei, text) VALUES (%s, %s, %s, %s)'"
                cur.execute(INSERT_LANG, (sense_id, source['lang'], source['wasei'], source['text']))
            for gloss in Senses[s]['gloss']:
                INSERT_MEANING = f"INSERT INTO meaning (sense_id, meaning, lang_id, type) VALUES (%s, %s, %s, %s)"
                cur.execute(INSERT_MEANING, (sense_id, gloss['text'], 1, gloss['type']))
        # Need to commit changes else it does not register
        conn.commit()
        inserted += 1


if __name__ == "__main__":
    INSERT_Language()
    JMDict_db()
    # cur.execute("INSERT INTO JMDict_id (id) VALUES (1)")
    # cur.execute("SELECT * FROM JMDict_id")
    # print(cur.fetchall())
    # print(cur.itersize)
    cur.close()
    conn.close()