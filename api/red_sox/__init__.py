from imports import *
from utils import make_request


class RedSoxDataExplorer:

    BASE_URL = "https://statsapi.mlb.com/api/v1"

    def __init__(self):
        self.id = 111

    def get_team_info(self):
        url = f"{self.BASE_URL}/teams/{self.id}"

        team_data = []

        response = make_request(url)
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
            roster_data.append(
                {
                    "player_id": item["person"]["id"],
                    "name": item["person"]["fullName"],
                    "position": item["position"]["name"],
                    "abbreviation": item["position"]["abbreviation"],
                }
            )
        return roster_data 