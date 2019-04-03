import re
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity)
from flask import request, jsonify
from statisticsapi import app
# from config import app_config
from validations import Validator
from statisticsapi.models.associations import Association
from ..controllers.associations import Association_Controller
from ..controllers.database import DatabaseConnection
con = DatabaseConnection()
# from statisticsapi.models.user import User
import datetime


"""Endpoint for the index page"""


@app.route("/index")
@app.route("/")
def index():
    return Association_Controller.index()


"""
    Endpoint for creating a association
"""


@app.route("/api/v1/associations", methods=['POST'])
@jwt_required
def create_association():
    """
        function to create a association
    """
    
    return Association_Controller.create_association()

"""
    Endpoint for fetching all associations
"""


@app.route("/api/v1/associations", methods=['GET'])
@jwt_required
def fetch_all_associations():
    """
        Function fetch all associations'}), 401
    return Association_Controller.approve_association(associationId)

        :return associations list:
    """

    return Association_Controller.fetch_all_associations()
    

@app.route("/api/v1/associations/<int:associationId>", methods=['GET'])
# @jwt_required
def fetch_specific_association(associationId):
    """
        Function fetch specific association
        :return association:
    """
    
    return Association_Controller.fetch_specific_association(associationId)

@app.route("/api/v1/associations/pending", methods=['GET'])
@jwt_required
def pending():
    """
        Function fetch pending association
        :return association:
    """
    
    return Association_Controller.fetch_pending_association()

@app.route("/api/v1/associations/approve/<int:associationId>", methods=['POST'])
@jwt_required
def approve_association(associationId):
    """
        Function approve specific association
        :return association:
    """

    
    return Association_Controller.approve_association(associationId)


@app.route("/api/v1/associations/cancel/<int:associationId>", methods=['PUT'])
@jwt_required
def cancel_specific_association(associationId):
    """
        Function cancel association
        :return success message:
    """
    
    return Association_Controller.cancel_specific_association(associationId)

@app.route("/api/v1/associations/update_location/<int:associationId>", methods=['PUT'])
@jwt_required
def update_location(associationId):
    """
        Function to update location
        :return success message:
    """
    return Association_Controller.update_location(associationId)


@app.route("/api/v1/associations/name/<int:associationId>", methods=['PUT'])
@jwt_required
def update_name(associationId):
    """
        Function update name
        :return success message:
    """
    return Association_Controller.update_name(associationId)


@app.route("/api/v1/associations/delete/<int:associationId>", methods=['PUT'])
@jwt_required
def delete_association(associationId):
    """
        Function delete
        :return success message:
    """
    return Association_Controller.delete_association(associationId)