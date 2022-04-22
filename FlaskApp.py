from flask import Flask, request
from flask_login import LoginManager
from flask_session import Session
import os
from Models import Users

def init_app():

    flaskApp = Flask(__name__)
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


@app.route('/login', methods=['GET', 'POST'])
def user_login():
    data = request.json or request.form
    email = data.get("email", None)
    try:
        user = Users.get_user_by_email(email)
        data = {"email": user.Email, "phone": user.PhoneNum, "name": user.Name}
    except Users.UserDoesNotExist as e:
        return build_response(code=401, error_code=401, error_message=e.args[0])
    return build_response(json=data, code=200)


@app.route('/logout', methods=['POST'])
def user_logout():
    pass


@app.route('/signup', methods=['POST'])
def user_signup():
    pass

@app.route('/get_region', methods=['GET'])
def get_region():
    pass

@app.route('/get_cities_in_the_same_region', methods=['GET'])
def get_cities_in_the_same_region():
    pass

@app.route('/get_all_regions', methods=['GET'])
def get_all_regions():
    pass

@app.route('/get_all_cities', methods=['GET'])
def get_all_cities():
    pass

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    pass


@app.route('/delete_product', methods=['GET', 'POST'])
def delete_product():
    pass

@app.route('/add_photo', methods=['GET', 'POST'])
def add_photo():
    pass

@app.route('/get_products_ordered_by_date', methods=['GET'])
def get_products_ordered_by_date():
    pass

@app.route('/get_all_products', methods=['GET'])
def get_all_products():
    pass

@app.route('/filter_products', methods=['GET'])
def filter_products():
    pass


if __name__ == "__main__":
    os.chdir("../")
    app.run(host="0.0.0.0", port=3000, use_reloader=True, debug=True, use_debugger=True)
    Models.validate_database()


