CREATE TABLE IF NOT EXISTS kun_reading (
    reading varchar(50),
    kanji varchar(50) REFERENCES individual_kanji (kanji) ON DELETE CASCADE,
    PRIMARY KEY (reading, kanji)
)