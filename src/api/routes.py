"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required  
from api.models import db, User
from api.utils import generate_sitemap, APIException
from passlib.hash import bcrypt_sha256

api = Blueprint('api', __name__)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route("/signup", methods=["POST"])
def create_users():
    user_data = request.get_json(silent=True)

    if user_data is None: 
        return jsonify({
            "message": "No Data Provided"
        }), 400
    
    if "email" not in user_data or "password" not in user_data:
        return jsonify({
            "message": "email and password requiered"
        }), 400
    
    user = User.query.filter_by(email=user_data["email"]).one_or_none()
    
    if user:
        return jsonify({
            "message": "User already exist"
        }), 400
    password_hash = bcrypt_sha256.hash(user_data["password"])
    email = user_data["email"]
    
    user = User()
    user.email = email
    user.password = password_hash
    user.is_active = True

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as error:
        print("Este es el error: ", error)
        print("Tipo de error: ", type(error))
        print("Args del error: ", error.args)
        db.session.rollback()
        return jsonify({
            "message": "DB ERROR"
        }), 500
    
    return jsonify({"message": "User Created"}), 201

@api.route("/login", methods=["POST"])
def login():
    user_data = request.get_json(silent=True)

    if user_data is None: 
        return jsonify({
            "message": "email and password requiered"
        }), 400
    
    if "email" not in user_data or "password" not in user_data:
        return jsonify({
            "message": "email and password requiered"
        }), 400
    
    email = user_data.get("email")
    password = user_data.get("password")
    user = User.query.filter_by(email=email).one_or_none()
    
    if user is None:
        return jsonify({
            "message": "User not found"
        }), 404
    
    # password_is_valid = password == user.password 
    password_is_valid = bcrypt_sha256.verify(password, user.password)

    if not password_is_valid:
        return jsonify({
            "message": "Invalid credential"
         }), 400
        
    access_token = create_access_token(identity = user.id)

    return jsonify({
        "token": access_token
    }), 201


@api.route("/user", methods=["GET"])
@jwt_required()
def get_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify(user.serialize()), 200