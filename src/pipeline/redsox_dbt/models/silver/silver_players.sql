
SELECT DISTINCT ON (player_id)
    player_id,
    raw_json->'person'->>'fullName' AS player_name,
    raw_json->'position'->>'abbreviation' AS primary_position,
    raw_json->>'jerseyNumber' AS jersey_number,
    CURRENT_DATE AS valid_from,
    NULL::DATE AS valid_to,
    TRUE AS is_current
FROM {{ source('bronze', 'player_game_stats') }}
ORDER BY player_id, ingested_at DESC