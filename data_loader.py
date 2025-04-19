from constants import *
from utils import *
from imports import *
from pandas import DataFrame


def get_data() -> tuple[DataFrame, DataFrame]:
    batting_data = make_request(url=BATTING_URL, headers=BATTING_HEADERS)
    pitching_data = make_request(url=PITCHING_URL, headers=PITCHING_HEADERS)

    batters = []
    pitchers = []

    for batter in batting_data.json()["stats"]:
        batters.append(
            {
                "name": batter["playerFullName"],
                "postion": batter["position"],
                "pos_abb": batter["primaryPositionAbbrev"],
                "avg": batter["avg"],
                "at_bats": batter["atBats"],
                "obp": batter["obp"],
                "slg": batter["slg"],
                "ops": batter["ops"],
                "hits": batter["hits"],
                "rbi": batter["rbi"],
            }
        )

    for pitcher in pitching_data.json()["stats"]:
        pitchers.append(
            {
                "name": pitcher["playerFullName"],
                "position": pitcher["position"],
                "wins": pitcher["wins"],
                "losses": pitcher["losses"],
                "era": pitcher["era"],
                "whip": pitcher["whip"],
                "k_per_9": pitcher["strikeoutsPer9"],
                "avg": pitcher["avg"],
            }
        )

    batter_df = pd.DataFrame(batters)
    pitcher_df = pd.DataFrame(pitchers)

    for column in FLOAT_STATS:
        if column in batter_df.columns:
            batter_df[column] = batter_df[column].astype(float)
        if column in pitcher_df.columns:
            pitcher_df[column] = pitcher_df[column].astype(float)

    return batter_df, pitcher_df
