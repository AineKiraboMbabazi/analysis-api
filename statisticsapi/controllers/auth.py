import re
import os
import datetime
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required,decode_token, get_jwt_identity)
from flask import request, jsonify
from statisticsapi.models.users import User
from statisticsapi.controllers.users import User_Controller
from config import app_config
from statisticsapi import app
from validations import Validator
from statisticsapi.controllers.database import DatabaseConnection


def verify_hash(password, hash):
    return sha256.verify(password, hash)

def decode_jwt_token(authorization_token):
        return(decode_token(authorization_token,app.config.get('SECRET_KEY'))['identity'])

class Auth():

    def create_user():
        """
            function to create a user
        """
        return User_Controller.create_user()


    
    def login():
        """
            Function login user
            :return success message, authentication token, userId:
        """
        request_data = request.get_json(force=True)
        if len(request_data.keys()) != 2:
            return jsonify({"message": "some fields are missing"}), 401

        email = request_data['email']
        
        password = request_data['password']
        
        login_validation = Validator()
        if not login_validation.validate_email(email):
            return jsonify({"message": "You entered an invalid email or the email is missing"}), 401

        if not login_validation.validate_password(password):
            return jsonify({"message": "You entered an invalid password,password should be atleast 8 characters long"}), 401

        
        user=DatabaseConnection()
        check_user=user.get_user_by_email(email)
        
        if check_user == None:
            return jsonify ({"message":"user is not availabe"}),404
        
        verified_hash=verify_hash(password, check_user['password'])
        
        if not verified_hash:
            return jsonify({"message":"The password you have entered is incorrect"}),401
        
        
        expires = datetime.timedelta(days=1)
        
        auth_token = create_access_token(identity=check_user['userId'],
                                        expires_delta=expires)

        return jsonify({
            'first_name':check_user['first_name'],
            'last_name':check_user['last_name'],
            'other_name':check_user['other_name'],
            'role':check_user['user_role'],
            'id':check_user['userId'],
            'message': 'login successful',
            'auth_token': auth_token
            }), 200

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
        # print(user['status'])
        if user['status'] == 0 or user['status'] == '0':
            return jsonify({"message":"Account has been deactivated"}),400
            
        newpassword = generate_hash(newpassword)
        con.reset_password(email, newpassword)
        return jsonify({"message":"password successfully updated"}),200
 

        