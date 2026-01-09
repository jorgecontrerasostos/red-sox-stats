import dagster as dg
from dagster._core.definitions.partitions.subset import PartitionsSubset
import statsapi
import os
from src.utils.db_connection import get_connection_params
import psycopg2
import logging
from psycopg2.extras import Json


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

params = get_connection_params()

@dg.asset
def fetch_game_info() -> dict:
    target_date = "2025-04-18"

    game_info = statsapi.schedule(target_date, team=os.getenv("REDSOX_ID", "111"))
    logger.info(f"Found {len(game_info)} games for {target_date}")

    if not game_info:
        logger.error(f"No games found on {target_date}")
        return {"games_processed": 0, "target_date": target_date}

    query = """
    INSERT INTO bronze.games (game_id, raw_json)
    VALUES (%s, %s)
    ON CONFLICT (game_id) DO UPDATE SET
        raw_json = EXCLUDED.raw_json,
        ingested_at = NOW()
    """

    try:
        conn = psycopg2.connect(**params)
        cursor = conn.cursor()

        for game in game_info:
            game_id = game["game_id"]
            logger.info(f"Inserting game: {game_id}")

            cursor.execute(query, (game_id, Json(game)))

        conn.commit()
        logger.info(f"Successfully inserted: {len(game_info)} games")

        cursor.close()
        conn.close()

        return {
            "games_processed": len(game_info),
            "target_date": target_date
        }

    except psycopg2.OperationalError as e:
        logger.error(f"Connection Failed: {e}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error during database connection test: {e}")
        raise
@dg.asset(
    deps=["fetch_game_info"]
)
def fetch_game_boxscores():
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()

    cursor.execute("SELECT game_id from bronze.games")
    game_ids = cursor.fetchall()

    logger.info(f"Found {len(game_ids)} games to fetch box scores for")

    total_players = 0

    for (game_id,) in game_ids:
        logger.info(f"Fetching box score for game_id={game_id}")

        try:
            box_score_data = statsapi.get("game", {"gamePk": game_id})

            box_score = box_score_data.get("liveData", {}).get("boxscore", {})
            teams = box_score.get("teams", {})

            home_team_id = teams.get("home", {}).get("team", {}).get("id", {})
            away_team_id = teams.get("away", {}).get("team", {}).get("id", {})

            if home_team_id == os.getenv("REDSOX_ID", "111"):
                red_sox_players = teams.get("home", {}).get("players", {})

            elif away_team_id == int(os.getenv("REDSOX_ID", "111")):
                red_sox_players = teams.get("away", {}).get("players", {})

            else:
                logger.warning(f"Red Sox not found in game_id={game_id}, skipping")
                continue

            logger.info(f"Found {len(red_sox_players)} players for game_id={game_id}")

            for _, player_data in red_sox_players.items():
                player_id = player_data.get("person", {}).get("id", {})

                if not player_id:
                    logger.warning(f"No player_id for: {player_id}")
                    continue

                cursor.execute(
                    """
                    INSERT INTO bronze.player_game_stats (game_id, player_id, raw_json)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (game_id, player_id)
                    DO UPDATE SET
                        raw_json = EXCLUDED.raw_json,
                        ingested_at = NOW()
                    """,
                    (game_id, player_id, Json(player_data))
                )
                total_players += 1
            conn.commit()
        except Exception as e:
            logger.error(f"Error processing game: {game_id}. Error: {e}")
            continue
    cursor.close()
    conn.close()

    logger.info(f"Successfully processed {total_players} player records")

    return {
        "games_processed": len(game_ids),
        "players_processed": total_players
    }


