import json
import logging
from datetime import timedelta

from fastapi import APIRouter, Depends

from zephyr.app.api import deps
from zephyr.app.core.redis import cache
from zephyr.app.core.spotify import query_tracks

router = APIRouter()

log = logging.getLogger("uvicorn")


@router.post("/tracks")
def search_tracks(
    *,
    _=Depends(deps.get_current_user),
    q: str,
):
    """
    Search tracks using Spotify API
    """
    cache_key = f"search:track:q:{q}"
    if results := cache.get(cache_key):
        log.info("Search results from cache...")
        return json.loads(results)

    results = query_tracks(q)
    cache.setex(
        cache_key,
        timedelta(minutes=1),
        json.dumps(results),
    )
    return results
