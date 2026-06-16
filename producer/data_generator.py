from faker import Faker
import random

fake = Faker()

SKILLS = [
    "Python",
    "SQL",
    "Spark",
    "Airflow",
    "Docker",
    "AWS",
    "Kafka"
]

def generate_job():

    return {
        "job_id": fake.uuid4(),
        "title": random.choice(
            [
                "Data Engineer",
                "Python Developer",
                "Analytics Engineer",
                "BI Developer"
            ]
        ),
        "company": fake.company(),
        "location": random.choice(
            [
                "Remote",
                "Warsaw",
                "Krakow",
                "Wroclaw"
            ]
        ),
        "salary": random.randint(
            8000,
            25000
        ),
        "skills": random.sample(
            SKILLS,
            3
        )
    }