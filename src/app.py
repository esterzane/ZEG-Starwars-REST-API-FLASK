"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route ('/people', methods=['GET'])
def get_list_people():
    people_list = people.get_all_people()
    response_body = {
        "list_of_people": people
    }
    return jsonify(response_body), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def handle_get_single_people(people_id):
    single_people = people.get_single_people(people_id)

    if single_people is None:
        return jsonify({"error": "One single people not found"}), 404

    return jsonify(single_people), 200

@app.route ('/planets', methods=['GET'])
def get_list_planets():
    planets_list = planets.get_all_planets()
    response_body = {
        "list_of_planets": planets_list 
    }
    return jsonify(response_body), 200

@app.route('/planets/<int:planet>', methods=['GET'])
def handle_get_one_planet(planet_id):
    one_planet = planets.get_one_planet(planet_id)

    if one_planet is None:
        return jsonify({"error": "The people you look for is not found"}), 404

    return jsonify(one_planet), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
