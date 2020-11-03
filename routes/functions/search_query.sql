DROP FUNCTION IF EXISTS search_kana(character);
CREATE OR REPLACE FUNCTION search_kana(word char)

RETURNS TABLE(JMDICT_ID INTEGER, kanji_id INTEGER, kana_id INTEGER, slug CHARACTER VARYING, reading CHARACTER VARYING, sense_id INTEGER, expl json,
antonym json, category json, misc json, info json, dialect json, lang CHARACTER VARYING, wasei BOOLEAN, languageSourceText json,
meaning json, meaning_type json, meaning_lang json, related_words json) AS
$$
DECLARE
    kana_var RECORD;
BEGIN
    FOR kana_var IN
        SELECT * FROM kana as k
        WHERE k.reading = word
    LOOP
        RETURN QUERY
            WITH RECURSIVE mapping_res AS (SELECT kana_var.jmdict_id, reading.kanji_id, reading.kana_id, kan.slug, kana_var.reading, re_kana.sense_id
            FROM reading_mappings as reading, kanji as kan, related_kana as re_kana, related_kanji as re_kanji
            WHERE (reading.kana_id = kana_var.id and kan.id = reading.kanji_id) and
                (re_kana.kana_id = kana_var.id and re_kanji.kanji_id = kan.id and re_kana.sense_id = re_kanji.sense_id))

            SELECT
                mapping.jmdict_id, mapping.kanji_id, mapping.kana_id, mapping.slug, mapping.reading, mapping.sense_id,
                   array_to_json(array_agg(DISTINCT p.expl)), array_to_json(array_agg(DISTINCT a.antonym)), array_to_json(array_agg(DISTINCT f.category)),
                   array_to_json(array_agg(DISTINCT misc.misc)), array_to_json(array_agg(DISTINCT info.info)), array_to_json(array_agg(DISTINCT dialect.dialect)),
                   L.lang, L.wasei, array_to_json(array_agg(DISTINCT L.text)), array_to_json(array_agg(DISTINCT m.meaning)),
                   array_to_json(array_agg(DISTINCT m.type)), array_to_json(array_agg(DISTINCT m.lang_id)) AS LANG_ID, array_to_json(array_agg(DISTINCT related_to.slug))
            FROM
                mapping_res AS mapping
            LEFT JOIN
                partsofspeech AS p ON p.sense_id = mapping.sense_id
            LEFT JOIN
                antonym AS a ON a.sense_id = mapping.sense_id
            LEFT JOIN
                field AS f ON f.sense_id = mapping.sense_id
            LEFT JOIN
                misc ON misc.sense_id = mapping.sense_id
            LEFT JOIN
                info on info.sense_id = mapping.sense_id
            LEFT JOIN
                dialect on dialect.sense_id = mapping.sense_id
            LEFT JOIN
                languagesource AS L on L.sense_id = mapping.sense_id
            LEFT JOIN
                meaning AS m ON m.sense_id = mapping.sense_id
            LEFT JOIN
                related_to ON related_to.sense_id = mapping.sense_id
            GROUP BY mapping.jmdict_id, mapping.kanji_id, mapping.kana_id, mapping.slug, mapping.reading, mapping.sense_id, L.lang, L.wasei
            ;

    end loop;
    RETURN;
END
$$ LANGUAGE plpgsql;