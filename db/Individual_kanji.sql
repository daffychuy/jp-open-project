CREATE TABLE IF NOT EXISTS individual_Kanji (
    kanji varchar(50),
    JLPT_lvl int REFERENCES JLPT_Level (id),
    frequency int NULL,
    grade_learnt int NOT NULL,
    strokes int NOT NULL,
    PRIMARY KEY (kanji)
)