import datetime
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity)
import pymysql
from flask import request, jsonify
from validations import Validator
from ..models.users import User
from ..models.associations import Association
from .database import DatabaseConnection
con = DatabaseConnection()

def generate_hash(password):
        return sha256.hash(password)



class User_Controller:
    
    
    def create_user():
        """
            function to create a user
        """

        request_data = request.get_json(force=True)
        if len(request_data.keys()) != 8:
            return jsonify({"message": "Some fields are missing"}), 400
        
        associationId = request_data['associationId']
        country = request_data['country']
        name = request_data['name']
        status = 1
        user_group = request_data['user_group']
        user_role = request_data['user_role']
        created_by = name
        email = request_data['email']
        password = request_data['password']
        confirm_password = request_data['confirm_password']
        creation_date = datetime.date.today().strftime('%Y-%m-%d')
        validate_input = Validator()
        if not (validate_input.validate_password(password)):
            return jsonify({"message": "The password must be more than 8 characters"}),400
        if password != confirm_password:
            return jsonify({"message":"password mismatch"}),400
        if not (validate_input.validate_string_input(name)):
            return jsonify({"message": "name Field should\
                            contain strings "}), 400
        if not (validate_input.validate_email(email)):
            return jsonify({"message": "invalid email"}), 400
        user = con.get_user_by_email(email)
        
        if  user:
            return jsonify({"message": "User with that email already exists"}), 400
        if not (validate_input.validate_email(email)):
            return jsonify({"message":"The password you have created is weak"}),400
        if not (validate_input.validate_string_input(country)):
            return jsonify({"message": "location Field should\
                            contain strings"}), 400
        if not (validate_input.validate_string_input(user_group)):
            return jsonify({"message": "userid Field should contain strings"}), 400
        if not (validate_input.validate_string_input(user_role)):
            return jsonify({"message": "userid Field should contain strings"}), 400
        association = con.get_single_association(associationId)
        if (not association):
            return jsonify({"message": "The association with that id doesnot exist"}), 400
        encrpted_password=generate_hash(password)
        
        user=User(associationId, name, status,email,encrpted_password, country, user_group,user_role,created_by,creation_date).__dict__
        con.add_user(user['associationId'], user['name'],user['status'], user['email'],user['password'],user['country'], user['user_group'],user['user_role'],user['created_by'],user['creation_date'])

        return jsonify({"message": "Your account has been created","account":request_data}), 201

    def fetch_specific_user(userId):
        """
            Function fetch specific user
            :return user:
        """
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'message': 'Missing token in the Authorization Header'}), 401
          
        single_user = con.get_single_user(userId)
        if not single_user:
            return jsonify({"message": "user with that id doesnot exist"}), 404

        if single_user['status'] == 0:
            return jsonify({"message": "Account has been deactivated"}), 404

        role = single_user['user_role']
        if role == 'admin' or role == 'superadmin' or current_user_id == single_user['userId']:
            if single_user == []:
                return jsonify({"message": "No users found"}), 404
            return jsonify({'user': single_user}), 200
            
        return jsonify ({"message":"You are not authorised to view user details"}),400
    
    
    def fetch_all_users():
        """
            Function fetch all users
            :return users list:
        """
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'message': 'Missing token in the Authorization Header'}), 401
        
        User = con.get_single_user(current_user_id)
        
        role = User['user_role']
        if role == 'admin' or role == 'superadmin':
            users = con.get_all_users()
            if users == []:
                return jsonify({"message": "No users found"}), 404
            return jsonify({'users': users}), 200

        return jsonify({"message":"You are not authorised to view all users"}),401





    def cancel_specific_user(userId):
        """
            Function cancel user
            :return success message:
        """

        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'message': 'Missing token in the Authorization Header'}), 401

        user_to_edit = con.get_single_user(userId)
        role = user_to_edit['user_role']
        if not user_to_edit:
            return jsonify({"message": "The user with that id doesnt exist"}), 404
            
        if user_to_edit['status'] == 0:
            return jsonify({"message": "Account has been deactivated"}), 404
            
        if role == 'admin' or role == 'superadmin' or current_user_id == user_to_edit['userId']:
            con.cancel_user(userId)
            return jsonify({"message": "User has been cancelled"}), 200

        return jsonify({"message":"You are not authorised to cancel users"}),400       
        
    def update_user_name(userId):
        """
            Function update name
            :return success message:
        """

        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'message': 'Missing token in the Authorization Header'}), 401

        user = con.get_single_user(userId)
        role = user['user_role']
        id = user['userId']
        
        if user['status'] == 0:
            return jsonify({"message": "The user with that account doesnt exist"}), 404
            
        if not user:
            return jsonify({"message": "The user you are editing doesnt\
                            exist"}), 404

        request_data=request.get_json(force=True)
        
        if len(request_data.keys()) != 1:
            return jsonify({"message": "Some fields are missing"}), 400

        name = request_data['name']

        if (user['name'] == name):
            return jsonify({"message": "The name is already upto date"}), 400
            
        validate_name = Validator().validate_string_input(name)

        if role == 'admin' or role == 'superadmin' or current_user_id == id:
            con.update_user_name(userId, name)
            edited_data = con.get_single_user(userId)
            return jsonify({"message": "Your name has been updated ",
                        "updated user credentials": edited_data}), 200

        return jsonify({"message":"You cannot change a name of an association you have not created"}),400

        

    def update_user_role(userId):
        """
            Function update user_role
            :param userId:
            
            :return success message:
        """
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'message': 'Missing token in the Authorization Header'}), 401

        user = con.get_single_user(userId)
        role = user['user_role']
        id = user['userId']
        
        if user['status'] == 0:
            return jsonify({"message": "The user with that account doesnt exist"}), 404
            
        if not user:
            return jsonify({"message": "The user you are editing doesnt\
                            exist"}), 404

        request_data=request.get_json(force=True)
        
        if len(request_data.keys()) != 1:
            return jsonify({"message": "Some fields are missing"}), 400

        user_role = request_data['user_role']

        if (user['user_role'] == user_role):
            return jsonify({"message": "The user_role is already upto date"}), 400
            
        validate_user_role = Validator().validate_string_input(user_role)

        if role == 'admin' or role == 'superadmin':
            con.update_userrole(userId, user_role)
            edited_data = con.get_single_user(userId)
            return jsonify({"message": "Your user_role has been updated ",
                        "updated user credentials": edited_data}), 200

        return jsonify({"message":"You cannot change a name of an association you have not created"}),400

    def delete_user(userId):
        """
            Function delete
            :return success message:
        """
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'message': 'Missing token in the Authorization Header'}), 401

        User = fetch_specific_user(current_user_id)
        user_to_edit = con.get_single_user(userId)
        role = user_to_edit['user_role']
        if not user_to_edit:
            return jsonify({"message": "The user with that id doesnt exist"}), 404
            
        if user_to_edit['status'] == 0:
            return jsonify({"message": "Account has been deactivated"}), 404
            
        if role == 'admin' or role == 'superadmin' or current_user_id == user_to_edit['userId']:
            con.delete_user(userId)
            return jsonify({"message": "User has been deleted"}), 200

        return jsonify({"message":"You are not authorised to delete users"}),400

    def recover_password(email,newpassword):
        """
        Function to reset password
        :param email:
        :param newpassword:
        :return success message:
        """
        password= generate_hash(newpassword)
        
        return con.reset_password(email, password)
        
    def fetch_pending_accounts():
        """
        Function to fetch_pending_accounts
        :return all accounts whose status is pending:
        """

        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({'message': 'Missing token in the Authorization Header'}), 401

        User = fetch_specific_user(current_user_id)
        user_to_edit = con.get_single_user(userId)
        role = user_to_edit['user_role']
        if not user_to_edit:
            return jsonify({"message": "The user with that id doesnt exist"}), 404
            
        if user_to_edit['status'] == 0:
            return jsonify({"message": "Account has been deactivated"}), 404
            
        if role == 'superadmin' :
            return jsonify({"Pending accounts":con.get_pending_accounts()}),200


    def logout():
        """User_Controller
        Function to rlogout
        :param token:
        :return successful logout message:
        """
        
        token = get_jwt_identity()
        
        if not token:
            return jsonify({"message": "missing authentication token"}), 401

        con.add_to_blacklist(token)
        return jsonify({"message": "successfully logged out"}), 200
        
        

    