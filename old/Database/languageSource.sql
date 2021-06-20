CREATE TABLE IF NOT EXISTS languageSource (
    id serial not NULL,
    sense_id int REFERENCES sense (id),
    lang varchar(50) NULL,
    wasei boolean NULL DEFAULT False,
    text text NULL,
    PRIMARY KEY (id, sense_id) 
)