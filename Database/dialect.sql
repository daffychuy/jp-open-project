CREATE TABLE IF NOT EXISTS dialect (
    id serial not NULL,
    sense_id int REFERENCES sense (id),
    dialect text NULL,
    PRIMARY KEY (id, sense_id) 
)