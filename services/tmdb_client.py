"""Simple TMDB client to resolve poster URLs by movie title."""
from pathlib import Path
from typing import Optional
import re
import requests
from config import BASE_DIR, TMDB_API_KEY, TMDB_IMAGE_BASE_URL

STATIC_POSTER_DIR = Path(BASE_DIR) / 'static' / 'images' / 'posters'
STATIC_POSTER_DIR.mkdir(parents=True, exist_ok=True)


def _slugify(value: str) -> str:
    value = str(value or '').strip().lower()
    value = re.sub(r'[^a-z0-9]+', '-', value)
    value = value.strip('-')
    return value or 'movie'


def _download_image(url: str, dest_path: Path) -> bool:
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200 and resp.content:
            dest_path.write_bytes(resp.content)
            return True
    except Exception:
        pass
    return False


def get_poster_url(title: str, year: Optional[int] = None) -> str:
    """Return a local cached poster path or default placeholder."""
    DEFAULT = '/static/images/logo.png'
    title = str(title or '').strip()
    if not title:
        return DEFAULT

    cache_name_parts = [_slugify(title)]
    if year:
        cache_name_parts.append(str(year))
    cache_base = '-'.join(cache_name_parts)
    cache_file = f"{cache_base}.jpg"
    local_path = STATIC_POSTER_DIR / cache_file
    static_url = f'/static/images/posters/{cache_file}'

    if local_path.exists():
        return static_url

    if not TMDB_API_KEY:
        return DEFAULT

    try:
        params = {'api_key': TMDB_API_KEY, 'query': title}
        if year:
            params['year'] = int(year)
        resp = requests.get('https://api.themoviedb.org/3/search/movie', params=params, timeout=6)
        if resp.status_code != 200:
            return DEFAULT

        data = resp.json()
        results = data.get('results') or []
        if not results:
            return DEFAULT

        poster_path = results[0].get('poster_path')
        if not poster_path:
            return DEFAULT

        image_url = TMDB_IMAGE_BASE_URL.rstrip('/') + '/' + poster_path.lstrip('/')
        if _download_image(image_url, local_path):
            return static_url
    except Exception:
        pass

    return DEFAULT
