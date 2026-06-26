"""Manage favorites storage."""
from typing import List, Dict, Any
from utils.database import get_connection
from utils.helper import now_iso


class FavoritesManager:
    """Simple favorites CRUD operations."""

    @staticmethod
    def add(title: str, genre: str):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO favorites (title, genre, saved_date) VALUES (?,?,?)",
            (title, genre, now_iso())
        )
        conn.commit()
        conn.close()

    @staticmethod
    def list_all() -> List[Dict[str, Any]]:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM favorites ORDER BY id DESC")
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def delete(record_id: int):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM favorites WHERE id=?", (record_id,))
        conn.commit()
        conn.close()
