SELECT
    game_id,
    (raw_json->>'game_date')::DATE AS game_date,
    raw_json->>'game_type' AS game_type,
    -- Checking if the current game is played at Fenway
    CASE
        WHEN (raw_json->>'home_id')::INTEGER = 111 THEN TRUE
        ELSE FALSE
    END AS is_home_game,
    -- Opponent name
    CASE 
        WHEN (raw_json->>'home_id')::INTEGER = 111 THEN raw_json->>'away_name'
        ELSE raw_json->>'home_name'
    END AS opponent,
    -- Red Sox score
    CASE 
        WHEN (raw_json->>'home_id')::INTEGER = 111 THEN (raw_json->>'home_score')::INTEGER
        ELSE (raw_json->>'away_score')::INTEGER
    END AS red_sox_score,
    -- Opponent score
    CASE 
        WHEN (raw_json->>'home_id')::INTEGER = 111 THEN (raw_json->>'away_score')::INTEGER
        ELSE (raw_json->>'home_score')::INTEGER
    END AS opponent_score,
    -- Game result
    CASE
        WHEN raw_json->>'winning_team' = 'Boston Red Sox' THEN 'W'
        ELSE 'L'
    END AS game_result,
    raw_json->>'venue_name' AS venue,
    raw_json ->>'winning_pitcher' AS winning_pitcher,
    raw_json ->>'losing_pitcher' AS losing_pitcher,
    raw_json->>'save_pitcher' AS save_pitcher,
    raw_json->>'doubleheader' AS double_header

FROM {{ source('bronze', 'games') }}