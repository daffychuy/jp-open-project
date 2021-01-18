import json
import copy
import psycopg2
import sys
# from tqdm import tqdm
import curses
import time
from datetime import datetime

stdscr = curses.initscr()
JMDICT = ''
try:
    conn = None
    conn = psycopg2.connect(database ="", user = "", 
                        password = "", host = "",  
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

def INSERT_JLPT():
    """
        Level 5 : 5
        Level 4 : 4
        Level 3 : 3
        Level 2 : 2
        Level 1 : 1
    """
    cur.execute("INSERT INTO JLPT_level (level) VALUES (1)")
    cur.execute("INSERT INTO JLPT_level (level) VALUES (2)")
    cur.execute("INSERT INTO JLPT_level (level) VALUES (3)")
    cur.execute("INSERT INTO JLPT_level (level) VALUES (4)")
    cur.execute("INSERT INTO JLPT_level (level) VALUES (5)")
    conn.commit()
    return 


def JMDict_db():

    with open("Log", "w") as f:
        start_time = time.time()
        FAILED = []
        inserted = 1
        file_name = "Finalize_JMdict_e.json"
        for data in iter(Load_JSON(file_name)):
            KANJI_MAPPING, KANA_MAPPING = {}, {}
            sense_ids = []
            # * Getting JMDict id into the database first
            JMDict_id = data['JMdict_id']
            # ! JMDict_id table
            INSERT_ID = f"INSERT INTO JMDict_id (id) VALUES (%s)"
            cur.execute(INSERT_ID, (JMDict_id,))

            # Logging purpose
            stdscr.refresh()
            stdscr.addstr(0, 0, f"Time elapsed: {round(time.time() - start_time, 2)} seconds")
            stdscr.addstr(1, 0, f"Inserting data # {inserted} with JMdict_id: {JMDict_id} --- Failed: {len(FAILED)}")
            stdscr.addstr(2, 0, f"Failed: {FAILED}")

            now = datetime.now()

            current_time = now.strftime("%H:%M:%S")
            f.write(f"[{current_time}] Inserting data # {inserted} with JMdict_id: {JMDict_id} FAILED: {FAILED}\n")

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
                    INSERT_ANTONYM = f"INSERT INTO antonym (sense_id, antonym) VALUES (%s, %s)"
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
                    INSERT_LANG = f"INSERT INTO languageSource (sense_id, lang, wasei, text) VALUES (%s, %s, %s, %s)"
                    cur.execute(INSERT_LANG, (sense_id, source['lang'], source['wasei'], source['text']))
                for gloss in Senses[s]['gloss']:
                    INSERT_MEANING = f"INSERT INTO meaning (sense_id, meaning, lang_id, type) VALUES (%s, %s, %s, %s)"
                    cur.execute(INSERT_MEANING, (sense_id, gloss['text'], 1, gloss['type']))
            # Need to commit changes else it does not register
            conn.commit()
            inserted += 1

def Kanjidic():
    with open("Log", "w") as f:
        start_time = time.time()
        FAILED = []
        inserted = 1
        file_name = 'Kanjidic.json'
        for data in iter(Load_JSON(file_name)['words']):
            stdscr.refresh()
            stdscr.addstr(0, 0, f"Time elapsed: {round(time.time() - start_time, 2)} seconds")
            stdscr.addstr(1, 0, f"Inserting data # {inserted} with Kanji: {data['kanji']} --- Failed: {len(FAILED)}")
            stdscr.addstr(2, 0, f"Failed: {FAILED}")

            now = datetime.now()

            current_time = now.strftime("%H:%M:%S")
            f.write(f"[{current_time}] Inserting data # {inserted} with Kanji: {data['kanji']} FAILED: {FAILED}\n")

            INSERT_KANJI = f"INSERT INTO individual_kanji (kanji, jlpt_lvl, frequency, grade_learnt, strokes) VALUES (%s, %s, %s, %s, %s) returning kanji"
            cur.execute(INSERT_KANJI, (data['kanji'], data['jlpt'], data['freq'], data['grade'], data['strokes']))
            kanji = cur.fetchall()[0][0]
            for kun_reading in data['reading']['kun']:
                INSERT_KUN = f"INSERT INTO kun_reading (reading, kanji) VALUES (%s, %s)"
                cur.execute(INSERT_KUN, (kun_reading, kanji))
            for on_reading in data['reading']['on']:
                INSERT_ON = f"INSERT INTO on_reading (reading, kanji) VALUES (%s, %s)"
                cur.execute(INSERT_ON, (on_reading, kanji))
            for meaning in data['meaning']:
                INSERT_MEANING = f"INSERT INTO kanji_meaning (meaning, kanji, lang_id) VALUES (%s, %s, %s)"
                cur.execute(INSERT_MEANING, (meaning, kanji, 1))
            for name_reading in data['name_reading']:
                INSERT_NAME = f"INSERT INTO name_reading (reading, kanji) VALUES (%s, %s)"
                cur.execute(INSERT_NAME, (name_reading, kanji))
            conn.commit()
            inserted += 1

if __name__ == "__main__":
    
    try:
        # INSERT_Language()
        INSERT_JLPT()
        curses.noecho()
        curses.cbreak()
        Kanjidic()
        # JMDict_db()
    finally:
        cur.close()
        conn.close()
        curses.echo()
        curses.nocbreak()
        curses.endwin()