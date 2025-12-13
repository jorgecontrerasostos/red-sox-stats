from typing import Dict
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc

# from view_single_player import roster

from src.data.roster_cache import get_roster_data
from src.utils.utils import get_player_headshot_url


roster_data = get_roster_data()

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

player_options = [
    {
        "label": f"{player['player_name']} - {player['position']}",
        "value": player["player_id"],
    }
    for player in roster_data
]


def create_player_card(player_data):
    """Create a player info card with headshot."""
    player_id = player_data["player_id"]
    name = player_data["player_name"]
    number = player_data["jersey_number"]
    position = player_data["position"]

    headshot_url = get_player_headshot_url(player_id)

    return dbc.Card(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Img(
                                src=headshot_url,
                                style={
                                    "width": "100%",
                                    "maxWidth": "180px",
                                    "borderRadius": "10px",
                                },
                            )
                        ],
                        width=4,
                    ),
                    dbc.Col(
                        [
                            html.H3(f"{name}", className="mb-2"),
                            html.H5(
                                f"#{number} | {position}", className="text-muted mb-3"
                            ),
                        ],
                        width=8,
                    ),
                ],
                align="center",
            )
        ],
        body=True,
        className="shadow-sm",
    )


def create_stats_display(player_data):
    """Create stats cards for a player."""
    stats_data = player_data.get("stats", {})
    player_stats = stats_data.get("stats", [])
    position = player_data["position"]

    if not player_stats:
        return html.P("No stats available for this player.", className="text-muted")

    # Find hitting or pitching stats
    for stat_group in player_stats:
        if position == "P" and stat_group.get("group") == "pitching":
            stats = stat_group.get("stats", {})
            return dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    html.H6("ERA", className="text-muted mb-1"),
                                    html.H4(stats.get("era", "N/A")),
                                ],
                                body=True,
                                className="text-center",
                            )
                        ],
                        width=3,
                    ),
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    html.H6("Wins", className="text-muted mb-1"),
                                    html.H4(stats.get("wins", "N/A")),
                                ],
                                body=True,
                                className="text-center",
                            )
                        ],
                        width=3,
                    ),
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    html.H6("Strikeouts", className="text-muted mb-1"),
                                    html.H4(stats.get("strikeOuts", "N/A")),
                                ],
                                body=True,
                                className="text-center",
                            )
                        ],
                        width=3,
                    ),
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    html.H6("WHIP", className="text-muted mb-1"),
                                    html.H4(stats.get("whip", "N/A")),
                                ],
                                body=True,
                                className="text-center",
                            )
                        ],
                        width=3,
                    ),
                ]
            )
        elif stat_group.get("group") == "hitting":
            stats = stat_group.get("stats", {})
            return dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    html.H6("AVG", className="text-muted mb-1"),
                                    html.H4(stats.get("avg", "N/A")),
                                ],
                                body=True,
                                className="text-center",
                            )
                        ],
                        width=3,
                    ),
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    html.H6("HR", className="text-muted mb-1"),
                                    html.H4(stats.get("homeRuns", "N/A")),
                                ],
                                body=True,
                                className="text-center",
                            )
                        ],
                        width=3,
                    ),
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    html.H6("RBI", className="text-muted mb-1"),
                                    html.H4(stats.get("rbi", "N/A")),
                                ],
                                body=True,
                                className="text-center",
                            )
                        ],
                        width=3,
                    ),
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    html.H6("OPS", className="text-muted mb-1"),
                                    html.H4(stats.get("ops", "N/A")),
                                ],
                                body=True,
                                className="text-center",
                            )
                        ],
                        width=3,
                    ),
                ]
            )

    return html.P("No stats available.", className="text-muted")


app.layout = dbc.Container(
    [
        # Headings
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1(
                            "Red Sox Stats Dashboard",
                            className="text-center my-4",
                            style={"color": "#0C2340"},
                        ),
                        html.H4("2025 Season", className="text-center text-muted mb-4"),
                        html.Hr(),
                    ]
                )
            ]
        ),
        # Player Dropdown
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Select Player:", className="fw-bold mb-2"),
                        dcc.Dropdown(
                            id="player-dropdown",
                            options=player_options,
                            value=(
                                player_options[0]["value"] if player_options else None
                            ),
                            placeholder="Choose a Player",
                            className="mb-4",
                        ),
                    ],
                    width=6,
                ),
            ],
            className="mb-4",
        ),
        # Player Card Row
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            create_player_card(
                                roster_data[0]
                                if roster_data
                                else "No Players Available"
                            ),
                            id="player-card-section",
                        )
                    ]
                )
            ],
            className="mb-4",
        ),
        # Player Stats
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            (
                                create_stats_display(roster_data[0])
                                if roster_data
                                else "No stats available"
                            ),
                            id="stats-section",
                        )
                    ]
                )
            ]
        ),
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
