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
            controller to create a association

            :return object of created association:
        """

        current_user = get_jwt_identity()

        request_data = request.get_json(force=True)

        if len(request_data.keys()) != 2:
            return jsonify({"message": "Some fields are missing"}), 400

        
        user = con.get_single_user(current_user)
        userId = current_user
        status  = user['status']
        
        if  status == 0 or status == '0':
            return jsonify({"message": "The user account has been deactivated"}), 400
            
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
            return jsonify({"message": "Name field should contain strings "}), 400

        if not (validate_input.validate_string_input(Location)):
            return jsonify({"message": "location Field should contain strings "}), 400 
                            
        association=con.fetch_associations_by_name(name)
        
        if association:
            return jsonify({"message":"An association with that name already exists"}),400
        
        association = Association(userId, name, Location, status, created_by, creation_date).__dict__

        con.create_association(association['userId'], association['name'], association['Location'], association['status'], association['created_by'], association['creation_date'])
        
        return jsonify({"message": "Your association has been created","association":request_data}), 201

    def fetch_all_associations():
        """
            controller fetch all associations
            :return associations list:
        """

        current_user_id = get_jwt_identity()

        User = con.get_single_user(current_user_id)
        
        role = User['user_role']
        user_group = User['user_group']
        country = User['country']

        associations = con.get_all_associations()
     
        
        if role == 'superadmin':
            if len (associations) == 0 or associations == None or associations == []:
                return jsonify({"message": "No associations found"}), 404
        
            return jsonify({'associations' :associations}), 200
       
        if user_group == 'government':
            if len (associations) == 0 or associations == None or associations == []:
                return jsonify({"message": "No associations found"}), 404
        
            return jsonify({'associations': associations}), 200  
            
        
        return jsonify({"message":"Unauthorised access"}),400

    def fetch_pending_association():
        """
            controller fetch pending association
            :return association:
        """

        current_user_id = get_jwt_identity()
        
        user = con.get_single_user(current_user_id)
        
        if user['status'] == 0 or user['status'] == '0':
            return jsonify({"message":"Trying to edit association using a deactivated account"}),400
        
        user_role = user['user_role']

        associations = con.fetch_pending_association()

        if user_role == 'superadmin':
            if  len (associations) == 0 or associations == None or associations == []:
                return jsonify({"message": "No pending associations found "}), 404

            return jsonify({'associations': associations}), 200

        return jsonify({"message":"Unauthorised access"}),400

    

    def fetch_specific_association(associationId):
        """
            controller fetch specific association
            :return association:
        """

        single_association = con.get_single_association(associationId)
        if not single_association or single_association == [] or len(single_association) == 0:
            return jsonify({"message": "association with that id doesnot exist"}), 404

        return jsonify({'association': single_association}), 200


    def cancel_specific_association(associationId):
        """
            controller cancel association
            :return success message:
        """

        current_user_id = get_jwt_identity()

        association_to_edit = con.get_single_association(associationId)
        if not association_to_edit or association_to_edit == []:
            return jsonify({"message": "Association with that id doesnt exist"}), 404

        if association_to_edit['status'] == '0':
            return jsonify({"message": "Cant update an inactive association "}), 400
 
        User = con.get_single_user(current_user_id)
        role = User['user_role']
        if User['status'] == 0 or User['status'] == '0':
            return jsonify({"message":"Trying to edit association using a deactivated account"}),400

        if role == 'superadmin':
            con.cancel_association(associationId)
            return jsonify({"message": "Your association has been cancelled"}), 200

        return jsonify({"message": "unauthorised access"}), 400           

    # def update_location(associationId):
    #     """
    #         Function to update location
    #         :param associationid:
    #         :return success message:
    #     """

    #     current_user_id = get_jwt_identity()

    #     if not current_user_id:
    #         return jsonify({'message': 'Missing token in the Authorization Header'}), 401

    #     User = con.get_single_user(current_user_id)
    #     if User['status'] == 0:
    #         return jsonify({"message":"Trying to edit association using a deactivated account"}),400
        
    #     role = User['user_role']
        
    #     request_data = request.get_json(force=True)

    #     newlocation = request_data['newlocation']

    #     if len(request_data.keys()) != 1:
    #         return jsonify({"message": "Some fields are missing"}), 400

    #     validate_input = Validator().validate_string_input(newlocation)

    #     if not validate_input:
    #         return jsonify({"message": "The new location should be a none\
    #                         empty string "}), 400
                            
    #     association_to_edit=con.get_single_association(associationId)
        
    #     if not association_to_edit or association_to_edit['status'] == 0:
    #         return jsonify({"message": "The association you are tring to edit doesnt\
    #                 exist "}), 400
                    
    #     if association_to_edit['Location'] == newlocation:
    #         return jsonify({"message": "Present location is already upto date"}), 400
        
    #     if  role == 'superadmin' or associations['userId'] == current_user_id:
    #         con.update_location(associationId, newlocation)
    #         association = con.get_single_association(associationId)
    #         return jsonify({"message": "Your location has been updated ", "Updated association": association}), 200

    #     return jsonify({"message": "You are not allowed to change association location"}),400
        
    def update_name(associationId):
        """
            Function update name
            :param associationid:
            :return success message:
        """

        current_user_id = get_jwt_identity()

        User = con.get_single_user(current_user_id)
        if User == []:
            return jsonify({"message": "User not found"}), 404
            
        if User['status'] == 0 or User['status'] == '0':
            return jsonify({"message": "user account inactive"}), 400
            
        role = User['user_role']

        association = con.get_single_association(associationId)
        if association == [] or not association or association['status'] == 0:
            return jsonify({"message": "association not found"}), 404

                            
        request_data=request.get_json(force=True)
        
        if len(request_data.keys()) != 1:
            return jsonify({"message": "Some fields are missing"}), 400

        name = request_data['name']

        if (association['name'] == name):
            return jsonify({"message": "The name is already upto date"}), 400
            
        validate_name = Validator().validate_string_input(name)

        if not validate_name:
            return jsonify({"message": "name must be a non empty string"}), 400

        if association['userId'] == current_user_id or role == 'superadmin':
            con.update_association_name(associationId,name)
            association1 = con.get_single_association(associationId)
            return jsonify({"message": "Your name has been updated ",
                        "updated association": association1}), 200

        return jsonify({"message": "unauthorised access"}), 400

    def delete_association(associationId):
        """
            controller to delete
            :param associationid:
            :return success message:
        """

        current_user_id = get_jwt_identity()

        association_to_edit = con.get_single_association(associationId)
        if not association_to_edit:
            return jsonify({"message": "The association doesnt exist"}), 404
            
        association_status = association_to_edit['status']

        if association_status == '0':
            return jsonify({"message": "Cant update an inactive association "}), 400
 
        User = con.get_single_user(current_user_id)
        if User['status'] == 0 or User == None or User['status'] == '0':
            return jsonify({"message":"user with id not found"}),404
        role = User['user_role']

        if role == 'superadmin':
            con.delete_association(associationId)
            return jsonify({"message": "Your association has been deleted"}), 200

        return jsonify({"message": "unauthorised access"}), 400
        

    def approve_association(associationId):
        """

            Function to approve association
            :param associationId:
            :return success message:
        """

        current_user_id = get_jwt_identity()

        association_to_approve = con.get_single_association(associationId)

        if not association_to_approve or association_to_approve['status'] == '0':
            return jsonify({"message": "The association you are trying to approve doesnt exist"}), 404

        if association_to_approve['status'] == 'approved':
            return jsonify({"message": "The association is already approved"}), 400

        user = con.get_single_user(current_user_id)

        if user['user_role'] == 'superadmin':
            con.approve_association(associationId)
            return jsonify({"message": "The association has been approved"}), 200

        return jsonify({"message": "unauthorised access"}), 400
        