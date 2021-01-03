set -o allexport; source ../.env; set +o allexport
echo ${DB_HOST}

mongoimport --db ${DB_NAME} --collection JMDict \
          --host ${DB_HOST} --port ${DB_PORT} \
          --username ${DB_USER} --password ${DB_PASS} \
          --drop --file "./JMdict Kanjidic files/JMdict/Finalize_JMdict_e.json" --jsonArray