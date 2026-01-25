import argparse
import logging
import os

from src import generate_data
from src.etl.extract import extract_events
from src.etl.load import load_to_sqlite, write_marts
from src.etl.transform import make_mart_daily_kpi, make_mart_downtime_by_tooltype


logger = logging.getLogger(__name__)


def _repo_root() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _events_path() -> str:
    return os.path.join(_repo_root(), "data", "generated", "events.csv")


def _marts_dir() -> str:
    return os.path.join(_repo_root(), "output", "marts")


def _warehouse_db_path() -> str:
    return os.path.join(_repo_root(), "output", "warehouse.db")


def _schema_path() -> str:
    return os.path.join(_repo_root(), "src", "db", "schema.sql")


def _generate_data() -> str:
    output_path = _events_path()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    rows = generate_data.generate_events()
    generate_data.write_events_csv(rows, output_path)
    logger.info("Wrote %s rows to %s", len(rows), output_path)
    return output_path


def _run_etl(events_path: str) -> None:
    df = extract_events(events_path)
    daily_kpi = make_mart_daily_kpi(df)
    downtime_by_tooltype = make_mart_downtime_by_tooltype(df)
    load_to_sqlite(df, _warehouse_db_path(), _schema_path())
    write_marts(daily_kpi, downtime_by_tooltype, _marts_dir())


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
    parser = argparse.ArgumentParser(description="Ops Insights pipeline runner")
    parser.add_argument("--generate-data", action="store_true", help="Generate events CSV")
    parser.add_argument("--run-etl", action="store_true", help="Run ETL to build marts")
    args = parser.parse_args()

    if not args.generate_data and not args.run_etl:
        parser.print_help()
        return

    events_path = _events_path()
    if args.generate_data:
        events_path = _generate_data()

    if args.run_etl:
        if not os.path.exists(events_path):
            raise FileNotFoundError(f"Events CSV not found: {events_path}")
        _run_etl(events_path)


if __name__ == "__main__":
    main()

