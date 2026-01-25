CREATE TABLE IF NOT EXISTS events (
    event_time TEXT,
    site TEXT,
    tool_id TEXT,
    tool_type TEXT,
    status TEXT,
    alarm_code TEXT,
    cycle_time_sec REAL,
    wafer_out INTEGER,
    operator_shift TEXT
);

CREATE INDEX IF NOT EXISTS idx_events_event_time
    ON events (event_time);

CREATE INDEX IF NOT EXISTS idx_events_tool_id
    ON events (tool_id);

