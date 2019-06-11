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
   

        if len(request_data.keys()) != 10:
            return jsonify({"message": "Some fields are missing "}), 400

        first_name = request_data['first_name']
        last_name = request_data['last_name']
        other_name = request_data['other_name']
        photo = request_data['photo']
        associationId = request_data['associationId']
        governmentId = request_data['governmentId'] 
        status = 1
        user_role = request_data['user_role']
        email = request_data['email']       
        password = request_data['password']
        country = request_data['country']
        created_by= "Null"
        updated_by = "Null"
        creation_date= datetime.date.today().strftime('%Y-%m-%d')
        updated_at= datetime.date.today().strftime('%Y-%m-%d')
        

        if associationId == 'null' and governmentId == 'null' and user_role != 'superadmin':
            return jsonify({"message":"missing associationId or governmentid"}),400

        validate_input = Validator()

        if not (validate_input.validate_password(password)):
            return jsonify({"message": "The password must be more than 8 characters"}), 400
            
        
        if not (validate_input.validate_string_input(first_name)):
            return jsonify({"message": "name must be a string"}), 400

        if not (validate_input.validate_string_input(last_name)):
            return jsonify({"message": "name must be a string"}), 400
        
        if not (validate_input.validate_string_input(other_name)):
            return jsonify({"message": "name must be a string "}), 400

        if not (validate_input.validate_email(email)):
            return jsonify({"message": "invalid email"}), 400
            
        if not (validate_input.validate_string_input(country)):
            return jsonify({"message": "country Field should contain a string "}), 400
        

        if not (validate_input.validate_string_input(user_role)):
            return jsonify({"message": "user_role field should contain strings"}), 400

        if not (validate_input.validate_user_role(user_role)):
            return jsonify({"message": "invalid user role"}), 400

        user = con.get_user_by_email(email)
        
        if  user:
            return jsonify({"message": "User with that email already exists"}), 400

        association = con.get_single_association(associationId)

        if (not association):
            return jsonify({"message": "The association with that id doesnot exist"}), 400
        
        government = con.get_single_government(governmentId)

        if (not government):
            return jsonify({"message": "The government with that id doesnot exist"}), 400
        # if user_role == "superadmin"

        encrpted_password=generate_hash(password)
        
        user = User(first_name ,last_name ,other_name ,photo ,associationId ,governmentId ,status ,user_role ,email ,encrpted_password ,country ,created_by,creation_date ,updated_by,updated_at).__dict__
        
        con.add_user(user['first_name'], user['last_name'], user['other_name'],user['photo'], user['associationId'],user['governmentId'],user['status'], user['user_role'],user['email'],user['password'],user['country'],user['created_by'],user['creation_date'],user['updated_by'],user['updated_at'])

        return jsonify({"message": "Your account has been created","User Details":request_data}), 201

    def fetch_specific_user(userId):
        """
            Function fetch specific user
            :param userid:
            :return user:
        """

        current_user_id = get_jwt_identity()
   
        single_user = con.get_single_user(userId)
        if not single_user:
            return jsonify({"message": "user with that id doesnot exist"}), 404

        if single_user['status'] == 0 or single_user['status'] == '0':
            return jsonify({"message": "Account has been deactivated"}), 404

        role = single_user['user_role']

        if role == 'admin' or role == 'superadmin' or current_user_id == single_user['userId']:
            return jsonify({'message':'User detais','user': single_user}), 200
            
        return jsonify ({"message":"Unauthorised access"}),401
    
    
    def fetch_all_users():
        """
            Function fetch all users
            :return users list:
        """

        current_user_id = get_jwt_identity()
        
        User = con.get_single_user(current_user_id)
        
        role = User['user_role']
        if role == 'admin' or role == 'superadmin':
            users = con.get_all_users()
            return jsonify({'users': users}), 200

        return jsonify({"message":"Unauthorised access"}),401

    def cancel_specific_user(userId):
        """
            Function cancel user
            :param userid:
            :return success message:
        """

        current_user_id = get_jwt_identity()

        user_to_edit = con.get_single_user(userId)
       
        if user_to_edit == None:
            return jsonify({"message": "The user with that id doesnt exist"}), 404

        if user_to_edit['status'] == 0 or user_to_edit['status'] == '0':
            return jsonify({"message": "Account has been deactivated"}), 404
        
        role = user_to_edit['user_role']
        if role == 'admin' or role == 'superadmin' or current_user_id == user_to_edit['userId']:
            con.cancel_user(userId)
            return jsonify({"message": "User has been cancelled"}), 200

        return jsonify({"message":"Unauthorised access"}),400       
        
    def update_user_name(userId):
        """
            Function update name
            :param userid:
            :return success message:
        """

        current_user_id = get_jwt_identity()

        user = con.get_single_user(userId)
        if not user or user == None:
            return jsonify({"message": "The user you are editing doesnt exist"}), 404
        
        id = user['userId']
        
        if user['status'] == 0 or user['status'] == '0':
            return jsonify({"message": "The user with that account doesnt exist"}), 404
            

        request_data=request.get_json(force=True)
        
        if len(request_data.keys()) != 3:
            return jsonify({"message": "Some fields are missing"}), 400

        first_name = request_data['first_name']
        last_name = request_data['last_name']
        other_name = request_data['other_name']
        updated_by, userId = current_user_id
        updated_at = datetime.date.today().strftime('%Y-%m-%d')
        
        if (user['first_name'] == first_name and user['last_name'] == last_name and user['other_name'] == other_name):
            return jsonify({"message": "The name is already upto date"}), 400
            
        validate_name = Validator().validate_string_input(name)
        if not (validate_input.validate_string_input(first_name)):
            return jsonify({"message": "name must be a string"}), 400

        if not (validate_input.validate_string_input(last_name)):
            return jsonify({"message": "name must be a string"}), 400
        
        if not (validate_input.validate_string_input(other_name)):
            return jsonify({"message": "name must be a string "}), 400
        
        role = user['user_role']
        if role == 'admin' or role == 'superadmin' or current_user_id == id:
            con.update_user_name(first_name, last_name, othername, updated_by,updated_at,userId )
            edited_data = con.get_single_user(userId)
            return jsonify({"message": "Your name has been updated ",
                        "updated user credentials": edited_data}), 200

        return jsonify({"message":"Unauthorised access"}),401

        

    def update_user_role(userId):
        """
            Function update user_role
            :param userId:
            :return success message:
        """

        current_user_id = get_jwt_identity()

        user = con.get_single_user(userId)
        if not user or user == None:
            return jsonify({"message": "The user you are editing doesnt exist"}), 404

        id = user['userId']
        
        if user['status'] == 0 or user['status'] == '0':
            return jsonify({"message": "The user with that account doesnt exist"}), 404

        request_data=request.get_json(force=True)
      
        
        if len(request_data.keys()) != 1:
            return jsonify({"message": "Some fields are missing"}), 400

        user_role = request_data['user_role']
        updated_by = userId
        updated_at = datetime.date.today().strftime('%Y-%m-%d')

        role = user['user_role']
        if (role == user_role):
            return jsonify({"message": "The user_role is already upto date"}), 400
            
        validate_user_role = Validator().validate_string_input(user_role)
        if not validate_user_role:
            return jsonify({"message": "user role must be a string"}), 400
        
        if not Validator().validate_user_role(user_role):
            return jsonify({"message":"invalid user role"}),400

        if role == 'admin' or role == 'superadmin':
            con.update_userrole(userId, user_role, updated_by, updated_at)
            edited_data = con.get_single_user(userId)
            return jsonify({"message": "User_role has been updated",
                        "updated user credentials": edited_data}), 200

        return jsonify({"message":"Unauthorised access"}),401

    def delete_user(userId):
        """
            Function delete
            :param userid:
            :return success message:
        """

        current_user_id = get_jwt_identity()
        
        User = con.get_single_user(current_user_id)
        user_to_edit = con.get_single_user(userId)
        updated_by =userIduserId
        updated_at = datetime.date.today().strftime('%Y-%m-%d')

        if not user_to_edit or user_to_edit == None:
            return jsonify({"message": "The user with that id doesnt exist"}), 404
            
        if user_to_edit['status'] == 0 or user_to_edit['status'] == '0':
            return jsonify({"message": "Account has been deactivated"}), 404

        role = user_to_edit['user_role'] 
        if role == 'admin' or role == 'superadmin' or current_user_id == user_to_edit['userId']:
            con.delete_user(userId, updated_by, updated_at)
            return jsonify({"message": "User has been deleted"}), 200

        return jsonify({"message":"Unauthorised access"}),401

    def recover_password():
        """
        Function to reset password
        :param email:
        :param newpassword:
        :return success message:
        """

        request_data = request.get_json(force = True)
        
        if len(request_data.keys()) != 2:
            return jsonify({"message": "Some fields are missing"}), 400

        email = request_data['email']
        newpassword = request_data['newpassword']

        validator = Validator()
        
        validate_mail = validator.validate_email(email)
        if not validate_mail:
            return jsonify({"message": "invalid email"}), 400
            
        validate_password = validator.validate_password(newpassword)
        if not validate_password:
            return jsonify({"message": "invalid password"}), 400
            
        user = con.get_user_by_email(email)
        if not user or user == []:
            return jsonify({"message": "User with that email doesnot exist"}), 404
        
        if user['status'] == 0 or user['status'] == '0':
            return jsonify({"message":"Account has been deactivated"}),400
            
        newpassword = generate_hash(newpassword)
        con.reset_password(email, newpassword)
        return jsonify({"message":"password successfully updated"}),200
        
    def fetch_pending_accounts():
        """
        Function to fetch_pending_accounts
        :return all accounts whose status is pending:
        """

        current_user_id = get_jwt_identity()

        User = fetch_specific_user(current_user_id)
        user_to_edit = con.get_single_user(userId)
        role = user_to_edit['user_role']

        if not user_to_edit:
            return jsonify({"message": "The user with that id doesnt exist"}), 404
            
        if user_to_edit['status'] == 0 or user_to_edit['status'] == '0':
            return jsonify({"message": "Account has been deactivated"}), 404
            
        if role == 'superadmin' :
        
            return jsonify({"Pending accounts": con.get_pending_accounts()}), 200

        return jsonify({"message":"Unauthorised access"}),401


    # def logout():
    #     """
    #         Function to logout user
    #         :return successful logout message:
    #     """
        
    #     token = get_jwt_identity()


    #     con.add_to_blacklist(token)
    #     return jsonify({"message": "successfully logged out"}), 200
        
        

    