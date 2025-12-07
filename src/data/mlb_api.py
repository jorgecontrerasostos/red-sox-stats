"""MLB Stats API wrapper for fetching Red Sox data."""

import logging
import statsapi
from typing import Dict, List
import json

logger = logging.getLogger(__name__)

# Red Sox team ID (constant)
RED_SOX_TEAM_ID = 111


def get_roster() -> List[Dict[str, str]]:
    """
    Fetch the current Red Sox roster.

    Returns:
        dict: Roster data from MLB Stats API

    Raises:
        Exception: If API call fails
    """
    try:
        roster_data = statsapi.get("team_roster", {"teamId": RED_SOX_TEAM_ID})
        if "roster" in roster_data:
            roster = roster_data["roster"]
            logger.info(f"Roster fetched successfully: {len(roster)} players")
            return roster
        else:
            logger.error(f"No roster found in response: {roster_data}")
            return []
    except Exception as e:
        logger.error(f"Error fetching roster: {e}")
        return []

def get_player_stats(player_id: int, stat_type: str = "season"):
    """
    Fetch stats for a specific player.

    Args:
        player_id: MLB player ID
        stat_type: Type of stats to fetch (season, career, etc.)

    Returns:
        dict: Player stats data

    Raises:
        Exception: If API call fails
    """
    # TODO: Implement player stats fetching
    # Hint: Use statsapi.player_stats(player_id, type=stat_type)
    pass


def fetch_red_sox_roster_with_stats():
    """
    Fetch Red Sox roster and basic stats for all players.

    This is the main function that combines roster and stats data.

    Returns:
        list: List of dictionaries containing player info and stats
    """
    logger.info("Fetching Red Sox roster...")

    # TODO: Step 1 - Get the roster
    # TODO: Step 2 - Parse the roster data
    # TODO: Step 3 - For each player, get their stats
    # TODO: Step 4 - Combine roster + stats data
    # TODO: Step 5 - Return the combined data

    pass
