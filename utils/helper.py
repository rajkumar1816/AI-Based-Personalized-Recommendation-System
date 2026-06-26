"""Utility helpers used across the application."""
import csv
import os
from datetime import datetime
from typing import Any, Dict, List


def now_iso() -> str:
    """Return the current UTC timestamp in ISO format."""
    return datetime.utcnow().isoformat()


def export_history_to_csv(history_rows: List[Dict[str, Any]], output_path: str) -> None:
    """Write history rows to a CSV file for export."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'search_query', 'category', 'timestamp'])
        for row in history_rows:
            writer.writerow([row['id'], row['search_query'], row['category'], row['timestamp']])


def build_error_message(message: str) -> Dict[str, str]:
    """Return a structured error payload for API responses."""
    return {'error': message}


def safe_text(value: Any) -> str:
    """Return a normalized string for display."""
    if value is None:
        return ''
    return str(value)
