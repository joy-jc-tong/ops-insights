import logging
import os
import sqlite3

import pandas as pd


logger = logging.getLogger(__name__)


def _ensure_logger() -> None:
    if not logger.handlers:
        logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")


def write_mart(df: pd.DataFrame, output_path: str) -> None:
    _ensure_logger()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info("Wrote mart: %s (rows=%s)", output_path, len(df))


def write_marts(
    daily_kpi: pd.DataFrame,
    downtime_by_tooltype: pd.DataFrame,
    output_dir: str,
) -> None:
    _ensure_logger()
    write_mart(daily_kpi, os.path.join(output_dir, "mart_daily_kpi.csv"))
    write_mart(downtime_by_tooltype, os.path.join(output_dir, "mart_downtime_by_tooltype.csv"))


def load_to_sqlite(df: pd.DataFrame, db_path: str, schema_path: str) -> None:
    _ensure_logger()
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    with sqlite3.connect(db_path) as connection:
        with open(schema_path, "r", encoding="utf-8") as schema_file:
            connection.executescript(schema_file.read())

        connection.execute("DELETE FROM events;")
        df.to_sql("events", connection, if_exists="append", index=False)

    logger.info("Loaded SQLite: %s (rows=%s)", db_path, len(df))

