import dash_bootstrap_components as dbc
from dash import html

from src.utils.utils import get_player_headshot_url


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
