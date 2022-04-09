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


class Mapping(Base):

    __table__ = sa.Table("Mapping", metadata)

    @staticmethod
    def get_region(city):
        pass

    @staticmethod
    def get_cities_in_the_same_region(region):
        pass

    @staticmethod
    def get_all_regions():
        pass

    @staticmethod
    def get_cities():
        pass


