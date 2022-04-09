import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from DB_metadata import PASSWORD, ENDPOINT, DBNAME


pengine = sa.create_engine('postgresql+psycopg2://postgres:' + PASSWORD + '@' + ENDPOINT + '/' + DBNAME)
Base = declarative_base()
# reflect current database engine to metadata
metadata = sa.MetaData(pengine)
metadata.reflect()
Session = sa.orm.sessionmaker(pengine)
session = Session()

class Products(Base):
    __table__ = sa.Table("Products", metadata)

    @staticmethod
    def add_product():
        pass
    @staticmethod
    def delete_product():
        pass

    def add_photo(self, product_id, photo):
        pass
    @staticmethod
    def get_products_ordered_by_date(products):
        pass

    @staticmethod
    def get_all_products():
        # lex order
        pass


    # all filtering functions should return a list of product ids only
    @staticmethod
    def get_products_by_city(cities):
        # cities is a list of cities name - can assume that all of them exists
        pass

    @staticmethod
    def get_products_by_region(regions):
        # same as cities above
        pass

    @staticmethod
    def get_products_by_photo():
        pass

    @staticmethod
    def get_products_by_category(categories):
        pass

    @staticmethod
    def get_products_by_rating(rating):
        # all products with rating higher than the input
        pass

    @staticmethod
    def get_products_by_views():
        pass

    @staticmethod
    def get_products_by_name(name):
        # one name only
        pass





