CREATE TABLE IF NOT EXISTS reading_mappings (
    kanji_id int REFERENCES kanji (id),
    kana_id int REFERENCES kana (id),
    PRIMARY KEY (kanji_id, kana_id) 
)