INSERT INTO job_metrics
SELECT 
    title,
    COUNT(*),
    ROUND(AVG(salary),2),
    MIN(salary),
    MAX(salary),
    NOW()
FROM job_events_raw
GROUP BY title;