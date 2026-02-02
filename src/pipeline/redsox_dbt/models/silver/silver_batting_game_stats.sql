
SELECT
    game_id,
    player_id,
    raw_json->'person'->>'fullName' AS player_name,
    (raw_json->>'battingOrder')::INTEGER / 100 AS batting_order,
    raw_json->'position'->>'abbreviation' AS position_played,
    (raw_json->'stats'->'batting'->>'atBats')::INTEGER AS at_bats,
    (raw_json->'stats'->'batting'->>'runs')::INTEGER AS runs,
    (raw_json->'stats'->'batting'->>'hits')::INTEGER AS hits,
    (raw_json->'stats'->'batting'->>'doubles')::INTEGER AS doubles,
    (raw_json->'stats'->'batting'->>'triples')::INTEGER AS triples,
    (raw_json->'stats'->'batting'->>'homeRuns')::INTEGER AS home_runs,
    (raw_json->'stats'->'batting'->>'rbi')::INTEGER AS rbi,
    (raw_json->'stats'->'batting'->>'basesOnBalls')::INTEGER AS walks,
    (raw_json->'stats'->'batting'->>'strikeOuts')::INTEGER AS strikeouts,
    (raw_json->'stats'->'batting'->>'stolenBases')::INTEGER AS stolen_bases,
    (raw_json->'stats'->'batting'->>'hitByPitch')::INTEGER AS hit_by_pitch,
    (raw_json->'stats'->'batting'->>'sacFlies')::INTEGER AS sac_flies,
    (raw_json->'stats'->'batting'->>'plateAppearances')::INTEGER AS plate_appearances
FROM {{ source('bronze', 'player_game_stats') }}
WHERE (raw_json->'stats'->'batting'->>'plateAppearances')::INTEGER > 0