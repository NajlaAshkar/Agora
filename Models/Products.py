import base64

import sqlalchemy as sa
import logging as log
import psycopg2

import geopy.distance

from . import Mapping, citiesinfo
from datetime import datetime
from .DB_metadata import Base, metadata, session


class ProductAlreadyExists(Exception):
    pass


class ProductDoesNotExist(Exception):
    pass


class ProductHasAnImage(Exception):
    pass


class IllegalProductAttributes(Exception):
    pass


class IllegalImgUrl(Exception):
    pass


class Products(Base):

    __table__ = sa.Table("Products", metadata)

    def __init__(self, name: str, category: int, description: str, rating: int, city: str, phone: str, image_url=None):
        print("name:",name, "desc:", description,"city:",city, "phone:",phone, "image:", image_url)
        if len(name) > 50 or not (0 <= category <= 5) or len(description) > 200 or not (1 <= rating <= 5) or len(city) > 50 or len(phone) != 10:
            message = "tried to add a product with illegal attributes"
            log.warning(message)
            raise IllegalProductAttributes(message)
        self.Name = name
        self.Region = citiesinfo.get_region(city)
        self.Category = category
        self.Date = datetime.today().strftime('%Y-%m-%d')
        self.Description = description
        self.Rating = rating
        self.City = city
        self.PhoneNum = phone
        if image_url is not None:
            self.Image = psycopg2.Binary(image_url)



def inc_num_of_views(product_id):
    product = session.query(Products).get(product_id)
    print("product id ***:", product_id)
    if product is None:
        message = "Tried to access product with id {} which does not exist".format(product)
        log.warning(message)
        raise ProductDoesNotExist(message)
    product.NumOfViews += 1
    session.commit()


def add_product(name, category, description, rating, city, phone, image_url=None):
    try:
        cur = Products(name, category, description, rating, city, phone, image_url)
        session.add(cur)
        session.commit()
    except Exception as e:
        log.warning(e)
        print(e)
        raise ProductAlreadyExists(e)
    else:
        return cur


def delete_product(product_id):
    product = session.query(Products).get(product_id)
    if product is None:
        message = "Tried to remove product with id {} which does not exist".format(product)
        log.warning(message)
        raise ProductDoesNotExist(message)
    session.delete(product)
    session.commit()


def add_photo(product_id, img_url):
    product = session.query(Products).get(product_id)
    if product is None:
        message = "Tried to add image to product with id {} which does not exist".format(product_id)
        log.warning(message)
        raise ProductDoesNotExist(message)
    if product.Image is not None:
        message = "Tried to add image to product with id {} which already has one".format(product_id)
        log.warning(message)
        raise ProductHasAnImage(message)
    img_type = img_url[-3:]
    img_type2 = img_url[-4:]
    if img_url == '' or (img_type not in ["png", "jpg"] and img_type2 not in ["jpeg"]):
        message = "Tried to add image to product with id {} using broken img url".format(product_id)
        log.warning(message)
        raise IllegalImgUrl(message)
    product.Image = img_url
    session.commit()


def get_products_ordered_by_date():
    # products = get_all_products()
    # products.sort(key=lambda product: product["date"])
    # return products
    tmp = session.query(Products).order_by(Products.Date.desc()).all()
    return [toJson(product) for product in tmp]


def toJson(product):

    if product.Image is None:
        return {"name": product.Name, "category": product.Category, "description": product.Description,
                "rating": product.Rating, "city": product.City, "phone": product.PhoneNum,
                "image_url": product.Image, "ID": product.ID, "region": product.Region,
                "has_image": "no"}

    # img = Image.open(product.Image)
    # img_bitmap = img.tobitmap()
    with open(product.Image, "rb") as image:
        b64string = base64.b64encode(image.read()).decode('ASCII')

    return {"name": product.Name, "category": product.Category, "description": product.Description,
            "rating": product.Rating, "city": product.City, "phone": product.PhoneNum,
            "image_url": b64string, "ID": product.ID, "region": product.Region,
            "has_image": "yes"}


def toJson_minimal(product):

    return {"name": product.Name, "rating": product.Rating, "city": product.City, "ID": product.ID}


def get_all_products():
    # no need to specify a column
    try:
        products = session.query(Products).all()
    except Exception as e:
        session.rollback()
        return
    res = []
    for product in products:
        res.append(toJson_minimal(product))
    return res


# all filtering functions should return a list of product ids only

def get_products_by_city(cities):
    # cities is a list of cities name - can assume that all of them exists
    tmp = session.query(Products).all()
    res = []
    for product in tmp:
        if product.City in cities:
            res.append(product.ID)
    return res


def get_products_by_region(regions):
    # same as cities above
    tmp = session.query(Products).all()
    res = []
    for product in tmp:
        if product.Region in regions:
            res.append(product.ID)
    return res



def get_products_by_photo():
    tmp = session.query(Products).filter(Products.Image.is_not(None)).all()
    return [product.ID for product in tmp]


def get_products_by_category(categories):
    tmp = session.query(Products).filter(Products.Category == categories).all()
    return [product.ID for product in tmp]


def get_products_by_rating(rating):
    # all products with rating higher than the input
    tmp = session.query(Products).filter(Products.Rating >= rating).all()
    return [product.ID for product in tmp]


def get_most_viewed_products():
    tmp = session.query(Products).order_by(Products.NumOfViews.desc()).limit(10).all()
    return [toJson_minimal(product) for product in tmp]


def get_products_by_name(name):
    # one name only
    tmp = session.query(Products).filter(Products.Name == name).all()
    return [product.ID for product in tmp]


def get_product_by_id(_id):
    tmp = session.query(Products).filter(Products.ID == _id).all()
    return tmp[0]


def get_all_products_ids():
    tmp = session.query(Products).all()
    return [product.ID for product in tmp]


def get_all_products_radius_search(radius, lat, lng):
    products = session.query(Products).all()
    cur_cords = (lat, lng)
    res = []
    for product in products:
        city = product.City
        cords = citiesinfo.get_cords_by_city(city)
        if geopy.distance.geodesic(cur_cords, cords).km <= radius:
            res.append(toJson_minimal(product))
    return res



