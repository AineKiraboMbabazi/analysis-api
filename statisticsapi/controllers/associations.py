import datetime
import pymysql
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity)
from flask import request, jsonify
from validations import Validator
from ..models.associations import Association
from .database import DatabaseConnection
con = DatabaseConnection()


class Association_Controller:
    def index():
        """
            controller for the index page

        """

        return jsonify({"message": "Welcome to statistics API"}), 200      
    
    def create_association():
        """
            function to create a association
        """
        current_user = get_jwt_identity()
        if not current_user:
            return jsonify({'message': 'Missing token in the Authorization Header'}), 401
        request_data = request.get_json(force=True)
        if len(request_data.keys()) != 2:
            return jsonify({"message": "Some fields are missing"}), 400

        
        user = con.get_single_user(current_user)
        userId = current_user
        if user['status'] == 0:
            return jsonify({"message": "The user id you are using doesnot exist"}), 400
            
        role = user['user_role']
        if role == 'superadmin':
            status = 'active'

        status = 'pending'
        creation_date = datetime.date.today().strftime('%Y-%m-%d')
        name = request_data['name']
        Location = request_data['Location']
        created_by = user['name']
        validate_input = Validator()
        if not (validate_input.validate_string_input(name)):
            return jsonify({"message": "name Field should\
                            contain strings "}), 400

        if not (validate_input.validate_string_input(Location)):
            return jsonify({"message": "location Field should\
                            contain strings "}), 400  
                            
        association = con.fetch_associations_by_name(name)
        if association:
            return jsonify({"message":"An association with that name already exists"}),400
        
        association = Association(userId, name, Location, status, created_by, creation_date).__dict__
        con.create_association(association['userId'], association['name'], association['Location'], association['status'],association['created_by'],association['creation_date'])
        return jsonify({"message": "Your association has been created","association":request_data}), 201

    def fetch_all_associations():
        """
            Function fetch all associations
            :return associations list:
        """
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'message': 'Missing token in the Authorization Header'}), 401
        User = con.get_single_user(current_user_id)
        role = User['user_role']
        user_group = User['user_group']
        country = User['country']
        
        if  role == 'superadmin':
            associations = con.get_all_associations()
            if associations == []:
                return jsonify({"message": "No associations found"}), 404
            return jsonify({'associations': associations}), 200  
        if user_group == 'government':
            print(country)
            associations = con.fetch_associations_in_country(country)
            print(associations)
            if associations == []:
                return jsonify({"message": "No associations found"}), 404
            return jsonify({'associations': associations}), 200  
            
        return jsonify({"message":"You are not authorised to fetch all associations"}),400

    def fetch_pending_association():
        """
            Function fetch pending association
            :return association:
        """
        current_user_id = get_jwt_identity()
        print(current_user_id)
        user = con.get_single_user(current_user_id)
        print(user)
        user_role = user['user_role']

        if user_role == 'superadmin':
            associations = con.fetch_pending_association()
            if  associations == []:
                return jsonify({"message": "No pending associations found "}), 404

            return jsonify({'association': associations}), 200
        return jsonify({"message":"you are not allowed to access pending orders"}),400

    

    def fetch_specific_association(associationId):
        """
            Function fetch specific association
            :return association:
        """

        single_association = con.get_single_association(associationId)
        if not single_association:
            return jsonify({"message": "association with that id doesnot exist"}), 404
        return jsonify({'association': single_association}), 200


    def cancel_specific_association(associationId):
        """
            Function cancel association
            :return success message:
        """
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'message': 'Missing token in the Authorization Header'}), 401

        association_to_edit = con.get_single_association(associationId)
        association_status = association_to_edit['status']
        if association_status == 0:
            return jsonify({"message": "Cant update an inactive association "}), 400
 
        User = con.get_single_user(current_user_id)
        role = User['role']
        if role == 'superadmin':
            con.cancel_association(associationId)
            return jsonify({"message": "Your association has been cancelled"}), 200

        return jsonify({"message": "You are not allowed to cancel an association "}), 400           

    def update_location(associationId):
        """
            Function to update location
            :return success message:
        """

        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'message': 'Missing token in the Authorization Header'}), 401

        User = con.get_single_user(current_user_id)
        role = User['role']
        
        request_data = request.get_json(force=True)

        newlocation = request_data['newlocation']
        if len(request_data.keys()) != 1:
            return jsonify({"message": "Some fields are missing"}), 400

        validate_input = Validator().validate_string_input(newlocation)
        if not validate_input:
            return jsonify({"message": "The new location should be a none\
                            empty string "}), 400
                            
        association_to_edit=con.get_single_association(associationId)
        
        if not association_to_edit or association_to_edit['status'] == 0:
            return jsonify({"message": "The association you are tring to edit doesnt\
                    exist "}), 400
                    
        if association_to_edit['Location'] == newlocation:
            return jsonify({"message": "Present location is already upto date"}), 400
        
        if  role == 'superadmin' or associations['userId'] == current_user_id:
            con.update_location(associationId, newlocation)
            association = con.get_single_association(associationId)
            return jsonify({"message": "Your location has been updated ", "Updated association": association}), 200
        return jsonify({"message": "You are not allowed to change association location"}),400
        
    def update_name(associationId):
        """
            Function update name
            :return success message:
        """
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'message': 'Missing token in the Authorization Header'}), 401

        User = con.get_single_user(current_user_id)
        role = User['role']

        association = con.get_single_association(associationId)
        
        if not association or association['status'] == 0:
            return jsonify({"message": "The association you are editing doesnt\
                            exist "}), 404
                            
        request_data = request.get_json(force=True)
        if len(request_data.keys()) != 1:
            return jsonify({"message": "Some fields are missing"}), 400

        name = request_data['name']
        if (association['name'] == name):
            return jsonify({"message": "The name is already upto date"}), 400
            
        validate_name = Validator().validate_string_input(name)
        if not validate_name:
            jsonify({"message": "name must be a non empty string"}), 400

        if  role == 'superadmin' or associations['userId'] == current_user_id:
            con.update_name(associationId ,name)
            association1 = con.get_single_association(associationId)
            return jsonify({"message": "Your name has been updated ",
                        "updated association": association1}), 200

        return jsonify({"message": "You dont have the necessary credentials to edit the name"}), 400

    def delete_association(associationId):
        """
            Function delete
            :return success message:
        """
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'message': 'Missing token in the Authorization Header'}), 401

        association_to_edit = con.get_single_association(associationId)
        association_status = association_to_edit['status']
        if association_status == 0:
            return jsonify({"message": "Cant update an inactive association "}), 400
 
        User = con.get_single_user(current_user_id)
        role = User['role']
        if role == 'superadmin':
            con.delete_association(associationId)
            return jsonify({"message": "Your association has been deleted"}), 200

        return jsonify({"message": "You dont have the necessary credentials to delete an association"}), 400
        

    def approve_association(associationId):
        """

            Function to approve association
            :param associationId:
            :return success message:
        """
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'message': 'Missing token in the Authorization Header'}), 401

        association_to_approve = con.get_single_association(associationId)
        if not association_to_approve or association_to_approve['status'] == 0:
            return jsonify({"message": "The association you are trying to approve doesnt exist"}), 404

        if association_to_approve['status'] == 'approved':
            return jsonify({"message": "The association is all ready approved"}), 400

        user = con.get_single_user(current_user_id)
        if user['role'] == 'superadmin':
            con.approve_association(associationId)
            return jsonify({"message": "The association has been approved"}), 200

        return jsonify({"message": "you donot have the authorisation to approve the account"}), 400