-- Daily downtime by site based on Down events
-- Assumes each status='Down' event equals 10 minutes downtime
SELECT
  date(event_time) AS date,
  site,
  COUNT(*) AS down_events,
  COUNT(*) * 10 AS downtime_minutes
FROM events
WHERE status = 'Down'
GROUP BY date(event_time), site
ORDER BY date, site;
