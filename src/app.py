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
    return jsonify(members), 200

                # miembro por id
@app.route('/members/<int:id>', methods=['GET'])
def get_single_member(id):
    member = jackson_family.get_member(id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"message": "Member not found"}), 404




@app.route('/members', methods=['POST'])
def handle_post():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Invalid JSON"}), 400
    
    # Validate required fields
    if "first_name" not in data or not isinstance(data["first_name"], str) or not data["first_name"].strip():
        return jsonify({"message": "first_name is required and must be a non-empty string"}), 400
    
    if "age" not in data or not isinstance(data["age"], int) or data["age"] <= 0:
        return jsonify({"message": "age is required and must be a positive integer"}), 400
    
    if "lucky_numbers" not in data or not isinstance(data["lucky_numbers"], list) or not all(isinstance(num, int) for num in data["lucky_numbers"]):
        return jsonify({"message": "lucky_numbers is required and must be a list of integers"}), 400
    
    new_member = jackson_family.add_member(data) 
    return jsonify(new_member), 200


@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    success = jackson_family.delete_member(id)
    if success:
        return jsonify({"done": True}), 200
    else:
        return jsonify({"message": "Member not found"}), 404


# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)