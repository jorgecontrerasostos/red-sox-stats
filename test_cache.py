"""Test script for roster caching system."""

import logging
from src.data.roster_cache import get_roster_data

# Set up logging so we can see what's happening
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(name)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    logger.info("=" * 80)
    logger.info("Testing Roster Cache System")
    logger.info("=" * 80)

    # First call - should fetch from API and cache it
    logger.info("\n--- First call (should fetch from API) ---")
    players = get_roster_data()
    logger.info(f"Got {len(players)} players")

    if players:
        # Show a sample player
        sample = players[0]
        logger.info(f"\nSample player: {sample['player_name']}")
        logger.info(f"  Position: {sample['position']}")
        logger.info(f"  Number: {sample['jersey_number']}")

    # Second call - should load from cache (fast!)
    logger.info("\n--- Second call (should load from cache) ---")
    players2 = get_roster_data()
    logger.info(f"Got {len(players2)} players")

    logger.info("\n✅ Cache test complete!")

if __name__ == "__main__":
    main()
