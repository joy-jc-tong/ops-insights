import logging

import pandas as pd


logger = logging.getLogger(__name__)


def extract_events(csv_path: str) -> pd.DataFrame:
    if not logger.handlers:
        logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")

    df = pd.read_csv(csv_path)
    df["event_time"] = pd.to_datetime(df["event_time"], errors="coerce", utc=True)
    logger.info("Rows read: %s", len(df))
    logger.info("Columns: %s", list(df.columns))
    return df

