"""Database helper for SQLite operations."""
import os
import sqlite3
from sqlite3 import Connection
from typing import List
from config import DATABASE_PATH


def get_connection() -> Connection:
    """Return a SQLite connection, ensuring the database directory exists."""
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_db() -> None:
    """Create the persistent tables if they do not exist."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            genre TEXT NOT NULL,
            language TEXT NOT NULL,
            rating REAL NOT NULL,
            year INTEGER NOT NULL,
            description TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            search_query TEXT NOT NULL,
            category TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            genre TEXT NOT NULL,
            saved_date TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def insert_movies_from_csv(csv_path: str) -> None:
    """Bulk load movie records from CSV into the movies table only if empty."""
    from services.preprocess import load_movies

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Dataset file not found: {csv_path}")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM movies")
    existing_count = cur.fetchone()[0]
    if existing_count > 0:
        conn.close()
        return

    df = load_movies(csv_path)
    rows = [
        (
            row['title'].strip(),
            row['genre'].strip(),
            row['language'].strip(),
            float(row['rating'] or 0.0),
            int(row['year'] or 0),
            row['description'].strip(),
        )
        for _, row in df.iterrows()
    ]

    cur.executemany(
        "INSERT INTO movies (title,genre,language,rating,year,description) VALUES (?,?,?,?,?,?)",
        rows,
    )
    conn.commit()
    conn.close()


def query_movies() -> List[sqlite3.Row]:
    """Fetch all movies from the database."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM movies")
    rows = cur.fetchall()
    conn.close()
    return rows
