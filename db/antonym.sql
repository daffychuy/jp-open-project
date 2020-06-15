CREATE TABLE IF NOT EXISTS antonym (
    id serial not NULL,
    sense_id int REFERENCES sense (id),
    antonym varchar(50) not NULL,
    PRIMARY KEY (id, sense_id) 
)