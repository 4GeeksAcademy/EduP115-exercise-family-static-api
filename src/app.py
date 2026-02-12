"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_hello():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {"hello": "world",
                     "family": members}
    return jsonify(response_body), 200


# Ruta para el metodo post
@app.route('/members', methods=['POST'])
def add_members():
    data = request.get_json()
    new_member = jackson_family.add_member(data)

    if new_member is True:
        return jsonify({'code': 'realizado con exito'}), 200
    elif new_member is False:
        return jsonify({'code': 'error por parte del cliente'}), 400
    else:
        return jsonify({'code': 'error en el servidor'}), 500


# Ruta para el metodo delete
@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    result = jackson_family.delete_member(id)

    if result is True:
        return jsonify({"done": True}), 200
    elif result is False:
        return jsonify({"done": False, "error": "Miembro no encontrado"}), 404
    else:
        return jsonify({"done": False, "error": "Error interno del servidor"}), 400


# Ruta para el metodo Get_id
@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    result = jackson_family.get_member(id)
    
    if result is False:
        return jsonify({"error": "Miembro no encontrado"}), 404
    elif result is None:
        return jsonify({"error": "Error interno del servidor"}), 500
    else:
        return jsonify({
            "id": result["id"],
            "first_name": result["first_name"],
            "age": result["age"],
            "lucky_numbers": result["lucky_numbers"]
        }), 200


# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)