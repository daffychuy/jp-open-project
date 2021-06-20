CREATE TABLE IF NOT EXISTS related_kana (
    kana_id int REFERENCES kana (id),
    sense_id int REFERENCES sense (id)
)