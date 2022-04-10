import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.sql import func
from sqlalchemy.orm import load_only
from DB_metadata import PASSWORD, ENDPOINT, DBNAME


pengine = sa.create_engine('postgresql+psycopg2://postgres:' + PASSWORD + '@' + ENDPOINT + '/' + DBNAME)
Base = declarative_base()
# reflect current database engine to metadata
metadata = sa.MetaData(pengine)
metadata.reflect()
Session = sa.orm.sessionmaker(pengine)
session = Session()


class Mapping(Base):

    __table__ = sa.Table("Mapping", metadata)

    def __init__(self, city, region):
        self.City = city
        self.Region = region

    @staticmethod
    def get_region(city):
        return session.query(Mapping).filter(Mapping.City == city).first().Region

    @staticmethod
    def get_cities_in_the_same_region(region):
        cities = session.query(Mapping).filter(Mapping.Region == region).all()
        return [mapping.City for mapping in cities]

    @staticmethod
    def get_regions():
        #return session.query(func.distinct(Mapping.Region)).all()
        regions = []
        for region in session.query(Mapping.Region).distinct():
            regions.append(region[0])
        return regions


    @staticmethod
    def get_cities():
        cities = []
        for city in session.query(Mapping.City).distinct():
            cities.append(city[0])
        return cities


#print(Mapping.get_regions())
#print(Mapping.get_cities())
print(Mapping.get_region("GIZO "))
#print(Mapping.get_cities_in_the_same_region("Ashkelon "))


