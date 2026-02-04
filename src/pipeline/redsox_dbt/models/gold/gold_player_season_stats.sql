WITH players AS (
    SELECT * FROM {{ ref('silver_players') }}
    WHERE is_current = true
),

batting_agg AS (
    SELECT
        player_id,
        COUNT(*) AS games_played,
        SUM(at_bats) AS total_at_bats,
        SUM(runs) AS total_runs,
        SUM(hits) AS total_hits,
        SUM(doubles) AS total_doubles,
        SUM(triples) AS total_triples,
        SUM(home_runs) AS total_home_runs,
        SUM(rbi) AS total_rbi,
        SUM(walks) AS total_walks,
        SUM(strikeouts) AS total_strikeouts,
        SUM(hit_by_pitch) AS total_hit_by_pitch,
        SUM(plate_appearances) AS total_plate_appearances,
        SUM(total_bases) AS total_bases
    FROM {{ ref('silver_batting_game_stats') }}
    GROUP BY player_id
),

pitching_agg AS (
    SELECT
        player_id,
        COUNT(*) AS games_pitched,
        SUM(innings_pitched) AS total_innings,
        SUM(strikeouts) AS total_strikeouts,
        SUM(walks) AS total_walks,
        SUM(earned_runs) AS total_earned_runs,
        SUM(hits_allowed) AS total_hits_allowed,
        SUM(home_runs_allowed) AS total_home_runs_allowed
    FROM {{ ref('silver_pitching_game_stats') }}
    GROUP BY player_id
)

SELECT
    p.player_id,
    p.player_name,
    p.primary_position,
    p.jersey_number,
    COALESCE(b.games_played, 0) AS games_played,
    COALESCE(b.total_at_bats, 0) AS total_at_bats,
    COALESCE(b.total_runs, 0) AS total_runs_scored,
    COALESCE(b.total_hits, 0) AS total_hits,
    COALESCE(b.total_doubles, 0) AS total_doubles,
    COALESCE(b.total_triples, 0) AS total_triples,
    COALESCE(b.total_home_runs, 0) AS total_home_runs,
    COALESCE(b.total_rbi, 0) AS total_rbi,
    COALESCE(b.total_walks, 0) AS total_walks,
    COALESCE(b.total_strikeouts, 0) AS total_strikeouts,
    COALESCE(b.total_hit_by_pitch, 0) AS total_hit_by_pitch,
    b.total_hits::DECIMAL / NULLIF(b.total_at_bats, 0) AS batting_avg,
    (b.total_hits + b.total_walks + b.total_hit_by_pitch)::DECIMAL / NULLIF(b.total_plate_appearances, 0) AS obp,
    b.total_bases::DECIMAL / NULLIF(b.total_at_bats, 0) AS slugging_pct,
    (b.total_hits + b.total_walks + b.total_hit_by_pitch)::DECIMAL / NULLIF(b.total_plate_appearances, 0) + b.total_bases::DECIMAL / NULLIF(b.total_at_bats, 0) AS ops,
    COALESCE(pt.games_pitched, 0) AS total_games_pitched,
    COALESCE(pt.total_innings, 0) AS total_innings,
    COALESCE(pt.total_strikeouts, 0) AS total_strikeouts_pitching,
    COALESCE(pt.total_walks, 0) AS total_walks_pitching,
    COALESCE(pt.total_earned_runs, 0) AS total_earned_runs,
    COALESCE(pt.total_hits_allowed, 0) AS total_hits_allowed,
    COALESCE(pt.total_home_runs_allowed, 0) AS total_home_runs_allowed,
    (pt.total_earned_runs::DECIMAL / NULLIF(pt.total_innings, 0)) * 9 AS era,
    (pt.total_walks + pt.total_hits_allowed)::DECIMAL / NULLIF(pt.total_innings, 0) AS whip
FROM players p
LEFT JOIN batting_agg b ON p.player_id = b.player_id
LEFT JOIN pitching_agg pt ON p.player_id = pt.player_id