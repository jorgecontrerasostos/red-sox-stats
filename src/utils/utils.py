def slugify_name(first_name: str, last_name: str) -> str:
    """Slugify a name."""
    return f"{first_name.lower()}-{last_name.lower()}"
