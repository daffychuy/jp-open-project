CREATE TABLE IF NOT EXISTS name_reading (
    reading text NOT NULL,
    kanji varchar(50) REFERENCES individual_kanji (kanji) ON DELETE CASCADE,
    primary key (reading, kanji)
)