import re
# from flask_jwt_extended import (
    # JWTManager, create_access_token, jwt_required, get_jwt_identity)
from flask import request, jsonify
from statisticsapi import app
# from config import app_config
from validations import Validator
from statisticsapi.models.associations import Association
# from statisticsapi.models.user import User
import datetime


"""Endpoint for the index page"""


@app.route("/index")
@app.route("/")
def index():
    return jsonify({"message": "Welcome to statistics API"}), 200


"""
    Endpoint for creating a association
"""


@app.route("/api/v1/associations", methods=['POST'])
# @jwt_required
def create_association():
    """
        function to create a association
    """
    # userid = get_jwt_identity()
    # if not userid:
    #     return jsonify({'msg': 'Missing Authorization Header'}), 401
    
    request_data = request.get_json(force=True)
    if len(request_data.keys()) != 4:
        return jsonify({"message": "Some fields are missing"}), 400

    userId = request_data['userId']
    status = 1
    name = request_data['name']
    Location = request_data['Location']
    created_by = request_data['created_by']
    creation_date = datetime.date.today().strftime('%Y-%m-%d')
    validate_input = Validator()
    if not (validate_input.validate_string_input(name)):
        return jsonify({"message": "name Field should\
                         contain strings"}), 400
    if not (validate_input.validate_string_input(Location)):
        return jsonify({"message": "location Field should\
                         contain strings"}), 400
    # if not (validate_input.validate_string_input(userId)):
    #     return jsonify({"message": "userid Field should contain strings"}), 400
    association = Association()
    association.create_association(userId, name, Location, status,created_by,creation_date)

    return jsonify({"message": "Your association has been created","association":request_data}), 201


"""
    Endpoint for fetching all associations
"""


@app.route("/api/v1/associations", methods=['GET'])
# @jwt_required
def fetch_all_associations():
    """
        Function fetch all associations
        :return associations list:
    """
    association = Association()
    associations = association.get_all_associations()
    if associations == []:
        return jsonify({"message": "No associations found"}), 404
    return jsonify({'associations': associations}), 200
    # user = User()
    # userid = get_jwt_identity()
    # if not userid:
    #     return jsonify({'msg': 'Missing Authorization Header'}), 401
    # get_user = user.get_user_by_id(userid)
    # if not get_user:
    #     return jsonify({"message": " No user with that id"}), 404
    # if get_user['role'] == 'admin':
    #     parcel = Parcel()
    #     parcels = parcel.get_all_parcels()
    #     if parcels == []:
    #         return jsonify({"message": "No parcels found"}), 404
    #     return jsonify({'parcels': parcels}), 200

    # return jsonify({"message": "Only administrators can view parcels"}), 400


@app.route("/api/v1/associations/<int:associationId>", methods=['GET'])
# @jwt_required
def fetch_specific_association(associationId):
    """
        Function fetch specific association
        :return association:
    """
    # userId = get_jwt_identity()
    # if not userId:
    #     return({"message": "Missing authentication header"}), 401
    association = Association()
    single_association = association.get_single_association(associationId)
    if not single_association:
        return jsonify({"message": "association with that id doesnot exist"}), 404
    return jsonify({'association': single_association}), 200


@app.route("/api/v1/associations/cancel/<int:associationId>", methods=['PUT'])
# @jwt_required
def cancel_specific_association(associationId):
    """
        Function cancel association
        :return success message:
    """
    # userid = get_jwt_identity()
    association = Association()
    association_to_edit = association.get_single_association(associationId)
    
    # if not Parcel_to_edit:
    #     return jsonify({"message": " parcel doesnot exist"}), 404
    # parcel_owner_id = Parcel_to_edit['userId']
    # if parcel_owner_id != userid:
    #     return jsonify({"message": "You can only cancel an \
    #                     order you created"}), 400
    association_status = association_to_edit['status']
    if association_status == 0:
        return jsonify({"message": "Cant update an inactive association "}), 400
    association.cancel_association(associationId)
    return jsonify({"message": "Your association has been cancelled"}), 200


@app.route("/api/v1/associations/update_location/<int:associationId>", methods=['PUT'])
# @jwt_required
def update_location(associationId):
    """
        Function to update location
        :return success message:
    """
    request_data = request.get_json(force=True)
    newlocation = request_data['newlocation']
    
    # if not get_jwt_identity():
    #     return jsonify({"message": "Some fields are missing"}), 400
    if len(request_data.keys()) != 1:
        return jsonify({"message": "Some fields are missing"}), 400
    validate_input = Validator().validate_string_input(newlocation)
    if not validate_input:
        return jsonify({"message": "The new location should be a none\
                         empty string"}), 400
    # userid = get_jwt_identity()
    association = Association()
    # user = User()
    # editor = user.get_user_by_id(userid)['role']
    # if editor != 'admin':
    #     return jsonify({"message": "You can only update the present location\
    #                      if you are an admin"}), 400
    association_to_edit=association.get_single_association(associationId)
    print(association)
    if not association_to_edit or association_to_edit['status'] == 0:
        return jsonify({"message": "The association you are tring to edit doesnt\
                 exist"}), 400
    if association_to_edit['Location'] == newlocation:
        return jsonify({"message": "Present location is already upto date"}), 400
    
    association.update_location(associationId, newlocation)
    association = association.get_single_association(associationId)
    print(association)
    return jsonify({"message": "Your location has been updated ","Updated association":association}), 200


@app.route("/api/v1/associations/name/<int:associationId>", methods=['PUT'])
# @jwt_required
def update_name(associationId):
    """
        Function update name
        :return success message:
    """
    # userid = get_jwt_identity()
    association = Association()
    # user = User()
    # if not userid:
    #     return jsonify({"message": "Unauthorised access"}), 401

    # editor = user.get_user_by_id(userid)['role']
    association = association.get_single_association(associationId)
    
    if not association or association['status'] == 0:
        return jsonify({"message": "The association you are editing doesnt\
                         exist"}), 404
    # if not editor:
    #     return jsonify({"message": "You are not a registered user of the \
    #                     system"}), 401
    # if editor != 'user' or parcel['userid'] != userid:
    #     return jsonify({"message": "You can only update destination of the\
    #                      parcel you have created "}), 400
    request_data = request.get_json(force=True)
    if len(request_data.keys()) != 1:
        return jsonify({"message": "Some fields are missing"}), 400
    name = request_data['name']
    if (association['name'] == name):
        return jsonify({"message":"The name is already upto date"}),400
    validate_destination = Validator().validate_string_input(name)
    if not validate_destination:
        jsonify({"message": "name must be a non empty string"}), 400
    association = Association()
    association.update_name(associationId ,name)
    association1 = association.get_single_association(associationId)
    
    return jsonify({"message": "Your name has been updated ",
                    "updated association": association1}), 200


@app.route("/api/v1/associations/delete/<int:associationId>", methods=['PUT'])
# @jwt_required
def delete_association(associationId):
    """
        Function delete
        :return success message:
    """
    # userid = get_jwt_identity()
    # if not userid:
    #     return jsonify({"message": "unauthorised access"}), 401
    # user = User()
    association = Association()
    association_to_delete = association.get_single_association(associationId)
    if not association_to_delete or association_to_delete['status'] == 0:
        return jsonify({"message": "Order doesnt exist"}), 400

    association.delete_association(associationId)
    return jsonify({"message": "Your association has been deleted"}), 200
    # editor = user.get_user_by_id(userid)['role']
    # if editor == 'admin':
    #     parcel.delete_parcel(parcelId)
    #     return jsonify({"message": "Your parcel has been deleted"}), 200
    # return jsonify({"message": "only administrators can delete parcels"}), 400
