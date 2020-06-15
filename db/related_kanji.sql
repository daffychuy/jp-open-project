CREATE TABLE IF NOT EXISTS related_kanji (
    kanji_id int REFERENCES kanji (id),
    sense_id int REFERENCES sense (id)
)