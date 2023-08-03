from flask import Blueprint, request, jsonify
from app.models import Admin
from flask_jwt_extended import create_access_token

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    user = Admin.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token}), 200
