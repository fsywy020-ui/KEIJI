"""SQLite connection helpers."""

from __future__ import annotations

import sqlite3
from pathlib import Path


SCHEMA_PATH = Path(__file__).with_name("schema.sql")


def connect(path: str | Path = ":memory:") -> sqlite3.Connection:
    """Create a SQLite connection with row dictionaries and FK enforcement."""

    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_schema(connection: sqlite3.Connection) -> None:
    """Apply the KEIJI schema to a SQLite connection."""

    connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    connection.commit()
