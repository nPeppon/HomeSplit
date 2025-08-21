"""Database helper for HomeSplit.
Creates table `expenses` if it does not exist and offers simple CRUD helpers.
"""
from __future__ import annotations

import os
from contextlib import contextmanager
from datetime import date, datetime
from typing import Any, Dict, List

import psycopg

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://homesplit:homesplit@localhost:5434/homesplit"
)


def _get_conn():
    return psycopg.connect(DATABASE_URL, autocommit=True)


@contextmanager
def get_cursor():
    conn = _get_conn()
    try:
        with conn.cursor() as cur:
            yield cur
    finally:
        conn.close()



def get_all_expenses() -> List[Dict[str, Any]]:
    with get_cursor() as cur:
        cur.execute("SELECT date, category, paid_by, reimbursed_by, amount, description FROM expenses ORDER BY date DESC, id DESC")
        rows = cur.fetchall()
    cols = ["date", "category", "paid_by", "reimbursed_by", "amount", "description"]
    result: List[Dict[str, Any]] = []
    for row in rows:
        entry = {k: (v.isoformat() if isinstance(v, date) else v) for k, v in zip(cols, row)}
        result.append(entry)
    return result


def add_expense(entry: Dict[str, Any]) -> None:
    with get_cursor() as cur:
        cur.execute(
            """
            INSERT INTO expenses (date, category, paid_by, reimbursed_by, amount, description)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                entry["date"],
                entry["category"],
                entry["paid_by"],
                entry["reimbursed_by"],
                entry["amount"],
                entry.get("description", ""),
            ),
        )


# ---------------- People helpers ---------------- #


def get_people() -> List[str]:
    """Return list of all people names."""
    with get_cursor() as cur:
        cur.execute("SELECT name FROM people ORDER BY name")
        rows = cur.fetchall()
    return [r[0] for r in rows]


def add_person(name: str) -> None:
    """Insert a person if not already existing (case-insensitive)."""
    if not name:
        return
    with get_cursor() as cur:
        cur.execute("""
            INSERT INTO people (name)
            VALUES (LOWER(%s)) ON CONFLICT (name) DO NOTHING
        """, (name.lower(),))