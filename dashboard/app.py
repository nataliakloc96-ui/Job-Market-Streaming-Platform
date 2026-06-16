import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px


st.set_page_config(
    page_title="Job Market Analytics",
    layout="wide"
)

st.title("📊 Job Market Analytics")

conn = psycopg2.connect(
    host="postgres",
    database="postgres",
    user="postgres",
    password="postgres"
)

df = pd.read_sql(
    """
    SELECT *
    FROM job_metrics
    ORDER BY avg_salary DESC
    
    """,
    conn
)

st.subheader("Job metrics")

st.dataframe(df)

fig = px.bar(
    df,
    x="job_title",
    y="avg_salary",
    title="Average salary by role"
)

st.plotly_chart(fig)

fig2 = px.bar(
    df,
    x="job_title",
    y="offers_count",
    title="Number of offers"
)

st.plotly_chart(fig2)