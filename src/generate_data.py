import csv
import os
import random
from datetime import datetime, timedelta, timezone


def _make_output_path() -> str:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, "data", "generated")
    os.makedirs(output_dir, exist_ok=True)
    return os.path.join(output_dir, "events.csv")


def _build_tool_catalog() -> dict:
    tool_types = ["Litho", "Etch", "Deposition", "CMP", "Metrology"]
    catalog = {}
    for idx in range(1, 26):
        tool_id = f"TOOL-{idx:03d}"
        catalog[tool_id] = tool_types[(idx - 1) % len(tool_types)]
    return catalog


def _random_event_time(start: datetime, end: datetime) -> datetime:
    start_ts = start.timestamp()
    end_ts = end.timestamp()
    return datetime.fromtimestamp(random.uniform(start_ts, end_ts), tz=timezone.utc)


def _pick_status() -> str:
    roll = random.random()
    if roll < 0.7:
        return "Run"
    if roll < 0.9:
        return "Idle"
    return "Down"


def generate_events(row_count: int = 20000) -> list[dict]:
    now = datetime.now(tz=timezone.utc)
    start = now - timedelta(days=30)
    sites = ["FAB-A", "FAB-B", "FAB-C"]
    shifts = ["Day", "Night"]
    alarms = ["A101", "A205", "A310", "A404"]
    tool_catalog = _build_tool_catalog()
    tool_ids = list(tool_catalog.keys())

    rows = []
    for _ in range(row_count):
        status = _pick_status()
        alarm_code = ""
        cycle_time_sec = 0
        wafer_out = 0

        if status == "Down":
            alarm_code = random.choice(alarms)
        if status == "Run":
            cycle_time_sec = random.randint(30, 300)
            wafer_out = random.randint(1, 25)

        tool_id = random.choice(tool_ids)
        event_time = _random_event_time(start, now).isoformat().replace("+00:00", "Z")

        rows.append(
            {
                "event_time": event_time,
                "site": random.choice(sites),
                "tool_id": tool_id,
                "tool_type": tool_catalog[tool_id],
                "status": status,
                "alarm_code": alarm_code,
                "cycle_time_sec": cycle_time_sec,
                "wafer_out": wafer_out,
                "operator_shift": random.choice(shifts),
            }
        )
    return rows


def write_events_csv(rows: list[dict], output_path: str) -> None:
    fieldnames = [
        "event_time",
        "site",
        "tool_id",
        "tool_type",
        "status",
        "alarm_code",
        "cycle_time_sec",
        "wafer_out",
        "operator_shift",
    ]
    with open(output_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    output_path = _make_output_path()
    rows = generate_events()
    write_events_csv(rows, output_path)
    print(f"Wrote {len(rows)} rows to {output_path}")


if __name__ == "__main__":
    main()

