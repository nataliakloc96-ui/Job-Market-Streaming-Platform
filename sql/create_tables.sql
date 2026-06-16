CREATE TABLE job_events_raw (
    job_id TEXT PRIMARY KEY,
    title TEXT,
    company TEXT,
    location TEXT,
    salary INT,
    skills TEXT
);

CREATE TABLE job_metrics (
    job_title TEXT PRIMARY KEY,
    offers_count INT,
    avg_salary NUMERIC,
    min_salary INT,
    max_salary INT,
    updated_at TIMESTAMP DEFAULT NOW()
);