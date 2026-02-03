SELECT
    game_id,
    player_id,
    raw_json->'person'->>'fullName' AS player_name,
    raw_json->'position'->>'abbreviation' AS position_played,
    raw_json->'stats'->'fielding'->>'putOuts' AS put_outs,
    raw_json->'stats'->'fielding'->>'assists' AS assists,
    raw_json->'stats'->'fielding'->>'errors' AS errors,
    raw_json->'stats'->'fielding'->>'chances' AS chances
FROM {{ source('bronze', 'player_game_stats') }}
WHERE (raw_json->'stats'->'fielding'->>'chances')::INTEGER > 0
