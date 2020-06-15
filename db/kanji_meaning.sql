CREATE TABLE IF NOT EXISTS kanji_meaning (
    meaning text NOT NULL,
    kanji varchar(50) REFERENCES individual_kanji (kanji) ON DELETE CASCADE,
    primary key (meaning, kanji)
)