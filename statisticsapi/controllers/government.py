import datetime
import pymysql
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity)
from flask import request, jsonify
from validations import Validator
from ..models.government import Government
from .database import DatabaseConnection
con = DatabaseConnection()


class Government_Controller:

    
    def create_government():
        """
            controller to create a government

            :return object of created government:
        """

        current_user = get_jwt_identity()

        request_data = request.get_json(force=True)

        if len(request_data.keys()) != 2:
            return jsonify({"message": "Some fields are missing"}), 400

        
        user = con.get_single_user(current_user)
        
        userId = current_user
        
        if user['status'] == 0 or user['status'] == '0':
            return jsonify({"message": "User account has been deactivated"}), 400
            
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
            return jsonify({"message": "Location field should contain strings "}), 400 
                            
        government=con.fetch_governments_by_name(name)
        
        if government:
            return jsonify({"message":"A government with that name already exists"}), 400
        
        government = Government(userId, name, Location, status, created_by, creation_date).__dict__

        con.create_government(government['userId'], government['name'], government['Location'], government['status'], government['created_by'], government['creation_date'])
        
        return jsonify({"message": "Your government has been created", "government":request_data}), 201

    def fetch_all_governments():
        """
            controller fetch all governments
            :return governments list:
        """

        current_user_id = get_jwt_identity()

        User = con.get_single_user(current_user_id)
        
        role = User['user_role']
        user_group = User['user_group']
        country = User['country']
        
        if  role == 'superadmin':
            governments = con.get_all_governments()

            if governments == [] or len(governments) ==0:
                return jsonify({"message": "No governments found"}), 404

            return jsonify({'governments': governments}), 200
            
        
        return jsonify({"message":"Unauthorised access"}),400

    def fetch_pending_government():
        """
            controller fetch pending government
            :return government:
        """

        current_user_id = get_jwt_identity()
        
        user = con.get_single_user(current_user_id)
        user_role = user['user_role']

        if user['status'] == 0 or user['status'] == '0':
            return jsonify({"message": "Trying to edit government using a deactivated account"}), 400
            
        if user_role == 'superadmin':
            governments = con.fetch_pending_government()

            if  len(governments) == 0 or governments == []:
                return jsonify({"message": "No pending governments found "}), 404

            return jsonify({'government': governments}), 200

        return jsonify({"message":"Unauthorised access"}),400

    

    def fetch_specific_government(governmentId):
        """
            controller fetch specific government
            :return government:
        """

        single_government = con.get_single_government(governmentId)
        if not single_government:
            return jsonify({"message": "government with that id doesnot exist"}), 404
        return jsonify({'government': single_government}), 200


    def cancel_specific_government(governmentId):
        """
            controller cancel government
            :return success message:
        """

        current_user_id = get_jwt_identity()

        government_to_edit = con.get_single_government(governmentId)
        

        if government_to_edit == None :
            return jsonify({"message": "Cant update nonexistent government "}), 400
        
        if government_to_edit['status'] == '0':
            return jsonify({"message":"Cant update an inactive government "}),400
 
        User = con.get_single_user(current_user_id)
        role = User['user_role']
       
        if User['status'] == 0 or User['status'] == '0':
            return jsonify({"message": "Trying to edit government using a deactivated account"}), 400
            
        if role == 'superadmin':
            con.cancel_government(governmentId)
            return jsonify({"message": "Your government has been cancelled"}), 200

        return jsonify({"message": "You are not allowed to cancel an government "}), 400           

    # def update_location(governmentId):
    #     """
    #         Function to update location
    #         :param governmentid:
    #         :return success message:
    #     """

    #     current_user_id = get_jwt_identity()

    #     if not current_user_id:
    #         return jsonify({'message': 'Missing token in the Authorization Header'}), 401

    #     User = con.get_single_user(current_user_id)
    #     role = User['role']
        
    #     request_data = request.get_json(force=True)

    #     newlocation = request_data['newlocation']

    #     if len(request_data.keys()) != 1:
    #         return jsonify({"message": "Some fields are missing"}), 400

    #     validate_input = Validator().validate_string_input(newlocation)

    #     if not validate_input:
    #         return jsonify({"message": "The new location should be a none\
    #                         empty string "}), 400
                            
    #     government_to_edit=con.get_single_government(governmentId)
        
    #     if not government_to_edit or government_to_edit['status'] == 0:
    #         return jsonify({"message": "The government you are tring to edit doesnt\
    #                 exist "}), 400
                    
    #     if government_to_edit['Location'] == newlocation:
    #         return jsonify({"message": "Present location is already upto date"}), 400
        
    #     if  role == 'superadmin' or governments['userId'] == current_user_id:
    #         con.update_location(governmentId, newlocation)
    #         government = con.get_single_government(governmentId)
    #         return jsonify({"message": "Your location has been updated ", "Updated government": government}), 200

    #     return jsonify({"message": "You are not allowed to change government location"}),400
        
    def update_name(governmentId):
        """
            Function update name
            :param governmentid:
            :return success message:
        """

        current_user_id = get_jwt_identity()

        if not current_user_id:
            return jsonify({'message': 'Missing token in the Authorization Header'}), 401

        User = con.get_single_user(current_user_id)
        role = User['user_role']
        if User['status'] == 0 or User['status'] == '0':
            return jsonify({"message": "user account inactive"}), 400
            
        government = con.get_single_government(governmentId)
        
        if not government or government['status'] == 0:
            return jsonify({"message": "Government not found"}), 404
                            
        request_data=request.get_json(force=True)
        
        if len(request_data.keys()) != 1:
            return jsonify({"message": "Some fields are missing"}), 400

        name = request_data['name']

        if (government['name'] == name):
            return jsonify({"message": "The name is already upto date"}), 400
            
        validate_name = Validator().validate_string_input(name)

        if not validate_name:
            return jsonify({"message": "name must be a non empty string"}), 400

        if  role == 'superadmin' or government['userId'] == current_user_id:
            con.update_name(governmentId ,name)
            government1 = con.get_single_government(governmentId)
            return jsonify({"message": "Your name has been updated ",
                        "updated government": government1}), 200

        return jsonify({"message": "unauthorised access"}), 400

    def delete_government(governmentId):
        """
            controller to delete
            :param governmentid:
            :return success message:
        """

        current_user_id = get_jwt_identity()

        government_to_edit = con.get_single_government(governmentId)
        if government_to_edit == None:
            return jsonify({"message": "The government doesnt exist"}), 400
            
        government_status = government_to_edit['status']
        
        if government_status == '0':
            return jsonify({"message": "Cant update an inactive government "}), 400
 
        User = con.get_single_user(current_user_id)
        if User['status'] == 0 or User['status'] == '0':
            return jsonify({"message": "user with id not found"}), 404
            
        role = User['user_role']

        if role == 'superadmin':
            con.delete_government(governmentId)
            return jsonify({"message": "Your government has been deleted"}), 200

        return jsonify({"message": "unauthorised access"}), 400
        

    def approve_government(governmentId):
        """

            Function to approve government
            :param governmentId:
            :return success message:
        """

        current_user_id = get_jwt_identity()

        government_to_approve = con.get_single_government(governmentId)

        if not government_to_approve or government_to_approve['status'] == 0:
            return jsonify({"message": "The government you are trying to approve doesnt exist"}), 404

        if government_to_approve['status'] == 'approved':
            return jsonify({"message": "The government is already approved"}), 400

        user = con.get_single_user(current_user_id)

        if user['user_role'] == 'superadmin':
            con.approve_government(governmentId)
            return jsonify({"message": "The government has been approved"}), 200

        return jsonify({"message": "unauthorised access"}), 400