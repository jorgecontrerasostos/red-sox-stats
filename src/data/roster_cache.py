import json
import logging
import pathlib
from datetime import datetime, timedelta, timezone
from typing import Dict, List

logger = logging.getLogger(__name__)

def save_roster_cache(roster_data: List[Dict]) -> None:
    cache = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data": roster_data,
    }

    cache_dir = pathlib.Path("data/cache")
    cache_file = cache_dir / "roster_cache.json"
    cache_dir.mkdir(parents=True, exist_ok=True)

    with open(cache_file, "w") as f:
        json.dump(cache, f, indent=4)

    logger.info(f"Roster cache saved to {cache_file}")

def load_roster_cache() -> List[Dict]:
    cache_dir = pathlib.Path("data/cache")
    cache_file = cache_dir / "roster_cache.json"

    if not cache_file.exists():
        logger.warning("Roster cache file not found. Returning empty list.")
        return []

    try:
        with open(cache_file) as f:
            cache = json.load(f)
    except Exception as e:
        logger.error(f"Error loading roster cache: {e}")
        return []

    timestamp_str = cache.get("timestamp")
    if not timestamp_str:
        logger.error("Timestamp not found in cache. Returning empty list.")
        return []

    timestamp = datetime.fromisoformat(timestamp_str)

    age = datetime.now(timezone.utc) - timestamp
    cache_duration = timedelta(hours=24)

    if age > cache_duration:
        logger.info(f"Cache is stale (age: {age})")
        return []

    logger.info(f"Loaded {len(cache['data'])} players from cache (age: {age})")
    return cache["data"]
