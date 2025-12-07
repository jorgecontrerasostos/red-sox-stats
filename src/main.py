import logging

from data.mlb_api import fetch_red_sox_roster_with_stats

logging.basicConfig(level=logging.INFO)


def main() -> None:
    """Main function."""
    logger = logging.getLogger(__name__)

    # Use the combined function that gets roster + stats
    players = fetch_red_sox_roster_with_stats()

    if not players:
        logger.error("Failed to fetch roster data")
        return

    # Display header
    logger.info(f"\n{'='*80}")
    logger.info(f"RED SOX ROSTER WITH STATS - {len(players)} Players")
    logger.info(f"{'='*80}\n")

    # Display each player with their stats
    for player in players:
        name = player["player_name"]
        number = player["jersey_number"]
        position = player["position"]
        stats_data = player["stats"]

        # Display basic player info
        logger.info(f"#{number:<3} {position:<4} {name}")

        # Extract and display relevant stats based on position
        player_stats = stats_data.get("stats", [])
        if not player_stats:
            logger.info(
                "    No data available. Player has not played in MLB this season."
            )
            continue
        for stat_group in player_stats:
            group_type = stat_group.get("group")
            stats = stat_group.get("stats", {})

            if position != "P" and group_type == "hitting":
                # Show batting stats
                avg = stats.get("avg", "N/A")
                hr = stats.get("homeRuns", "N/A")
                rbi = stats.get("rbi", "N/A")
                logger.info(f"    Hitting: AVG {avg} | HR {hr} | RBI {rbi}")

            elif position == "P" and group_type == "pitching":
                # Show pitching stats
                era = stats.get("era", "N/A")
                wins = stats.get("wins", "N/A")
                strikeouts = stats.get("strikeOuts", "N/A")
                logger.info(f"    Pitching: ERA {era} | W {wins} | K {strikeouts}")

        logger.info("")  # Empty line between players


if __name__ == "__main__":
    main()
