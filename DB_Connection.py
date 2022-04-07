import psycopg2
import sys
#import boto3
import os

ENDPOINT = "agoradb.cqg31s3ekxny.us-east-1.rds.amazonaws.com"
PORT = "5432"
USER = "postgres"
REGION = "us-east-1f"
DBNAME = "postgres"
PASSWORD = "236371Aa!"

# # gets the credentials from .aws/credentials
# session = boto3.Session(profile_name='RDSCreds')
# client = session.client('rds')

# token = client.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USER, Region=REGION)

try:
    #conn = psycopg2.connect(host=ENDPOINT, port=PORT, database=DBNAME, user=USER, password=token)
    conn = psycopg2.connect(host=ENDPOINT, port=PORT, database=DBNAME, user=USER, password=PASSWORD)
    cur = conn.cursor()
    cur.execute("""SELECT now()""")
    query_results = cur.fetchall()
    print(query_results)

    # cur.execute("""CREATE TABLE passengers(
    # id SERIAL PRIMARY KEY,
    # name text,
    # sex text,
    # age float,
    # sibsp integer,
    # parch integer)""")
    # conn.commit()

except Exception as e:
    print("Database connection failed due to {}".format(e))


