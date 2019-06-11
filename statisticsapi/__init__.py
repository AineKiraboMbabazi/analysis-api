from flask import Flask
from config import app_config
from flask_jwt_extended import JWTManager
from flask_cors import CORS
app = Flask(__name__)
app.config['JWT_SECRET_KEY']='this is my secret key'
cors = CORS(app, resources={r"/*": {"origins": "*"}})
jwt = JWTManager(app)
from .routes import auth
from .routes import users
from .routes import associations
from .routes import government



