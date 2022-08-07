import sqlalchemy as sa
#from sqlalchemy.sql import func
from .DB_metadata import Base, metadata, session


class CitiesInfo(Base):

    __table__ = sa.Table("citiesinfo", metadata)

    def __init__(self, city, lat, lng, region):
        self.city = city
        self.region = region
        self.lat = lat
        self.lng = lng


def get_region(city):
    return session.query(CitiesInfo).filter(CitiesInfo.city == city).first().region


def get_cities_in_the_same_region(region):
    cities = session.query(CitiesInfo).filter(CitiesInfo.region == region).all()
    return [mapping.city for mapping in cities]


def get_regions():
    regions = []
    for region in session.query(CitiesInfo.region).distinct():
        regions.append(region[0])
    return regions


def get_cities():
    cities = []
    for city in session.query(CitiesInfo.city).distinct():
        cities.append(city[0])
    return cities

def get_cords_by_city(city):
    lat = session.query(CitiesInfo).filter(CitiesInfo.city == city).first().lat
    lng = session.query(CitiesInfo).filter(CitiesInfo.city == city).first().lng
    return lat, lng

