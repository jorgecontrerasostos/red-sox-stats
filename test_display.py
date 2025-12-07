"""Test the display with just 3 players."""

import logging
from src.data.mlb_api import get_roster, get_player_stats

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get roster
roster = get_roster()

# Build data for first 3 players only
players = []
for player in roster[:3]:
    player_id = player["person"]["id"]
    stats = get_player_stats(player_id)

    combined = {
        "player_name": player["person"]["fullName"],
        "jersey_number": player.get("jerseyNumber", "--"),
        "position": player.get("position", {}).get("abbreviation", "--"),
        "stats": stats
    }
    players.append(combined)

# Display using the same logic as main.py
logger.info(f"\n{'='*80}")
logger.info(f"RED SOX ROSTER WITH STATS - {len(players)} Players (TEST)")
logger.info(f"{'='*80}\n")

for player in players:
    name = player["player_name"]
    number = player["jersey_number"]
    position = player["position"]
    stats_data = player["stats"]

    # Display basic player info
    logger.info(f"#{number:<3} {position:<4} {name}")

    # Extract and display relevant stats
    player_stats = stats_data.get("stats", [])

    for stat_group in player_stats:
        group_type = stat_group.get("group")
        stats = stat_group.get("stats", {})

        if group_type == "hitting":
            avg = stats.get("avg", "N/A")
            hr = stats.get("homeRuns", "N/A")
            rbi = stats.get("rbi", "N/A")
            logger.info(f"    Hitting: AVG {avg} | HR {hr} | RBI {rbi}")

        elif group_type == "pitching":
            era = stats.get("era", "N/A")
            wins = stats.get("wins", "N/A")
            strikeouts = stats.get("strikeOuts", "N/A")
            logger.info(f"    Pitching: ERA {era} | W {wins} | K {strikeouts}")

    logger.info("")
