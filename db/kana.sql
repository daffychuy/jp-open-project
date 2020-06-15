CREATE TABLE IF NOT EXISTS kana (
    id serial not NULL,
    reading varchar(50) not NULL,
    is_common boolean not NULL,
    lang_id int REFERENCES language (id),
    JMDict_id int REFERENCES JMDict_id (id) ON DELETE CASCADE,
    JLPT_lvl int REFERENCES JLPT_Level (id),
    PRIMARY KEY (id)
)