CREATE TABLE IF NOT EXISTS misc (
    id serial not NULL,
    sense_id int REFERENCES sense (id),
    misc text NULL,
    PRIMARY KEY (id, sense_id) 
)