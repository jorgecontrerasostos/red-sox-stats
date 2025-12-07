import logging

from data.mlb_api import get_roster

logging.basicConfig(level=logging.INFO)

def main() -> None:
    """Main function."""
    logger = logging.getLogger(__name__)
    logger.info("Fetching Red Sox roster...")

    roster = get_roster()

    if roster:
        logger.info(f"\n{'='*80}")
        logger.info(f"RED SOX ROSTER - {len(roster)} Players")
        logger.info(f"{'='*80}\n")

        for player in roster:
            name = player.get("person", {}).get("fullName", "Unknown")
            jersey_number = player.get("jerseyNumber", "--")
            position = player.get("position", {}).get("abbreviation", "--")
            status = player.get("status", {}).get("description", "Unknown")

            logger.info(f"#{jersey_number:<3} {position:<4} {name:<30} ({status})")
    else:
        logger.error("Failed to fetch roster")


if __name__ == "__main__":
    main()
