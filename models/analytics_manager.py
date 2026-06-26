"""Analytics computations for dashboard metrics."""
from typing import Dict, Any, List
from datetime import datetime
from utils.database import get_connection


class AnalyticsManager:
    """Compute analytics and charts from persistent storage."""

    @staticmethod
    def totals() -> Dict[str, int]:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM history")
        total_searches = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM movies")
        total_movies = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM favorites")
        total_favorites = cur.fetchone()[0]
        conn.close()
        return {
            'total_searches': total_searches,
            'total_recommendations': total_movies,
            'total_favorites': total_favorites,
        }

    @staticmethod
    def most_favorite_genre() -> str:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT genre, COUNT(*) as count FROM favorites GROUP BY genre ORDER BY count DESC LIMIT 1")
        row = cur.fetchone()
        conn.close()
        return row[0] if row else 'No favorites yet'

    @staticmethod
    def most_viewed_movie() -> str:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT title, COUNT(*) as count FROM favorites GROUP BY title ORDER BY count DESC LIMIT 1")
        row = cur.fetchone()
        conn.close()
        return row[0] if row else 'No favorites yet'

    @staticmethod
    def searches_per_day() -> Dict[str, int]:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT substr(timestamp, 1, 10) AS day, COUNT(*) FROM history GROUP BY day ORDER BY day ASC")
        rows = cur.fetchall()
        conn.close()
        return {row[0]: row[1] for row in rows}

    @staticmethod
    def favorite_genres() -> Dict[str, int]:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT genre, COUNT(*) FROM favorites GROUP BY genre ORDER BY COUNT(*) DESC")
        rows = cur.fetchall()
        conn.close()
        return {row[0]: row[1] for row in rows}

    @staticmethod
    def user_activity() -> Dict[str, int]:
        totals = AnalyticsManager.totals()
        return {
            'searches': totals['total_searches'],
            'favorites': totals['total_favorites'],
            'movie_catalog': totals['total_recommendations'],
        }
