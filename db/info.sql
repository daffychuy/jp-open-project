CREATE TABLE IF NOT EXISTS info (
    id serial not NULL,
    sense_id int REFERENCES sense (id),
    info text not NULL,
    PRIMARY KEY (id, sense_id) 
)