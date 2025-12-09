import logging
from typing import List, Dict
import json
import pathlib
from datetime import datetime

logger = logging.getLogger(__name__)

def save_roster_cache(roster_data: List[Dict]) -> None:
    cache = {
        "timestamp": datetime.now().isoformat(),
        "data": roster_data,
    }

    CACHE_DIR = pathlib.Path("data/cache")
    CACHE_FILE = CACHE_DIR / "roster_cache.json"
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=4)

    logging.info(f"Roster cache saved to {CACHE_FILE}")

