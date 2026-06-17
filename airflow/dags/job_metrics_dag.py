from airflow import DAG
from airflow.operators.python import PythonOperator

from datetime import datetime, UTC

import psycopg2

def refresh_metrics():
    conn = psycopg2.connect(
        host="job-postgres",
        database="jobs_db",
        user="postgres",
        password="postgres"
    )

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO job_metrics (
            job_title,
            offers_count,
            avg_salary,
            min_salary,
            max_salary
        )

        SELECT 
            title,
            COUNT(*) AS offers_count,
            ROUND(AVG(salary),2),
            MIN(salary),
            MAX(salary)
        FROM job_events_raw
        GROUP BY title
        ON CONFLICT (job_title)
        DO UPDATE SET

        offers_count = EXCLUDED.offers_count,
        avg_salary = EXCLUDED.avg_salary,
        min_salary = EXCLUDED.min_salary,
        max_salary = EXCLUDED.maX_salary,
        updated_at = NOW();

        """
    )

    conn.commit()

    cur.close()
    conn.close()

with DAG(
    dag_id="refresh_job_metrics",
    start_date=datetime(2026,1,1),
    schedule_interval="@daily",
    catchup=False
):
    refresh = PythonOperator(
        task_id="refresh_metrics",
        python_callable=refresh_metrics
    )