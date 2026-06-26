"""Manage search history records."""
from typing import List, Dict, Any
from utils.database import get_connection
from utils.helper import now_iso


class HistoryManager:
    """Simple history manager for saving and querying searches."""

    @staticmethod
    def add(search_query: str, category: str):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO history (search_query, category, timestamp) VALUES (?,?,?)",
            (search_query, category, now_iso())
        )
        conn.commit()
        conn.close()

    @staticmethod
    def list_all() -> List[Dict[str, Any]]:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM history ORDER BY id DESC")
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def clear():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM history")
        conn.commit()
        conn.close()

    @staticmethod
    def delete(record_id: int):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM history WHERE id=?", (record_id,))
        conn.commit()
        conn.close()
