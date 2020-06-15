CREATE TABLE IF NOT EXISTS languageSource (
    id serial not NULL,
    sense_id int REFERENCES sense (id),
    lang varchar(50) not NULL,
    wasei boolean not NULL DEFAULT False,
    text text not NULL,
    PRIMARY KEY (id, sense_id) 
)