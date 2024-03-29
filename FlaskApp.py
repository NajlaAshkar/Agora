import gzip
from datetime import time

import werkzeug
import time

import flask
import werkzeug
from flask import Flask, request, send_from_directory, make_response
from flask_login import LoginManager
from flask_session import Session
import os

import json

from Models.DB_metadata import PASSWORD, ENDPOINT, DBNAME
from Models import Users, Mapping, Products, validate_database, citiesinfo


def init_app():

    flaskApp = Flask(__name__)
    flaskApp.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:' + PASSWORD + '@' + ENDPOINT + '/' + DBNAME
    flaskApp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flaskApp.config['Accept-encoding'] = True
    from Models import db
    db.init_app(flaskApp)
    # login_manager = LoginManager()
    # login_manager.init_app(flaskApp)
    sess = Session()
    sess.init_app(flaskApp)
    return flaskApp, db


app, db = init_app()
app.app_context().push()


def build_response(message=None, code=200, error_code=-1, json=None, error_message=None):
    if json is not None:
        return json, code
    to_return = {}
    if message:
        to_return["message"] = message
    if error_code != -1:
        to_return["error_code"] = error_code
        if error_message:
            to_return["error_message"] = error_message
    return to_return, code


@app.route('/', methods=['GET'])
def index():
    return "Successfully Connected"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/login', methods=['GET', 'POST'])
def user_login():
    data = request.json or request.form
    email = data.get("email", None)
    if not email:
        return build_response(error_message="Illegal Attributes", error_code=400, code=400)
    user = Users.get_user_by_email(email)
    if not user:
        data = {"email": email}
        return build_response(json=data, code=200)

    data = {"email": user.Email, "phone": user.PhoneNum, "name": user.Name}
    return build_response(json=data, code=200)


@app.route('/get_user_by_email', methods=['GET', 'POST'])
def get_user():
    data = request.json or request.form
    email = data.get("email", None)
    if not email:
        return build_response(error_message="Illegal Attributes", error_code=400, code=400)
    try:
        user = Users.get_user_by_email(email)
    except Users.UserDoesNotExist as e:
        return build_response(error_message="User does not exist", error_code=409, code=409)
    data = {"email": user.Email, "phone": user.PhoneNum, "name": user.Name}
    return build_response(json=data, code=200)


@app.route('/logout', methods=['POST'])
def user_logout():
    pass


@app.route('/signup', methods=['POST'])
def user_signup():
    data = request.json or request.form
    email = data.get("email", None)
    phone = data.get("phone", None)
    name = data.get("name", None)
    try:
        user = Users.add_user(phone, name, email)
    except Users.UserAlreadyExists as e:
        return build_response(error_message="User already exists", error_code=409, code=409)
    except Users.UserWithIllegalAttributes as e:
        return build_response(error_message="Illegal Attributes", error_code=400, code=400)
    else:
        return build_response(json={"email": user.Email, "name": user.Name, "phone": user.PhoneNum})


@app.route('/get_region', methods=['POST'])
def get_region():
    data = request.json or request.form
    city = data.get("city", None)
    region = citiesinfo.get_region(city)
    return build_response(json={"region": region})


@app.route('/get_cities_in_the_same_region', methods=['POST'])
def get_cities_in_the_same_region():
    data = request.json or request.form
    region = data.get("region", None)
    cities = citiesinfo.get_cities_in_the_same_region(region)
    return build_response(json={"cities": [cities]})


@app.route('/get_all_regions', methods=['GET'])
def get_all_regions():
    regions = citiesinfo.get_regions()
    regions.sort()
    return build_response(json={"regions": regions})


@app.route('/get_all_cities', methods=['GET'])
def get_all_cities():
    cities = citiesinfo.get_cities()
    cities.sort()
    return build_response(json={"cities": cities})


# @app.route('/add_image', methods = ['GET', 'POST'])
# def handle_request():
#     files_ids = list(flask.request.files)
#     print("\nNumber of Received Images : ", len(files_ids))
#     image_num = 1
#     for file_id in files_ids:
#         print("\nSaving Image ", str(image_num), "/", len(files_ids))
#         imagefile = flask.request.files[file_id]
#         filename = werkzeug.utils.secure_filename(imagefile.filename)
#         print("Image Filename : " + imagefile.filename)
#         timestr = time.strftime("%Y%m%d-%H%M%S")
#         imagefile.save(timestr+'_'+filename)
#         image_num = image_num + 1
#     print("\n")
#     return "Image(s) Uploaded Successfully. Come Back Soon."


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    data = request.json or request.form
    name = data.get("name", None)
    category = data.get("category", None)
    desc = data.get("description", None)
    rating = data.get("rating", None)
    city = data.get("city", None)
    phone = data.get("phone", None)
    image_url = data.get("img_url", None)

    try:
        product = Products.add_product(name, category, desc, rating, city, phone, image_url)
    except Products.ProductAlreadyExists as e:
        return build_response(error_message="Product already exists", error_code=409, code=409)
    except Products.IllegalProductAttributes as e:
        return build_response(error_message="Illegal Attributes", error_code=400, code=400)
    else:
        return build_response(json={"name": product.Name, "category": product.Category, "description": product.Description,
                                    "rating": product.Rating, "city": product.City, "phone": product.PhoneNum,
                                    "image_url": product.Image, "ID": product.ID, "region": product.Region,
                                    "date": product.Date, "views": product.NumOfViews})


@app.route('/delete_product', methods=['GET', 'POST'])
def delete_product():
    data = request.json or request.form
    product_id = data.get("product_id", None)
    try:
        Products.delete_product(product_id)
    except Products.ProductDoesNotExist as e:
        return build_response(error_message="Product does not exist", error_code=409, code=409)
    else:
        return build_response(json={"product_id": product_id})


@app.route('/add_image', methods=['GET', 'POST'])
# saves image locally and then should call "add_photo" in order to save its path in the DB
def handle_request():
    files_ids = list(request.files)
    image_num = 1
    for file_id in files_ids:
        print("\nSaving Image ", str(image_num), "/", len(files_ids))
        imagefile = request.files[file_id]
        filename = werkzeug.utils.secure_filename(imagefile.filename)
        print("Image Filename : " + imagefile.filename)
        timestr = time.strftime("%Y%m%d-%H%M%S")
        imagefile.save(timestr + '_' + filename)
        image_num = image_num + 1
        img_url = os.getcwd() + "\\" + timestr + '_' + filename
    return build_response(json={"img_url": img_url})


@app.route('/add_photo', methods=['GET', 'POST'])
def add_photo():
    data = request.json or request.form
    product_id = data.get("product_id", None)
    img_url = data.get("img_url", None)
    try:
        Products.add_photo(product_id, img_url)
    except Products.ProductDoesNotExist as e:
        return build_response(error_message="Product does not exist", error_code=409, code=409)
    except Products.ProductHasAnImage as e:
        return build_response(error_message="Product has an image", error_code=409, code=409)
    except Products.IllegalImgUrl as e:
        return build_response(error_message="Illegal Img Url", error_code=400, code=400)
    else:
        return build_response(json={"product_id": product_id})


@app.route('/get_products_ordered_by_date', methods=['GET'])
def get_products_ordered_by_date():
    products = Products.get_products_ordered_by_date()
    return build_response(json={"products": products})


@app.route('/get_all_products', methods=['GET'])
def get_all_products():
    products = Products.get_all_products()
    return build_response(json={"products": products})


@app.route('/most_viewed_products', methods=['GET'])
def get_most_viewed():
    most_viewed = Products.get_most_viewed_products()
    return build_response(json={"most_viewed": most_viewed})

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

@app.route('/filter_products', methods=['POST'])
def filter_products():
    # the request should look like:
    # json = {"cities":[list of cities name], "regions": [list of regions], "photo": yes or None,
    # "categories": [list of categories names], "rating": 0<= int <= 5, "name": string (one name)}
    # for every filter which is not used - should send None or not include it at all in the json
    data = request.json or request.form
    cities = data.get("cities", None)
    regions = data.get("regions", None)
    has_img = data.get("photo", None)
    categories = data.get("categories", None)
    rating = data.get("rating", None)
    name = data.get("name", None)
    all_products = Products.get_all_products_ids()
    if cities:
        cities_filtered = Products.get_products_by_city(cities)
        print("city: ", cities_filtered)
    else:
        cities_filtered = all_products
    if regions:
        regions_filtered = Products.get_products_by_region(regions)
        print("regions: ", regions_filtered)
    else:
        regions_filtered = all_products
    if has_img:
        img_filtered = Products.get_products_by_photo()
        print("images: ", img_filtered)
    else:
        img_filtered = all_products
    if categories:
        categories_filtered = Products.get_products_by_category(categories)
        print("categories: ", categories_filtered)
    else:
        categories_filtered = all_products
    if rating:
        rating_filtered = Products.get_products_by_rating(rating)
        print("rating: ", rating_filtered)
    else:
        rating_filtered = all_products
    if name:
        name_filtered = Products.get_products_by_name(name)
    else:
        name_filtered = all_products

    filtered_products = intersection(intersection(intersection(intersection(cities_filtered, regions_filtered), img_filtered), categories_filtered),rating_filtered)
    print(filtered_products)
    res = []

    for i in filtered_products:
        res.append(Products.toJson_minimal(Products.get_product_by_id(i)))
    return build_response(json={"products": res})


@app.route('/get_product_by_id', methods=['POST'])
def get_product_by_id():
    data = request.json or request.form
    id = data.get("product_id", None)
    try:
        cur = Products.get_product_by_id(id)
    except Products.ProductDoesNotExist as e:
        return build_response(error_message="Product does not exist", error_code=409, code=409)
    else:
        res = Products.toJson(cur)
        content = gzip.compress(json.dumps(res).encode('utf8'), 5)
        response = make_response(content)
        response.headers['Content-length'] = len(content)
        response.headers['Content-Encoding'] = 'gzip'
        return response
        # return build_response(json=json)


@app.route('/inc_num_of_views', methods=['POST'])
def inc_num_of_views():
    data = request.json or request.form
    user_email = data.get("email", None)
    user = Users.get_user_by_email(user_email)
    id = data.get("product_id", None)
    product = Products.get_product_by_id(id)
    if product.PhoneNum == user.PhoneNum:
        return build_response(json={})
    try:
        Products.inc_num_of_views(id)
    except Products.ProductDoesNotExist as e:
        return build_response(error_message="Product does not exist", error_code=409, code=409)
    else:
        return build_response(json={})


@app.route('/get_products_in_search_radius', methods=['POST'])
def get_products_in_search_radius():
    data = request.json or request.form
    radius = data.get("radius", None)
    lat = data.get("lat", None)
    lng = data.get("lng", None)
    products = Products.get_all_products_radius_search(radius, lat, lng)
    if len(products) == 0:
        empty = 1
    else:
        empty = 0
    return build_response(json={"products": products, "empty": empty})


@app.route('/get_my_products', methods=['POST'])
def get_my_products():
    data = request.json or request.form
    email = data.get("email", None)
    products = Products.get_my_products(email)
    if len(products) > 0:
        flag = 1
    else:
        flag = 0
    return build_response(json={"products": products, "flag": flag})




if __name__ == "__main__":
    os.chdir("../")
    app.run(host="0.0.0.0", port=3000, use_reloader=True, debug=True, use_debugger=True)
    validate_database()


