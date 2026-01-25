-- Daily throughput by site based on Run events
-- total_wafer_out sums wafer_out for run events
SELECT
  date(event_time) AS date,
  site,
  SUM(wafer_out) AS total_wafer_out,
  COUNT(*) AS run_events
FROM events
WHERE status = 'Run'
GROUP BY date(event_time), site
ORDER BY date, site;
