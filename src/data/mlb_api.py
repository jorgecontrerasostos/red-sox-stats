"""MLB Stats API wrapper for fetching Red Sox data."""

import logging
from typing import Dict, List

import statsapi

logger = logging.getLogger(__name__)

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

def get_player_stats(player_id: int, stat_type: str = "season") -> Dict:
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
    try:
        player_stats = statsapi.player_stat_data(player_id, type=stat_type)
        player_name = (
            f"{player_stats.get('first_name', '')} "
            f"{player_stats.get('last_name', '')}"
        )
        logger.info(
            f"Player stats fetched successfully: {player_name}"
        )
        return player_stats
    except Exception as e:
        logger.error(f"Error fetching player stats: {e}")
        return {}

def fetch_red_sox_roster_with_stats() -> List[Dict]:
    """
    Fetch Red Sox roster and basic stats for all players.

    This is the main function that combines roster and stats data.

    Returns:
        list: List of dictionaries containing player info and stats
    """
    logger.info("Fetching Red Sox roster...")

    roster = get_roster()

    if not roster:
        logger.error("Failed to get roster")
        return []

    players_with_stats = []

    for player in roster:
        player_id = player["person"]["id"]
        player_name = player["person"]["fullName"]

        stats = get_player_stats(player_id)
        if not stats:
            logger.error(f"Failed to get stats for {player_name}")
            continue

        combined_data = {
            "player_id": player_id,
            "player_name": player_name,
            "jersey_number": player.get("jerseyNumber", "--"),
            "position": player.get("position", {}).get("abbreviation", "--"),
            "status": player.get("status", {}).get("description", "Unknown"),
            "stats": stats
        }

        players_with_stats.append(combined_data)
    logger.info(f"Fetched complete data for {len(players_with_stats)} players")

    return players_with_stats
