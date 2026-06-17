# Architecture - Job Market Streaming Platform

This document describes the architecture of the real-time Data Engineering pipeline.

---

## High Level Architecture

              +----------------+
              | Python Producer |
              +--------+-------+
                       |
                       |
                       v
              +----------------+
              | Apache Kafka   |
              | job_events     |
              +--------+-------+
                       |
                       |
                       v
      +--------------------------------+
      | Spark Structured Streaming     |
      | - consume events               |
      | - parse JSON                   |
      | - transform data               |
      +---------------+----------------+
                      |
                      |
                      v
             +----------------+
             | PostgreSQL     |
             | RAW Layer      |
             +-------+--------+
                     |
                     |
                     v
            +----------------+
            | Apache Airflow |
            | DAG Scheduler  |
            +-------+--------+
                    |
                    |
                    v
         +--------------------+
         | Analytics Tables   |
         | job_metrics        |
         +---------+----------+
                   |
                   |
                   v
         +--------------------+
         | Streamlit Dashboard|
         +--------------------+



---

# Components


## Producer

Responsible for generating streaming job market events.

Technologies:

- Python
- Faker
- Kafka Producer


---

## Kafka

Kafka acts as a message broker.

Responsibilities:

- receive events
- store messages
- provide streaming source


Topic:
job_events


---

## Spark Structured Streaming

Spark continuously processes Kafka events.

Responsibilities:

- consume messages
- apply schema
- transform data
- save results


Output table:
job_events_raw

---

## PostgreSQL

Two data layers:


### RAW
job_events_raw


Stores incoming events.


### Analytics
job_metrics


Contains aggregated business metrics.


---

## Airflow

Orchestrates analytics refresh.

DAG:
refresh_job_metrics


Runs SQL transformations.


---

## Dashboard

Streamlit dashboard visualizes:

- average salaries
- offer counts
- market trends


---

## Data Flow
Kafka Event
 ↓
Spark Micro Batch
 ↓
PostgreSQL Insert
 ↓
Airflow Transformation
 ↓
Dashboard Update