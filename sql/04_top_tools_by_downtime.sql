-- Top 10 tools by downtime based on Down events
-- Assumes each status='Down' event equals 10 minutes downtime
SELECT
  tool_id,
  tool_type,
  COUNT(*) AS down_events,
  COUNT(*) * 10 AS downtime_minutes
FROM events
WHERE status = 'Down'
GROUP BY tool_id, tool_type
ORDER BY downtime_minutes DESC, tool_id
LIMIT 10;
