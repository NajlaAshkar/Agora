import sqlalchemy as sa
import logging as log
import psycopg2
import Mapping
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from DB_metadata import PASSWORD, ENDPOINT, DBNAME


pengine = sa.create_engine('postgresql+psycopg2://postgres:' + PASSWORD + '@' + ENDPOINT + '/' + DBNAME)
Base = declarative_base()
# reflect current database engine to metadata
metadata = sa.MetaData(pengine)
metadata.reflect()
Session = sa.orm.sessionmaker(pengine)
session = Session()


class ProductAlreadyExists(Exception):
    pass


class ProductDoesNotExist(Exception):
    pass


class ProductHasAnImage(Exception):
    pass


class IllegalAttributes(Exception):
    pass


class Products(Base):
    __table__ = sa.Table("Products", metadata)

    def __init__(self, name: str, category: int, description: str, rating: int, city: str, phone: str, image_url=None):
        if len(name) > 50 or not 0 <= category <= 5 or len(description) > 200 or not 1 <= rating <= 5 or len(city) > 50 or len(phone) != 10:
            message = "tried to add a product with illegal attributes"
            log.warning(message)
            raise IllegalAttributes(message)
        self.name = name
        self.Region = Mapping.get_region(city)
        self.Category = category
        self.Date = datetime.today().strftime('%Y-%m-%d')
        self.Description = description
        self.Rating = rating
        self.City = city
        self.PhoneNum = phone
        if image_url is not None:
            pic = open(image_url, 'rb').read()
            self.Image = psycopg2.Binary(pic)

    def inc_num_of_views(self):
        self.NumOfViewa += 1

    @staticmethod
    def add_product(name, category, description, rating, city, phone, image_url=None):
        try:
            session.add(Products(name, category, description, rating, city, phone, image_url))
            session.commit()
        except Exception as e:
            log.warning(e)
            raise ProductAlreadyExists(e)

    @staticmethod
    def delete_product(product_id):
        product = Products.query.get(product_id)
        if product is None:
            message = "Tried to remove product with id {} which does not exist".format(product)
            log.warning(message)
            raise ProductDoesNotExist(message)
        session.delete(product)
        session.commit()

    @staticmethod
    def add_photo(product_id, img_url):
        product = Products.query.get(product_id)
        if product is None:
            message = "Tried to add image to product with id {} which does not exist".format(product_id)
            log.warning(message)
            raise ProductDoesNotExist(message)
        if product.Image is not None:
            message = "Tried to add image to product with id {} which already has one".format(product_id)
            log.warning(message)
            raise ProductHasAnImage(message)

        try:
            # read data from a picture
            pic = open(img_url, 'rb').read()
            # execute the UPDATE statement
            product.Image = psycopg2.Binary(pic)
            # commit the changes to the database - maybe no need
            session.commit()
        except Exception as error:
            log.warning(error)

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
#print(Products.get_all_products())

