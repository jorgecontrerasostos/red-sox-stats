from imports import *
from utils import make_request
import pandas as pd


class RedSoxDataExplorer:

    BASE_URL = "https://statsapi.mlb.com/api/v1"

    def __init__(self):
        self.id = 111

    def get_team_info(self):
        url = f"{self.BASE_URL}/teams/{self.id}"

        team_data = []

        response = make_request(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        team_data.append(
            {
                "team_id": data["teams"][0]["id"],
                "name": data["teams"][0]["name"],
                "abbreviation": data["teams"][0]["abbreviation"],
                "team_code": data["teams"][0]["teamCode"],
                "location_name": data["teams"][0]["locationName"],
                "first_year_of_play": data["teams"][0]["firstYearOfPlay"],
                "division_id": data["teams"][0]["division"]["id"],
            }
        )
        return team_data

    def get_team_roster(self):
        url = f"{self.BASE_URL}/teams/{self.id}/roster"
        roster_data = []

        response = make_request(url)
        response.raise_for_status()
        data = response.json()
        for item in data["roster"]:
            # Get detailed player info to get jersey number
            player_info = self.get_player_info_by_id(item["person"]["id"])
            print(f"Player info for {item['person']['fullName']}:", player_info)  # Debug log
            
            roster_data.append(
                {
                    "player_id": item["person"]["id"],
                    "name": item["person"]["fullName"],
                    "position": item["position"]["name"],
                    "abbreviation": item["position"]["abbreviation"],
                    "jersey_number": player_info.get("jersey_number") if player_info else None
                }
            )

        return roster_data

    def get_player_id(self, roster_data: list, player_name: str):
        """
        Find a player's ID by searching through the roster data by name.

        Args:
            roster_data: List of player dictionaries from get_team_roster()
            player_name: Full name of the player to search for

        Returns:
            int: Player ID if found, None if not found
        """
        for player in roster_data:
            if player["name"].lower() == player_name.lower():
                return player["player_id"]

        # If exact match not found, try partial match
        for player in roster_data:
            if player_name.lower() in player["name"].lower():
                return player["player_id"]

        print(f"Player '{player_name}' not found in roster")
        return None

    def get_player_info_by_id(self, player_id: int):
        """
        Get detailed information about a player using their ID.

        Args:
            player_id: The MLB player ID

        Returns:
            dict: Player information including personal and professional details
        """
        url = f"{self.BASE_URL}/people/{player_id}"
        response = make_request(url)
        response.raise_for_status()
        data = response.json()

        if not data.get("people"):
            print(f"No player found with ID: {player_id}")
            return None

        player = data["people"][0]
        print(f"Raw player data for ID {player_id}:", player)  # Debug log
        
        player_info = {
            "id": player["id"],
            "full_name": player["fullName"],
            "birth_date": player.get("birthDate"),
            "birth_city": player.get("birthCity"),
            "age": player.get("currentAge"),
            "birth_country": player.get("birthCountry"),
            "height": player.get("height"),
            "weight": player.get("weight"),
            "position": player.get("primaryPosition", {}).get("name"),
            "position_code": player.get("primaryPosition", {}).get("code"),
            "bat_side": player.get("batSide", {}).get("code"),
            "throw_hand": player.get("pitchHand", {}).get("code"),
            "active": player.get("active", False),
            "jersey_number": player.get("primaryNumber"),
        }
        print(f"Processed player info for ID {player_id}:", player_info)  # Debug log
        return player_info

    def get_player_info_by_name(self, player_name: str):
        """
        Get detailed information about a player using their name.

        Args:
            player_name: The player's name (full or partial)

        Returns:
            dict: Player information including personal and professional details
            None: If player is not found
        """
        # First get the current roster
        roster = self.get_team_roster()

        # Find the player's ID from the roster
        player_id = self.get_player_id(roster, player_name)

        if player_id is None:
            return None

        # Get the detailed player information using the ID
        return self.get_player_info_by_id(player_id)

    def get_player_stats(self, player_id: int, season: int):
        """
        Get the stats for a player for a given season.

        Args:
            player_id: The MLB player ID
            season: The season to get stats for

        Returns:
            dict: Player stats including hitting and pitching stats
        """
        url = f"{self.BASE_URL}/people/{player_id}/stats?stats=season&season={season}"
        response = make_request(url)
        response.raise_for_status()
        data = response.json()

        # Check if stats are found
        if not data.get("stats"):
            print(f"No stats found for player {player_id} in {season}")
            return None

        # Initialize player stats dictionary
        player_stats = {
            "player_id": player_id,
            "season": season,
            "hitting": None,
            "pitching": None,
        }

        # Iterate through the stats
        for stat_group in data["stats"]:
            group_type = stat_group.get("group", {}).get("displayName", "")

            if not stat_group.get("splits"):
                continue

            stats = stat_group["splits"][0].get("stat", {})

            if "hitting" in group_type.lower():
                player_stats["hitting"] = {
                    "games_played": stats.get("gamesPlayed", 0),
                    "at_bats": stats.get("atBats", 0),
                    "runs": stats.get("runs", 0),
                    "hits": stats.get("hits", 0),
                    "doubles": stats.get("doubles", 0),
                    "triples": stats.get("triples", 0),
                    "home_runs": stats.get("homeRuns", 0),
                    "rbi": stats.get("rbi", 0),
                    "stolen_bases": stats.get("stolenBases", 0),
                    "walks": stats.get("baseOnBalls", 0),
                    "strikeouts": stats.get("strikeOuts", 0),
                    "batting_avg": stats.get("avg", ".000"),
                    "on_base_pct": stats.get("obp", ".000"),
                    "slugging_pct": stats.get("slg", ".000"),
                    "ops": stats.get("ops", ".000"),
                }

            elif "pitching" in group_type.lower():
                player_stats["pitching"] = {
                    "games_played": stats.get("gamesPlayed", 0),
                    "games_started": stats.get("gamesStarted", 0),
                    "wins": stats.get("wins", 0),
                    "losses": stats.get("losses", 0),
                    "saves": stats.get("saves", 0),
                    "innings_pitched": stats.get("inningsPitched", "0.0"),
                    "hits_allowed": stats.get("hits", 0),
                    "runs_allowed": stats.get("runs", 0),
                    "earned_runs": stats.get("earnedRuns", 0),
                    "home_runs_allowed": stats.get("homeRuns", 0),
                    "walks": stats.get("baseOnBalls", 0),
                    "strikeouts": stats.get("strikeOuts", 0),
                    "era": stats.get("era", "0.00"),
                    "whip": stats.get("whip", "0.00"),
                }

        return player_stats
    
    def get_roster_stats(self, season: int):
        """
        Get stats for all players in the current Red Sox roster for a given season.

        Args:
            season: The season to get stats for (e.g., 2024)

        Returns:
            list: List of dictionaries containing player info and stats for the season
        """
        # Get the current roster
        roster = self.get_team_roster()
        roster_stats = []

        # Get stats for each player
        for player in roster:
            # Get basic player info
            player_info = self.get_player_info_by_id(player["player_id"])
            
            # Get player stats
            player_stats = self.get_player_stats(player["player_id"], season)
            
            # Combine player info and stats
            player_data = {
                "player_id": player["player_id"],
                "name": player["name"],
                "position": player["position"],
                "position_abbrev": player["abbreviation"],
                "info": player_info,
                "stats": player_stats
            }
            
            roster_stats.append(player_data)
        
        return roster_stats

    def stats_to_dataframes(self, roster_stats: list):
        """
        Convert roster stats into two pandas DataFrames: one for hitters and one for pitchers.
        
        Args:
            roster_stats: List of player stats from get_roster_stats()
            
        Returns:
            tuple: (hitters_df, pitchers_df) containing the respective DataFrames
        """
        hitters_data = []
        pitchers_data = []
        
        for player in roster_stats:
            # Common player info
            base_info = {
                'player_id': player['player_id'],
                'name': player['name'],
                'position': player['position'],
                'age': player['info'].get('age'),
                'bat_side': player['info'].get('bat_side'),
                'throw_hand': player['info'].get('throw_hand'),
                'jersey_number': player['info'].get('jersey_number')
            }
            
            # Add hitting stats if available
            if player['stats'] and player['stats']['hitting']:
                hitting_stats = base_info.copy()
                hitting_stats.update(player['stats']['hitting'])
                hitters_data.append(hitting_stats)
            
            # Add pitching stats if available
            if player['stats'] and player['stats']['pitching']:
                pitching_stats = base_info.copy()
                pitching_stats.update(player['stats']['pitching'])
                pitchers_data.append(pitching_stats)
        
        # Create DataFrames
        hitters_df = pd.DataFrame(hitters_data) if hitters_data else pd.DataFrame()
        pitchers_df = pd.DataFrame(pitchers_data) if pitchers_data else pd.DataFrame()
        
        # Sort DataFrames
        if not hitters_df.empty:
            hitters_df = hitters_df.sort_values('batting_avg', ascending=False)
        if not pitchers_df.empty:
            pitchers_df = pitchers_df.sort_values('era')
            
        return hitters_df, pitchers_df


if __name__ == "__main__":
    explorer = RedSoxDataExplorer()
    # Get stats for all players in 2024
    print("Getting roster stats for 2025:")
    roster_stats = explorer.get_roster_stats(2025)
    
    # Convert to DataFrames
    hitters_df, pitchers_df = explorer.stats_to_dataframes(roster_stats)
    
    # Display hitting stats
    print("\nHitting Statistics:")
    if not hitters_df.empty:
        print(hitters_df[['name', 'position', 'at_bats', 'batting_avg', 'home_runs', 'rbi', 'ops']].sort_values(['at_bats', 'batting_avg'], ascending=False).to_string())
    else:
        print("No hitting statistics available")
    
    # Display pitching stats
    print("\nPitching Statistics:")
    if not pitchers_df.empty:
        print(pitchers_df[['name', 'position', 'era', 'wins', 'losses', 'strikeouts']].to_string())
    else:
        print("No pitching statistics available")
    

