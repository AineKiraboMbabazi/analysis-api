import re
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity)
from flask import request, jsonify
from statisticsapi import app
# from config import app_config
from validations import Validator
from statisticsapi.models.government import Government
from ..controllers.government import Government_Controller
from ..controllers.database import DatabaseConnection
con = DatabaseConnection()
# from statisticsapi.models.user import User
import datetime

"""
    Endpoint for creating a government
"""


@app.route("/api/v1/governments/sendmail/<toaddress>/<link>", methods=['GET'])

def sendmail():
    """
        function to create a government
    """
    
    return Government_Controller.sendmail(toaddress,link)

"""
    Endpoint for fetching all governments
"""
@app.route("/api/v1/governments/sendmail", methods=['POST'])

def create_government():
    """
        function to create a government
    """
    
    return Government_Controller.create_government()

"""
    Endpoint for fetching all governments
"""


@app.route("/api/v1/governments", methods=['GET'])
@jwt_required
def fetch_all_governments():
    """
        Function fetch all governments'}), 401
    return Government_Controller.approve_government(governmentId)

        :return governments list:
    """

    return Government_Controller.fetch_all_governments()
    

@app.route("/api/v1/governments/<int:governmentId>", methods=['GET'])
# @jwt_required
def fetch_specific_government(governmentId):
    """
        Function fetch specific government
        :return government:
    """
    
    return Government_Controller.fetch_specific_government(governmentId)




@app.route("/api/v1/governments/cancel/<int:governmentId>", methods=['PUT'])
@jwt_required
def cancel_specific_government(governmentId):
    """
        Function cancel government
        :return success message:
    """
    
    return Government_Controller.cancel_specific_government(governmentId)

@app.route("/api/v1/governments/photo/<int:governmentId>", methods=['PUT'])
@jwt_required
def update_location(governmentId):
    """
        Function to update location
        :return success message:
    """
    return Government_Controller.update_photo(governmentId)


@app.route("/api/v1/governments/name/<int:governmentId>", methods=['PUT'])
@jwt_required
def update_government_name(governmentId):
    """
        Function update name
        :return success message:
    """
    return Government_Controller.update_name(governmentId)


@app.route("/api/v1/governments/delete/<int:governmentId>", methods=['PUT'])
@jwt_required
def delete_government(governmentId):
    """
        Function delete
        :return success message:
    """
    return Government_Controller.delete_government(governmentId)