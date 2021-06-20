CREATE TABLE IF NOT EXISTS partsOfSpeech (
    id serial not NULL,
    sense_id int REFERENCES sense (id),
    expl text NULL,
    PRIMARY KEY (id, sense_id) 
)