from typing import Dict, List

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from zephyr.app.core.config import settings

spotify = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET,
    )
)


def query_tracks(query: str, page: int, limit: int = 10) -> List:
    results: dict = spotify.search(q=query, offset=page * limit, limit=limit)
    tracks: dict = results["tracks"]

    parsed_results = list()
    for track in tracks["items"]:
        artists = list()
        for artist in track["artists"]:
            artists.append(artist["name"])

        parsed_results.append(
            {
                "uri": track["uri"],
                "name": track["name"],
                "album_image": track["album"]["images"][0]["url"],
                "artists": ", ".join(artists),
                "preview_url": track["preview_url"],
            }
        )
    return parsed_results


def search_track_by_uri(track_uri: str) -> Dict[str, str]:
    track = spotify.track(track_uri)
    artists = list()
    for artist in track["artists"]:
        artists.append(artist["name"])
    return {
        "uri": track["uri"],
        "name": track["name"],
        "album_image": track["album"]["images"][0]["url"],
        "artists": ", ".join(artists),
        "preview_url": track["preview_url"],
    }
