FROM apache/airflow:2.9.1-python3.10
RUN pip install --no-cache-dir pandas>=2.0.0 requests>=2.31.0 psycopg2-binary>=2.9.0 sqlalchemy>=2.0.0