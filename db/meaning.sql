CREATE TABLE IF NOT EXISTS meaning (
    id serial not NULL,
    sense_id int REFERENCES sense (id),
    meaning text NULL,
    lang_id int REFERENCES language (id),
    type varchar(50) NULL,
    PRIMARY KEY (id, sense_id) 
)