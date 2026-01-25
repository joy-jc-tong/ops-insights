import logging

import pandas as pd


logger = logging.getLogger(__name__)


def _ensure_logger() -> None:
    if not logger.handlers:
        logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")


def _check_non_negative(df: pd.DataFrame, columns: list[str], label: str) -> None:
    negatives = {}
    for col in columns:
        if col in df.columns:
            count = int((df[col] < 0).sum())
            if count:
                negatives[col] = count
    if negatives:
        logger.warning("Negative values found in %s: %s", label, negatives)


def make_mart_daily_kpi(df: pd.DataFrame) -> pd.DataFrame:
    _ensure_logger()
    df = df.copy()
    df["date"] = pd.to_datetime(df["event_time"], errors="coerce", utc=True).dt.date.astype(str)

    counts = (
        df.pivot_table(
            index=["date", "site"],
            columns="status",
            values="tool_id",
            aggfunc="count",
            fill_value=0,
        )
        .rename(columns={"Run": "run_events", "Down": "down_events", "Idle": "idle_events"})
        .reset_index()
    )

    if "run_events" not in counts.columns:
        counts["run_events"] = 0
    if "down_events" not in counts.columns:
        counts["down_events"] = 0
    if "idle_events" not in counts.columns:
        counts["idle_events"] = 0

    run_df = df[df["status"] == "Run"].copy()
    avg_cycle = (
        run_df.groupby(["date", "site"], dropna=False)["cycle_time_sec"]
        .mean()
        .reset_index()
        .rename(columns={"cycle_time_sec": "avg_cycle_time_sec"})
    )

    wafer_sum = (
        df.groupby(["date", "site"], dropna=False)["wafer_out"]
        .sum()
        .reset_index()
        .rename(columns={"wafer_out": "total_wafer_out"})
    )

    mart = counts.merge(avg_cycle, on=["date", "site"], how="left").merge(
        wafer_sum, on=["date", "site"], how="left"
    )

    mart["downtime_minutes"] = mart["down_events"] * 10
    mart["avg_cycle_time_sec"] = mart["avg_cycle_time_sec"].fillna(0)
    mart["total_wafer_out"] = mart["total_wafer_out"].fillna(0)

    mart = mart[
        [
            "date",
            "site",
            "run_events",
            "down_events",
            "idle_events",
            "downtime_minutes",
            "total_wafer_out",
            "avg_cycle_time_sec",
        ]
    ]

    logger.info("Daily KPI rows: %s", len(mart))
    _check_non_negative(
        mart,
        ["run_events", "down_events", "idle_events", "downtime_minutes", "total_wafer_out", "avg_cycle_time_sec"],
        "daily_kpi",
    )
    return mart


def make_mart_downtime_by_tooltype(df: pd.DataFrame) -> pd.DataFrame:
    _ensure_logger()
    df = df.copy()
    df["date"] = pd.to_datetime(df["event_time"], errors="coerce", utc=True).dt.date.astype(str)

    down_df = df[df["status"] == "Down"].copy()
    mart = (
        down_df.groupby(["date", "site", "tool_type"], dropna=False)
        .size()
        .reset_index(name="down_events")
    )
    mart["downtime_minutes"] = mart["down_events"] * 10
    mart = mart[["date", "site", "tool_type", "downtime_minutes"]]

    logger.info("Downtime by tool_type rows: %s", len(mart))
    _check_non_negative(mart, ["downtime_minutes"], "downtime_by_tooltype")
    return mart

