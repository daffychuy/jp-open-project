CREATE TABLE IF NOT EXISTS related_to (
    id serial not NULL,
    sense_id int REFERENCES sense (id) not NULL,
    slug text NULL,
    PRIMARY KEY (id, sense_id)
)