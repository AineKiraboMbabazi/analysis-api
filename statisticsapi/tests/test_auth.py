import json
import unittest
from statisticsapi import app
from statisticsapi.routes.associations import Association
from statisticsapi import app
from statisticsapi.routes.auth import Auth
from statisticsapi.routes.users import User
from statisticsapi.controllers.database import DatabaseConnection
from .test_base import TestBase



class TestAuth(TestBase):
    #############################################################################################
    #                                                                                           #
    #                                   LOGIN TESTCASES                                         #
    #                                                                                           #
    #############################################################################################

    def test_can_login_user(self):
        """
            function to test user login
        """
        
        self.sign_up()
        user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
            data=json.dumps(self.user_login_data))
        
        self.assertEqual(user_login.status_code, 200)
        response = json.loads(user_login.data)
        self.assertEqual(response['message'], 'login successful')
        
    def test_cant_login_user_with_missing_fields(self):
        """
            function to test user creation
        """
        
        self.sign_up()
        user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
            data=json.dumps(self.user_login_datam))
        self.assertEqual(user_login.status_code, 401)
        response = json.loads(user_login.data)
        self.assertEqual(response['message'], 'some fields are missing')

    def test_cant_login_user_with_invalid_email(self):
        """
            function to test user creation
        """
        
        self.sign_up()
        user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
            data=json.dumps(self.user_login_datae))
        self.assertEqual(user_login.status_code, 401)
        response = json.loads(user_login.data)
        self.assertEqual(response['message'], 'You entered an invalid email or the email is missing')
        

    def test_cant_login_user_with_invalid_password(self):
        """
            function to test user creation
        """
        
        self.sign_up()
        user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
            data=json.dumps(self.user_login_datap))
        self.assertEqual(user_login.status_code, 401)
        response = json.loads(user_login.data)
        self.assertEqual(response['message'], 'You entered an invalid password,password should be atleast 8 characters long')

    def test_cant_login_non_existent_user(self):
        """
            function to test user creation
        """
        
        self.sign_up()
        user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
            data=json.dumps(self.user_login_data44))
        self.assertEqual(user_login.status_code, 404)
        response = json.loads(user_login.data)
        self.assertEqual(response['message'], 'user is not availabe')
        
    def test_cant_login_user_with_incorrect_password(self):
        """
            function to test user creation
        """
        
        self.sign_up()
        user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
            data=json.dumps(self.user_login_datai))
        self.assertEqual(user_login.status_code, 401)
        response = json.loads(user_login.data)
        self.assertEqual(response['message'], 'The password you have entered is incorrect')

    # #############################################################################################
    # #                                                                                           #
    # #                             RECOVER PASSWORD TESTCASES                                    #
    # #                                                                                           #
    # #############################################################################################

    # def test_can_reset_password_successfully(self):
    #     self.sign_up()
    #     user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
    #         data=json.dumps(self.user_login_data))
    #     self.assertEqual(user_login.status_code, 200)
        
    #     recover = self.app_client.post("/api/v1/auth/forgot_password", content_type="application/json", 
    #         data=json.dumps(self.recover))
    #     self.assertEqual(recover.status_code, 200)
    #     response = json.loads(recover.data)
    #     self.assertEqual(response['message'], 'password successfully updated')

    # def test_cant_reset_password_for_inactivated_account(self):
    #     self.sign_up()
    #     token = self.user_login()
    #     user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
    #         data=json.dumps(self.user_login_data))
    #     self.assertEqual(user_login.status_code, 200)
    #     self.app_client.put("api/v1/users/delete/1", content_type="application/json",headers={'Authorization': f'Bearer {token}'} )
        
    #     recover = self.app_client.post("/api/v1/auth/forgot_password", content_type="application/json", 
    #         data=json.dumps(self.recover))
    #     self.assertEqual(recover.status_code, 400)
    #     response = json.loads(recover.data)
    #     self.assertEqual(response['message'], 'Account has been deactivated')

    # def test_cant_reset_password_for_nonexistent_account(self):
        
    #     recover = self.app_client.post("/api/v1/auth/forgot_password", content_type="application/json", 
    #         data=json.dumps(self.recover))
    #     self.assertEqual(recover.status_code, 404)
    #     response = json.loads(recover.data)
    #     self.assertEqual(response['message'], 'User with that email doesnot exist')

    
    # def test_cant_reset_password_with_invalid_password(self):
    #     self.sign_up()
    #     user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
    #         data=json.dumps(self.user_login_data))
    #     self.assertEqual(user_login.status_code, 200)
        
    #     recover = self.app_client.post("/api/v1/auth/forgot_password", content_type="application/json", 
    #         data=json.dumps({
    #     "email" : "eve@gmail.com",
    #     "newpassword": "ne1234"
    # }))
    #     self.assertEqual(recover.status_code, 400)
    #     response = json.loads(recover.data)
    #     self.assertEqual(response['message'], 'invalid password')

    # def test_cant_reset_password_with_invalid_email(self):
    #     self.sign_up()
    #     user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
    #         data=json.dumps(self.user_login_data))
    #     self.assertEqual(user_login.status_code, 200)
        
    #     recover = self.app_client.post("/api/v1/auth/forgot_password", content_type="application/json", 
    #         data=json.dumps({
    #     "email" : "evegmail.com",
    #     "newpassword": "mine1234"
    # }))
    #     self.assertEqual(recover.status_code, 400)
    #     response = json.loads(recover.data)
    #     self.assertEqual(response['message'], 'invalid email')
        
    
    # def test_cant_reset_password_with_missing_fields(self):
    #     self.sign_up()
    #     user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
    #         data=json.dumps(self.user_login_data))
    #     self.assertEqual(user_login.status_code, 200)
        
    #     recover = self.app_client.post("/api/v1/auth/forgot_password", content_type="application/json", 
    #         data=json.dumps({
        
    #     "newpassword": "mine1234"
    # }))
    #     self.assertEqual(recover.status_code, 400)
    #     response = json.loads(recover.data)
    #     self.assertEqual(response['message'], 'Some fields are missing')