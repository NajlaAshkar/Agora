import psycopg2
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

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


#conn = psycopg2.connect(host=ENDPOINT, port=PORT, database=DBNAME, user=USER, password=token)
conn = psycopg2.connect(host=ENDPOINT, port=PORT, database=DBNAME, user=USER, password=PASSWORD)
cur = conn.cursor()
cur.execute("""SELECT now()""")
query_results = cur.fetchall()
print(query_results)
pengine = sa.create_engine('postgresql+psycopg2://postgres:' + PASSWORD + '@' + ENDPOINT + '/' + DBNAME)
# define declarative base
Base = declarative_base()
# reflect current database engine to metadata
metadata = sa.MetaData(pengine)
metadata.reflect()

from . import Users
Session = sa.orm.sessionmaker(pengine)
session = Session()

print(session.query(User).filter(User.PhoneNum == "0526866526").first().Name)
