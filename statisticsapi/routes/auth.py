import re
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity)
from flask import request, jsonify,jsonify
from statisticsapi import app
from config import app_config
from validations import Validator
from statisticsapi.models.users import User
from ..controllers.users import User_Controller
from ..controllers.auth import Auth
from ..controllers.database import DatabaseConnection
con = DatabaseConnection()
# from statisticsapi.models.user import User
import datetime

"""
    Endpoint for signing up a user
"""
@app.route('/api/v1/auth/signup', methods=['POST'])
def signup():
    return Auth.create_user()

"""
    Endpoint for logging in a user
"""
@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    return Auth.login()

"""
    Endpoint for changing the password
"""
@app.route('/api/v1/auth/forgot_password', methods=['POST'])
def recover_password():
    return Auth.recover_password()

"""
    Endpoint for logging out a user
"""
@app.route('/api/v1/auth/logout', methods=['POST'])
def logout():
    Auth.logout()