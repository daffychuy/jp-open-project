#!/bin/bash

config="./database.conf"
logfile="./logs/errorlog.`uname -n`.log"
if [ -f "$config" ]
    then
        echo "Loading $config file"
        . $config
        
        {
            PGPASSWORD=${password} psql -U ${username} -p ${port} -h ${hostname} ${database} < ./JMDict_id.sql
            PGPASSWORD=${password} psql -U ${username} -p ${port} -h ${hostname} ${database} < ./language.sql
            PGPASSWORD=${password} psql -U ${username} -p ${port} -h ${hostname} ${database} < ./JLPT_Level.sql
            PGPASSWORD=${password} psql -U ${username} -p ${port} -h ${hostname} ${database} < ./kanji.sql
            PGPASSWORD=${password} psql -U ${username} -p ${port} -h ${hostname} ${database} < ./kana.sql
            PGPASSWORD=${password} psql -U ${username} -p ${port} -h ${hostname} ${database} < ./reading_mappings.sql
            PGPASSWORD=${password} psql -U ${username} -p ${port} -h ${hostname} ${database} < ./sense.sql
            PGPASSWORD=${password} psql -U ${username} -p ${port} -h ${hostname} ${database} < ./partsOfSpeech.sql
            PGPASSWORD=${password} psql -U ${username} -p ${port} -h ${hostname} ${database} < ./antonym.sql
            PGPASSWORD=${password} psql -U ${username} -p ${port} -h ${hostname} ${database} < ./field.sql
            PGPASSWORD=${password} psql -U ${username} -p ${port} -h ${hostname} ${database} < ./misc.sql
            PGPASSWORD=${password} psql -U ${username} -p ${port} -h ${hostname} ${database} < ./info.sql
            PGPASSWORD=${password} psql -U ${username} -p ${port} -h ${hostname} ${database} < ./dialect.sql
            PGPASSWORD=${password} psql -U ${username} -p ${port} -h ${hostname} ${database} < ./languageSource.sql
            PGPASSWORD=${password} psql -U ${username} -p ${port} -h ${hostname} ${database} < ./meaning.sql
            PGPASSWORD=${password} psql -U ${username} -p ${port} -h ${hostname} ${database} < ./related_kanji.sql
            PGPASSWORD=${password} psql -U ${username} -p ${port} -h ${hostname} ${database} < ./related_kana.sql
            PGPASSWORD=${password} psql -U ${username} -p ${port} -h ${hostname} ${database} < ./related_to.sql
            PGPASSWORD=${password} psql -U ${username} -p ${port} -h ${hostname} ${database} < ./Individual_kanji.sql
            PGPASSWORD=${password} psql -U ${username} -p ${port} -h ${hostname} ${database} < ./kun_reading.sql
            PGPASSWORD=${password} psql -U ${username} -p ${port} -h ${hostname} ${database} < ./on_reading.sql
            PGPASSWORD=${password} psql -U ${username} -p ${port} -h ${hostname} ${database} < ./kanji_meaning.sql
            PGPASSWORD=${password} psql -U ${username} -p ${port} -h ${hostname} ${database} < ./name_reading.sql
        } > /dev/null 2> "$logfile"; [ -s "$logfile" ] || rm -f "$logfile"
            if [ -f "$logfile" ]
            then
              if grep ERROR "$logfile"
                then
                  echo "An error may have occurred while creating tables, please check $logfile for detailed errors"
                  echo "If you believe this is an error on our side, delete the log file then proceed once again"
              else
                echo "Database created successfully"
              fi
        fi
    else
        echo "$config not found."
    fi