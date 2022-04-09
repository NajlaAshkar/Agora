import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

ENDPOINT = "agoradb.cqg31s3ekxny.us-east-1.rds.amazonaws.com"
DBNAME = "postgres"
PASSWORD = "236371Aa!"

pengine = sa.create_engine('postgresql+psycopg2://postgres:' + PASSWORD + '@' + ENDPOINT + '/' + DBNAME)
Base = declarative_base()
# reflect current database engine to metadata
metadata = sa.MetaData(pengine)
metadata.reflect()


class User(Base):
    __table__ = sa.Table("User", metadata)

    @staticmethod
    def add_user(phone, name, email):
        pass

    def authenticate(self):
        pass

    def logout(self):
        pass

    @staticmethod
    def get_user_by_phone(phone):
        pass


Session = sa.orm.sessionmaker(pengine)
session = Session()





