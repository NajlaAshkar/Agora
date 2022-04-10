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

    def __init__(self, name, category, description, rating, city, phone, image=None):
        pass

    @staticmethod
    def add_product(name, category, description, rating, city, phone, image=None):
        pass

    @staticmethod
    def delete_product():
        pass

    def add_photo(self, product_id, photo):
        pass

    @staticmethod
    def get_products_ordered_by_date(products):
        return products.sort(key=lambda product: product.Date)

    @staticmethod
    def get_all_products():
        # no need to specify a column
        products = session.query(Products).all()
        return products


    # all filtering functions should return a list of product ids only

    @staticmethod
    def get_products_by_city(cities):
        # cities is a list of cities name - can assume that all of them exists
        tmp = session.query(Products).filter_by(Products.City in cities).all()
        return [product.ID for product in tmp]

    @staticmethod
    def get_products_by_region(regions):
        # same as cities above
        tmp = session.query(Products).filter_by(Products.Region in regions).all()
        return [product.ID for product in tmp]

    @staticmethod
    def get_products_by_photo():
        tmp = session.query(Products).filter(not(Products.Image is None)).all()
        return [product.ID for product in tmp]

    @staticmethod
    def get_products_by_category(categories):
        tmp = session.query(Products).filter_by(Products.Category in categories).all()
        return [product.ID for product in tmp]

    @staticmethod
    def get_products_by_rating(rating):
        # all products with rating higher than the input
        tmp = session.query(Products).filter(Products.Rating >= rating).all()
        return [product.ID for product in tmp]

    @staticmethod
    def get_most_viewed_products():
        tmp = session.query(Products).order_by(Products.NumOfViews).limit(10).all()
        return [product.ID for product in tmp]

    @staticmethod
    def get_products_by_name(name):
        # one name only
        tmp = session.query(Products).filter(Products.Name == name).all()
        return [product.ID for product in tmp]

#print(Products.get_products_ordered_by_date())
print(Products.get_all_products())

