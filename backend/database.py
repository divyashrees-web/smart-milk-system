
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "smart_milk.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS sensor_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tank_id TEXT NOT NULL,
                ambient_temperature_c REAL,
                humidity_percent REAL,
                milk_temperature_simulated_c REAL,
                tank_level_percent REAL,
                cooling_status TEXT,
                power_status TEXT,
                timestamp TEXT NOT NULL,
                data_mode TEXT NOT NULL
            )
        """)


def save_reading(reading):
    with get_connection() as connection:
        connection.execute("""
            INSERT INTO sensor_readings (
                tank_id,
                ambient_temperature_c,
                humidity_percent,
                milk_temperature_simulated_c,
                tank_level_percent,
                cooling_status,
                power_status,
                timestamp,
                data_mode
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            reading["tank_id"],
            reading["ambient_temperature_c"],
            reading["humidity_percent"],
            reading["milk_temperature_simulated_c"],
            reading["tank_level_percent"],
            reading["cooling_status"],
            reading["power_status"],
            reading["timestamp"],
            reading["data_mode"],
        ))


def get_readings(limit=50):
    with get_connection() as connection:
        rows = connection.execute("""
            SELECT * FROM sensor_readings
            ORDER BY id DESC
            LIMIT ?
        """, (limit,)).fetchall()

        return [dict(row) for row in rows]
