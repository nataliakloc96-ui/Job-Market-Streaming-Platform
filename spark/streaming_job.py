from pyspark.sql import SparkSession
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

    (
        batch_df
        .write
        .format("jdbc")
        .option(
            "url",
            "jdbc:postgresql://job-postgres:5432/postgres"
        )
        .option(
            "dbtable",
            "job_events_raw"
        )
        .option(
            "user",
            "postgres"
        )
        .option(
            "password",
            "postgres"
        )
        .option(
            "driver",
            "org.postgresql.Driver"
        )
        .mode("append")
        .save()
    )

query = (
    jobs.writeStream
    .foreachBatch(save_to_postgres)
    .start()
)

query.awaitTermination()