CREATE TABLE IF NOT EXISTS kanji (
    id serial NOT NULL,
    slug varchar(50) NULL,
    is_common boolean not NULL DEFAULT False,
    JMDict_id int references JMDict_id (id) ON DELETE CASCADE,
    JLPT_lvl int references JLPT_Level (id) DEFAULT NULL,
    PRIMARY KEY (id)
)