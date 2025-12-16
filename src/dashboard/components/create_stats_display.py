import dash_bootstrap_components as dbc
from dash import Dash, html, dcc

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