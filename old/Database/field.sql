CREATE TABLE IF NOT EXISTS field (
    id serial not NULL,
    sense_id int REFERENCES sense (id),
    category text NULL,
    PRIMARY KEY (id, sense_id) 
)