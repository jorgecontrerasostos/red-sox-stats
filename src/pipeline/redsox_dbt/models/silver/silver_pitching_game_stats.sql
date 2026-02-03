
SELECT
    game_id,
    player_id,
    raw_json->'person'->>'fullName' AS player_name,
    (raw_json->'stats'->'pitching'->>'inningsPitched')::DECIMAL AS innings_pitched,
    (raw_json->'stats'->'pitching'->>'hits')::INTEGER AS hits_allowed,
    (raw_json->'stats'->'pitching'->>'runs')::INTEGER AS runs_allowed,
    (raw_json->'stats'->'pitching'->>'earnedRuns')::INTEGER AS earned_runs,
    (raw_json->'stats'->'pitching'->>'baseOnBalls')::INTEGER AS walks,
    (raw_json->'stats'->'pitching'->>'strikeOuts')::INTEGER AS strikeouts,
    (raw_json->'stats'->'pitching'->>'homeRuns')::INTEGER AS home_runs_allowed,
    (raw_json->'stats'->'pitching'->>'pitchesThrown')::INTEGER AS pitches_thrown,
    (raw_json->'stats'->'pitching'->>'battersFaced')::INTEGER AS batters_faced,
    (raw_json->'stats'->'pitching'->>'wildPitches')::INTEGER AS wild_pitches
FROM {{ source('bronze', 'player_game_stats') }}
WHERE (raw_json->'stats'->'pitching'->>'battersFaced')::INTEGER > 0
