from pprint import pprint

import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, callback, dcc, html

from src.dashboard.components.create_player_card import create_player_card
from src.dashboard.components.create_stats_display import create_stats_display
from src.data.roster_cache import get_roster_data

roster_data = get_roster_data()
pprint(roster_data)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

player_options = [
    {
        "label": f"{player['player_name']} - {player['position']}",
        "value": player["player_id"],
    }
    for player in roster_data
]


@callback(
    Output("player-card-section", "children"),
    Output("stats-section", "children"),
    Input("player-dropdown", "value")
)
def update_player_display(selected_player_id: int) -> tuple:
    # Find the player with matching ID
    selected_player = next(
        (player for player in roster_data if player["player_id"] == selected_player_id),
        None
    )

    # Handle case where player not found
    if not selected_player:
        return (
            html.P("Player not found"),
            html.P("No stats available")
        )

    # Create and return the player card and stats display
    return (
        create_player_card(selected_player),
        create_stats_display(selected_player)
    )

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
