set -o allexport; source ../.env; set +o allexport

if [ ! -d "./JMdict Kanjidic files/JMdict/" ]
then 
    unzip "./JMdict Kanjidic files.zip"
fi
mongoimport --db ${DB_NAME} --collection JMDict \
          --host ${DB_HOST} --port ${DB_PORT} \
          --username ${DB_USER} --password ${DB_PASS} \
          --drop --file "./JMdict Kanjidic files/JMdict/Finalize_JMdict_e.json" --jsonArray