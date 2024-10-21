from flask import Flask, request, jsonify, send_from_directory
from service import BeerService
from models import Schema
import logging

app = Flask(__name__, static_url_path='', static_folder='.')

beer_service = BeerService()

logging.basicConfig(level=logging.DEBUG)

@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['Access-Control-Allow-Headers'] = "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods'] = "POST, GET, PUT, DELETE, OPTIONS"
    return response

@app.route("/")
def index():
    return send_from_directory('', 'index.html')

@app.route("/locations")
def locations_page():
    return send_from_directory('', 'locations.html')

@app.route("/beers")
def beers_page():
    return send_from_directory('', 'beers.html')

@app.route("/drink")
def drink_page():
    return send_from_directory('', 'drink.html')

@app.route("/location", methods=["POST"])
def add_location():
    return jsonify(beer_service.add_location(request.get_json()))

@app.route("/location/<location_name>", methods=["DELETE"])
def remove_location(location_name):
    return jsonify(beer_service.remove_location(location_name))

@app.route("/location-list", methods=["GET"])
def get_locations():
    return jsonify(beer_service.get_locations())

@app.route("/location/<location_name>/beers", methods=["GET"])
def get_beers_for_location(location_name):
    return jsonify(beer_service.get_beers_for_location(location_name))

@app.route("/beer", methods=["POST"])
def add_beer():
    return jsonify(beer_service.add_beer(request.get_json()))

@app.route("/inventory", methods=["POST"])
def add_inventory():
    return jsonify(beer_service.add_inventory(request.get_json()))

@app.route("/beer/<beer_name>/<brewery>/locations", methods=["GET"])
def get_locations_for_beer(beer_name, brewery):
    return jsonify(beer_service.get_locations_for_beer(beer_name, brewery))

@app.route("/beer/<beer_name>/<brewery>/inventory", methods=["GET"])
def get_inventory_for_beer(beer_name, brewery):
    return jsonify(beer_service.get_inventory_for_beer(beer_name, brewery))

@app.route("/beer/<beer_name>/<brewery>/sizes", methods=["GET"])
def get_sizes_for_beer(beer_name, brewery):
    return jsonify(beer_service.get_sizes_for_beer(beer_name, brewery))

@app.route("/beer-list", methods=["GET"])
def get_beer_list():
    return jsonify(beer_service.get_beer_list())

@app.route("/drink", methods=["POST"])
def drink_beer():
    data = request.get_json()
    return jsonify(beer_service.drink_beer(data['beerName'], data['brewery'], data['locationName'], data['size']))

if __name__ == "__main__":
    Schema()
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=False)