from scrapling import Fetcher
import logging
from src.utils.utils import slugify_name
from pprint import pprint

logging.basicConfig(level=logging.INFO)

BASE_URL = "https://baseballsavant.mlb.com/savant-player/"

def get_savant_url(player_id: int, first_name: str, last_name: str) -> str:
    """Get the Savant URL for a player."""
    return f"{BASE_URL}{slugify_name(first_name, last_name)}-{player_id}"

def fetch_savant_page():
    fetcher = Fetcher()
    try:
        page = fetcher.get(get_savant_url(547973, "Aroldis", "Chapman"))
    except Exception as e:
        logging.error(f"Error: {e}")

    return page

if __name__ == "__main__":
    page = fetch_savant_page()
    pprint(page)