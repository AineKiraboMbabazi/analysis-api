import re
import os
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (JWTManager, create_access_token)
import datetime
from flask import request, jsonify
from statisticsapi.models.users import User
from statisticsapi.controllers.users import User_Controller
from config import app_config
from statisticsapi import app
from validations import Validator
from statisticsapi.controllers.database import DatabaseConnection


def verify_hash(password, hash):
    return sha256.verify(password, hash)

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
            return jsonify({"message": "You entered an invalid email or the\
                            email is missing"}), 401

        if not login_validation.validate_password(password):
            return jsonify({"message": "You entered an invalid password,\
                            password should be atleast 8 characters long"}), 401

        
        user=DatabaseConnection()
        check_user=user.get_user_by_email(email)
        
        
        verified_hash=verify_hash(password, check_user['password'])
        if not verified_hash:
            return jsonify({"message":"The password you have entered is incorrect"}),401
        
        if check_user and verified_hash:
            expires = datetime.timedelta(days=1)
            
            auth_token = create_access_token(identity=check_user['userId'],
                                            expires_delta=expires)
            return jsonify({
                'message': 'login successful',
                'auth_token': auth_token}), 200

        return jsonify({"message": "You are not a system user"}), 401


    
    def recover_password():
        """
            function to recover password
        """
        request_data = request.get_json(force=True)
        if len(request_data.keys()) != 2:
            return jsonify({"message": "some fields are missing"}), 401
        email = request_data['email']
        newpassword= request_data['newpassword']
        
        
        login_validation = Validator()
        if not login_validation.validate_email(email):
            return jsonify({"message": "You entered an invalid email or the\
                            email is missing "}), 401
        if not login_validation.validate_password(newpassword):
            return jsonify({"message":" The password you entered is too weak"}),401
        User_Controller.recover_password(email,newpassword)

        return jsonify({"message": "You password has been reset"}), 200
        
    
    def logout():
        """
            function for logout
        """
        token = get_jwt_identity()
        User_Controller.logout(token)
        return jsonify({"message":"successfully logged out"}),200