CREATE TABLE IF NOT EXISTS related_to (
    id serial not NULL,
    sense_id int REFERENCES sense (id) not NULL,
    kanji_id int REFERENCES kanji (id),
    kana_id int REFERENCES kana (id),
    PRIMARY KEY (id, sense_id)
)