"""
Exploration script to understand the MLB Stats API.

Run this to see what data is available before implementing the fetcher.
"""

import statsapi
import json
from pprint import pprint

# Red Sox team ID
RED_SOX_TEAM_ID = 111

print("=" * 80)
print("EXPLORING MLB STATS API")
print("=" * 80)

# 1. Get roster data (formatted string)
print("\n1. ROSTER AS FORMATTED STRING:")
print("-" * 80)
roster_string = statsapi.roster(RED_SOX_TEAM_ID)
print(roster_string)

# 2. Look for functions that return structured data
print("\n2. LOOKING FOR DATA FUNCTIONS:")
print("-" * 80)
print("Let's try functions that might return structured data...")

# Try the 'get' function with roster endpoint
print("\n3. USING THE LOW-LEVEL 'get' FUNCTION:")
print("-" * 80)
try:
    # The statsapi.get() function returns actual JSON data
    roster_data = statsapi.get('team_roster', {'teamId': RED_SOX_TEAM_ID})
    print(f"Type: {type(roster_data)}")
    print(json.dumps(roster_data["roster"], indent=2))
    print(f"\nKeys available: {roster_data.keys() if isinstance(roster_data, dict) else 'Not a dict'}")

    if 'roster' in roster_data:
        print(f"\nNumber of players: {len(roster_data['roster'])}")
        print("\nFirst player structure:")
        print(json.dumps(roster_data['roster'][0], indent=2))
except Exception as e:
    print(f"Error: {e}")

# 4. Check player stats structure
print("\n4. EXPLORING PLAYER STATS:")
print("-" * 80)
# Let's see what functions exist for player data
player_funcs = [f for f in dir(statsapi) if 'player' in f.lower()]
print(f"Player-related functions: {player_funcs}")

print("\n" + "=" * 80)
print("This shows us the actual data structure we can work with!")
print("=" * 80)
