import re
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity)
from flask import request, jsonify,jsonify
from statisticsapi import app
from config import app_config
from validations import Validator
from statisticsapi.models.users import User
from ..controllers.users import User_Controller
from ..controllers.database import DatabaseConnection
con = DatabaseConnection()
# from statisticsapi.models.user import User
import datetime


"""
    Endpoint for fetching all users
"""


@app.route("/api/v1/users", methods=['GET'])
@jwt_required
def fetch_all_users():
    """
        Function fetch all users
        :return user list:
    """
    return User_Controller.fetch_all_users()



@app.route("/api/v1/users/<int:userId>", methods=['GET'])
@jwt_required
def fetch_specific_user(userId):
    """
        Function fetch specific user
        :return user:
    """

    return User_Controller.fetch_specific_user(userId)
    
@app.route("/api/v1/users/cancel/<int:userId>", methods=['PUT'])
@jwt_required
def cancel_specific_user(userId):
    """
        Function cancel user
        :return success message:
    """

    return User_Controller.cancel_specific_user(userId)
    
@app.route("/api/v1/users/name/<int:userId>", methods=['PUT'])
@jwt_required
def update_user_name(userId):
    """
        Function update name
        :return success message:
    """

    return User_Controller.update_user_name(userId)
    

@app.route("/api/v1/users/user_role/<int:userId>", methods=['PUT'])
@jwt_required
def update_userrole(userId):
    """
        Function delete
        :return success message:
    """

    return User_Controller.update_user_role(userId)
    

@app.route("/api/v1/users/delete/<int:userId>", methods=['PUT'])
@jwt_required
def delete_user(userId):
    """
        Function delete
        :return success message:
    """
    
    return User_Controller.delete_user(userId)

@app.route("/api/v1/users/pending", methods=['GET'])
@jwt_required
def fetch_pending_accounts():
    """
        Function fetch all users whose accounts are pending
        :return user list:
    """

    return User_Controller.fetch_pending_accounts()
    