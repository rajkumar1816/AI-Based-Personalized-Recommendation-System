"""Preprocessing utilities for datasets."""
import json
import os
import pandas as pd


def _normalize_genres(value: object) -> str:
    if pd.isna(value):
        return ''
    if isinstance(value, str) and value.strip():
        try:
            parsed = json.loads(value)
            if isinstance(parsed, list):
                names = []
                for item in parsed:
                    if isinstance(item, dict) and 'name' in item:
                        names.append(str(item['name']))
                    elif isinstance(item, str):
                        names.append(item)
                return ' '.join(names)
        except json.JSONDecodeError:
            return value.strip()
    return str(value).strip()


def _parse_year(value: object) -> int:
    if pd.isna(value):
        return 0
    try:
        if isinstance(value, str) and value.strip():
            dt = pd.to_datetime(value, errors='coerce')
            if not pd.isna(dt):
                return int(dt.year)
        return int(value)
    except (ValueError, TypeError):
        return 0


def load_movies(csv_path: str) -> pd.DataFrame:
    """Load movies CSV into a cleaned DataFrame with normalized columns."""
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Dataset file not found: {csv_path}")

    df = pd.read_csv(csv_path)
    lower_columns = {col.lower(): col for col in df.columns}

    title_col = lower_columns.get('title') or lower_columns.get('original_title')
    genre_col = lower_columns.get('genre') or lower_columns.get('genres')
    language_col = lower_columns.get('language') or lower_columns.get('original_language')
    description_col = lower_columns.get('description') or lower_columns.get('overview')
    rating_col = lower_columns.get('rating') or lower_columns.get('vote_average')
    year_col = lower_columns.get('year') or lower_columns.get('release_date')

    if title_col:
        df['title'] = df[title_col].fillna('').astype(str)
    else:
        df['title'] = ''

    if genre_col:
        if lower_columns.get('genres') == genre_col:
            df['genre'] = df[genre_col].apply(_normalize_genres)
        else:
            df['genre'] = df[genre_col].fillna('').astype(str)
    else:
        df['genre'] = ''

    if language_col:
        df['language'] = df[language_col].fillna('').astype(str)
    else:
        df['language'] = ''

    if description_col:
        df['description'] = df[description_col].fillna('').astype(str)
    else:
        df['description'] = ''

    if rating_col:
        df['rating'] = pd.to_numeric(df[rating_col], errors='coerce').fillna(0.0).astype(float)
    else:
        df['rating'] = 0.0

    if year_col:
        if year_col == lower_columns.get('release_date'):
            df['year'] = pd.to_datetime(df[year_col], errors='coerce').dt.year.fillna(0).astype(int)
        else:
            df['year'] = pd.to_numeric(df[year_col], errors='coerce').fillna(0).astype(int)
    else:
        df['year'] = 0

    if 'id' not in df.columns:
        df.insert(0, 'id', range(1, len(df) + 1))
    else:
        df['id'] = pd.to_numeric(df['id'], errors='coerce')
        if df['id'].isna().any():
            df['id'] = range(1, len(df) + 1)
        else:
            df['id'] = df['id'].astype(int)

    return df[['id', 'title', 'genre', 'language', 'rating', 'year', 'description']]
