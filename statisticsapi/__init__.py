from flask import Flask
# from config import app_config
# from flask_jwt_extended import JWTManager
app = Flask(__name__)
# app.config['JWT_SECRET_KEY']='this is my secret key'
# jwt=JWTManager(app)
# from .routes import user
from .routes import associations
# from .routes import auth


