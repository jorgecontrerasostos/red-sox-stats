def slugify_name(first_name: str, last_name: str) -> str:
    """Slugify a name."""
    return f"{first_name.lower()}-{last_name.lower()}"


def get_player_headshot_url(player_id: int) -> str:
    """
    Get MLB headshot URL for a player.

    The URL includes a built-in fallback to a generic headshot silhouette
    if the player's image is not available.

    Args:
        player_id: MLB player ID

    Returns:
        URL string to player's headshot image

    Example:
        >>> get_player_headshot_url(680776)
        'https://img.mlbstatic.com/mlb-photos/..../680776/headshot/...'
    """
    return f"https://img.mlbstatic.com/mlb-photos/image/upload/d_people:generic:headshot:silo:current.png/r_max/w_180,q_auto:best/v1/people/{player_id}/headshot/silo/current"
