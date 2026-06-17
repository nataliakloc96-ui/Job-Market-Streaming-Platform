from pyspark.sql import SparkSession
import psycopg2
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    ArrayType
)

spark = (
    SparkSession.builder
    .appName("JobMarketStreaming")
    .getOrCreate()
)

schema = StructType([
    StructField("job_id", StringType()),
    StructField("title", StringType()),
    StructField("company", StringType()),
    StructField("location", StringType()),
    StructField("salary", IntegerType()),
    StructField(
        "skills", ArrayType(StringType())
    )
])

raw_df = (
    spark.readStream
    .format("kafka")
    .option(
        "kafka.bootstrap.servers", "job-kafka:29092"
    )
    .option(
        "subscribe", "job_events"
    )
    .option(
        "startingOffsets", "earliest"
    )
    .load()
)

jobs = (
    raw_df
    .selectExpr(
        "CAST(value AS STRING)"
    )
    .select(
        from_json(
            col("value"),
            schema
        ).alias("data")
    )
    .select("data.*")
)

def save_to_postgres(batch_df, batch_id):

    print(f"\n========== Batch: {batch_id} ==========")

    batch_df.select(
        "title",
        "salary"
    ).show(
        truncate=False
    )

    rows = batch_df.collect()

    conn = psycopg2.connect(
        host="postgres",
        database="jobs_db",
        user="postgres",
        password="postgres"
    )

    cur = conn.cursor()

    for row in rows:
        cur.execute(
            """
            INSERT INTO job_events_raw (
                job_id,
                title,
                company,
                location,
                salary,
                skills
            )
            VALUES (%s,%s,%s,%s,%s,%s)
            ON CONFLICT (job_id)
            DO NOTHING
            """,
            (
                row.job_id,
                row.title,
                row.company,
                row.location,
                row.salary,
                row.skills,
            )
        )
    conn.commit()
    cur.close()
    conn.close()
    print(f"Batch {batch_id} saved")

query = (
    jobs.writeStream
    .foreachBatch(save_to_postgres)
    .option(
        "checkpointLocation",
        "/tmp/job_stream/checkpoint"
    )
    .start()
)

print("Spark streaming started")

query.awaitTermination()

    