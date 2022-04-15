import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

ENDPOINT = "agoradb.cqg31s3ekxny.us-east-1.rds.amazonaws.com"
PORT = "5432"
USER = "postgres"
REGION = "us-east-1f"
DBNAME = "postgres"
PASSWORD = "236371Aa!"

pengine = sa.create_engine('postgresql+psycopg2://postgres:' + PASSWORD + '@' + ENDPOINT + '/' + DBNAME)
Base = declarative_base()
# reflect current database engine to metadata
metadata = sa.MetaData(pengine)
metadata.reflect()
Session = sa.orm.sessionmaker(pengine)
session = Session()



