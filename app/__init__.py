import os
from flask import Flask
from app.routes.api import bp as api_blueprint
from app.routes.auth import bp as auth_blueprint
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

load_dotenv()

db_uri = os.getenv("DB_URI")

jwt_secret = os.getenv("JWT_SECRET")

admin_username = os.getenv("ADMIN_USERNAME")
admin_password = os.getenv("ADMIN_PASSWORD")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = jwt_secret
jwt = JWTManager(app)


app.register_blueprint(api_blueprint, url_prefix="/api")
app.register_blueprint(auth_blueprint, url_prefix="/auth")
