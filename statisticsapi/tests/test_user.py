# import json
# import unittest
# from statisticsapi import app
# from statisticsapi.routes.associations import Association
# from statisticsapi import app
# from statisticsapi.routes.auth import Auth
# from statisticsapi.routes.users import User
# from statisticsapi.controllers.database import DatabaseConnection
# from .test_base import TestBase



# class TestUsers(TestBase):
#     #############################################################################################
#     #                                                                                           #
#     #                                   SIGNUP TESTCASES                                        #
#     #                                                                                           #
#     # #############################################################################################

#     def test_can_create_user(self):
#         """
#             function to test user creation
#         """
        
#         self.sign_up()

#     def test_cannot_create_user_with_missing_fields(self):
#         create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', 
#             data=json.dumps(self.user_missing_fields))
        
#         self.assertEqual(create_user.status_code, 400)
#         response = json.loads(create_user.data)
#         self.assertEqual(response['message'], 'Some fields are missing ')


#     def test_cannot_create_user_with_invalid_password(self):
#         create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', 
#             data=json.dumps(self.user_with_invalid_password))
        
#         self.assertEqual(create_user.status_code, 400)
#         response = json.loads(create_user.data)
#         self.assertEqual(response['message'], 'The password must be more than 8 characters')

#     def test_cannot_create_user_with_mismatching_password(self):
#         create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', 
#             data=json.dumps(self.user_with_invalid_password))
        
#         self.assertEqual(create_user.status_code, 400)
#         response = json.loads(create_user.data)
#         self.assertEqual(response['message'], 'The password must be more than 8 characters')

#     def test_cannot_create_user_with_invalid_name(self):
#         create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', 
#             data=json.dumps(self.user_with_invalid_name))
        
#         self.assertEqual(create_user.status_code, 400)
#         response = json.loads(create_user.data)
#         self.assertEqual(response['message'], 'name must be a string')

#     def test_cannot_create_user_with_invalid_email(self):
#         create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', 
#             data=json.dumps(self.user_with_invalid_email))
        
#         self.assertEqual(create_user.status_code, 400)
#         response = json.loads(create_user.data)
#         self.assertEqual(response['message'], 'invalid email')

#     def test_cannot_create_user_with_invalid_country(self):
#         create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', 
#             data=json.dumps(self.user_with_invalid_country))
        
#         self.assertEqual(create_user.status_code, 400)
#         response = json.loads(create_user.data)
#         self.assertEqual(response['message'], 'country Field should contain a string ')



#     def test_cannot_create_user_with_none_string_role(self):
#         create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', 
#             data=json.dumps(self.user_with_non_string_role))
        
#         self.assertEqual(create_user.status_code, 400)
#         response = json.loads(create_user.data)
#         self.assertEqual(response['message'], 'user_role field should contain strings')

#     def test_cannot_create_user_invalid_role(self):
#         create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', 
#             data=json.dumps(self.user_with_invalid_role))
        
#         self.assertEqual(create_user.status_code, 400)
#         response = json.loads(create_user.data)
#         self.assertEqual(response['message'], 'invalid user role')

#     def test_cannot_create_user_with_duplicate_email(self):
#         self.sign_up()
#         create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', 
#             data=json.dumps(self.user_with_duplicate_mail))
        
#         self.assertEqual(create_user.status_code, 400)
#         response = json.loads(create_user.data)
#         self.assertEqual(response['message'], 'User with that email already exists')


#     #############################################################################################
#     #                                                                                           #
#     #                             FETCH SPECIFIC USER TESTCASES                                 #
#     #                                                                                           #
#     #############################################################################################

#     def test_can_get_user_details_successfully(self):
#         self.sign_up()
#         user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
#             data=json.dumps(self.user_login_data))
#         self.assertEqual(user_login.status_code, 200)
#         response = json.loads(user_login.data)
#         self.assertEqual(response['message'], 'login successful')
#         self.user_access_token = response['auth_token']
        
#         token = self.user_access_token
#         users = self.app_client.get('/api/v1/users/1',content_type='application/json',
#                                 headers={'Authorization': f'Bearer {token}'})
#         self.assertEqual(users.status_code, 200)

#     def test_cannot_get_user_with_missing_token(self):
#         self.sign_up()
#         user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
#             data=json.dumps(self.user_login_data))
#         self.assertEqual(user_login.status_code, 200)
#         response = json.loads(user_login.data)
#         self.assertEqual(response['message'], 'login successful')
#         users = self.app_client.get('/api/v1/users/1', content_type='application/json')
#         response = json.loads(users.data)
#         self.assertEqual(users.status_code, 401)
#         self.assertEqual(response['msg'], 'Missing Authorization Header')

#     def test_cant_get_user_details_for_none_existent_user(self):
#         self.sign_up()
#         user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
#             data=json.dumps(self.user_login_data))
#         self.assertEqual(user_login.status_code, 200)
#         response = json.loads(user_login.data)
#         self.assertEqual(response['message'], 'login successful')
#         self.user_access_token = response['auth_token']
        
#         token = self.user_access_token
#         users = self.app_client.get('/api/v1/users/3',content_type='application/json',
#                                 headers={'Authorization': f'Bearer {token}'})
#         self.assertEqual(users.status_code, 404)
#         response = json.loads(users.data)
#     #     self.assertEqual(response['message'], 'user with that id doesnot exist')

#     def test_cant_get_user_details_for_deleted_user(self):
#         self.sign_up()
#         user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
#             data=json.dumps(self.user_login_data))
#         self.assertEqual(user_login.status_code, 200)
#         response = json.loads(user_login.data)
#         self.assertEqual(response['message'], 'login successful')
#         self.user_access_token = response['auth_token']
        
#         token = self.user_access_token
#         self.app_client.put('/api/v1/users/delete/1',content_type='application/json',
#                                 headers={'Authorization': f'Bearer {token}'})
        
#         users = self.app_client.get('/api/v1/users/1',content_type='application/json',
#                                 headers={'Authorization': f'Bearer {token}'})
#         self.assertEqual(users.status_code, 404)
#         response = json.loads(users.data)
#         self.assertEqual(response['message'], 'Account has been deactivated')


# #     def test_cant_get_user_details_without_authorisation_details(self):
# #         self.sign_up()
# #         self.sign_up1()
# #         user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
# #             data=json.dumps(self.user_login_data))
# #         self.assertEqual(user_login.status_code, 200)
# #         response = json.loads(user_login.data)
# #         self.assertEqual(response['message'], 'login successful')
# #         self.user_access_token = response['auth_token']
        
# #         token = self.user_access_token
# #         users = self.app_client.get('/api/v1/users/3',content_type='application/json',
# #                                 headers={'Authorization': f'Bearer {token}'})
# #         self.assertEqual(users.status_code, 401)
# #         response = json.loads(users.data)
# #         self.assertEqual(response['message'], 'Unauthorised access')

    
#     #############################################################################################
# #     #                                                                                           #
# #     #                             FETCH ALL USERS TESTCASES                                     #
# #     #                                                                                           #
# #     #############################################################################################

#     def test_can_get_all_users_successfully(self):
#         self.sign_up()
        
#         user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
#             data=json.dumps(self.user_login_data))
#         self.assertEqual(user_login.status_code, 200)
#         response = json.loads(user_login.data)
#         self.assertEqual(response['message'], 'login successful')
#         self.user_access_token = response['auth_token']
        
#         token = self.user_access_token
#         users = self.app_client.get('/api/v1/users',content_type='application/json',
#                                 headers={'Authorization': f'Bearer {token}'})
#         self.assertEqual(users.status_code, 200)

#     def test_cant_get_all_without_token(self):
#         self.sign_up()
      
#         user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
#             data=json.dumps(self.user_login_data))
#         self.assertEqual(user_login.status_code, 200)
#         response = json.loads(user_login.data)
#         self.assertEqual(response['message'], 'login successful')
#         users = self.app_client.get('/api/v1/users',content_type='application/json')
#         self.assertEqual(users.status_code, 401)

# #     def test_cant_get_all_users_without_access_rights(self):
# #         self.sign_up()
# #         token = self.superadmin_login()
# #         self.app_client.post("/api/v1/governments", content_type='application/json', 
# #             data=json.dumps(self.government_data), headers={'Authorization': f'Bearer {token}'})
# #         self.app_client.post("/api/v1/associations", content_type='application/json', 
# #             data=json.dumps(self.association_data), headers={'Authorization': f'Bearer {token}'})
# #         create_user =self.app_client.post("/api/v1/auth/signup", content_type='application/json', 
# #             data=json.dumps(self.user1))
        
# #         self.assertEqual(create_user.status_code, 201)
# #         response = json.loads(create_user.data)
# #         self.assertEqual(response['message'], 'Your account has been created')
    
# #         user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
# #             data=json.dumps(self.user1_login))
# #         self.assertEqual(user_login.status_code, 200)
# #         response = json.loads(user_login.data)
# #         self.assertEqual(response['message'], 'login successful')
# #         self.user_access_token = response['auth_token']
        
# #         token = self.user_access_token
# #         users = self.app_client.get('/api/v1/users',content_type='application/json',
# #                                 headers={'Authorization': f'Bearer {token}'})
# #         self.assertEqual(users.status_code, 401)
# #         response = json.loads(users.data)
# #         self.assertEqual(response['message'], 'Unauthorised access')
  
    

# #     #############################################################################################
# #     #                                                                                           #
# #     #                             CANCELLATION OF A USERS TESTCASES                             #
# #     #                                                                                           #
# #     #############################################################################################
  
#     def test_can_cancel_user(self):
#         self.sign_up()
#         user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
#             data=json.dumps(self.user_login_data))
#         self.assertEqual(user_login.status_code, 200)
#         response = json.loads(user_login.data)
#         self.assertEqual(response['message'], 'login successful')
#         self.user_access_token = response['auth_token']
        
#         token = self.user_access_token
             
#         users = self.app_client.put('/api/v1/users/cancel/1',content_type='application/json',
#                                 headers={'Authorization': f'Bearer {token}'})

#         self.assertEqual(users.status_code, 200)
#         response = json.loads(users.data)
#         self.assertEqual(response['message'], 'User has been cancelled')

    
#     def test_cant_cancel_user_without_token(self):
#         self.sign_up()
#         user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
#             data=json.dumps(self.user_login_data))
#         self.assertEqual(user_login.status_code, 200)
#         response = json.loads(user_login.data)
#         self.assertEqual(response['message'], 'login successful')
#         users = self.app_client.put('/api/v1/users/cancel/1',content_type='application/json')
#         self.assertEqual(users.status_code, 401)
#         response = json.loads(users.data)
#         self.assertEqual(response['msg'], 'Missing Authorization Header')

#     def test_cant_cancel_non_existent_user(self):
#         self.sign_up()
#         user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
#             data=json.dumps(self.user_login_data))
#         self.assertEqual(user_login.status_code, 200)
#         response = json.loads(user_login.data)
#         self.assertEqual(response['message'], 'login successful')
#         self.user_access_token = response['auth_token']
        
#         token = self.user_access_token
        
        
#         users = self.app_client.put('/api/v1/users/cancel/6',content_type='application/json',
#                                 headers={'Authorization': f'Bearer {token}'})
#         self.assertEqual(users.status_code, 404)
#         response = json.loads(users.data)
#         self.assertEqual(response['message'], 'The user with that id doesnt exist')

    
#     def test_cant_cancel_user_with_inactive_account(self):
#         self.sign_up()
#         user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
#             data=json.dumps(self.user_login_data))

#         self.assertEqual(user_login.status_code, 200)
#         response = json.loads(user_login.data)
#         self.assertEqual(response['message'], 'login successful')
#         self.user_access_token = response['auth_token']
        
#         token = self.user_access_token
#         delete = self.app_client.put('/api/v1/users/delete/1',content_type='application/json',
#                                 headers={'Authorization': f'Bearer {token}'})
        
#         users = self.app_client.put('/api/v1/users/cancel/1',content_type='application/json',
#                                 headers={'Authorization': f'Bearer {token}'})
      
#         self.assertEqual(users.status_code, 404)
#         response = json.loads(users.data)
#         self.assertEqual(response['message'], 'Account has been deactivated')


#     # def test_cant_cancel_user_without_necessary_rights(self):
        
#     #     self.sign_up1()
#     #     user_login1 = self.app_client.post("api/v1/auth/login", content_type="application/json", 
#     #         data=json.dumps(self.user1_login))
#     #     self.assertEqual(user_login1.status_code, 200)
#     #     response = json.loads(user_login1.data)
#     #     self.assertEqual(response['message'], 'login successful')
#     #     token = response['auth_token']
               
#     #     users = self.app_client.put('/api/v1/users/cancel/2',content_type='application/json',
#     #                             headers={'Authorization': f'Bearer {token}'})
#     #     self.assertEqual(users.status_code, 401)
#     #     response = json.loads(users.data)
#     #     self.assertEqual(response['message'], 'Unauthorised access')

#     #############################################################################################
#     #                                                                                           #
#     #                             UPDATE USERNAME TESTCASES                                     #
#     #                                                                                           #
# #     #############################################################################################
#     def test_can_update_user_name_successfully(self):

#         self.sign_up()
#         user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
#             data=json.dumps(self.user_login_data))
#         self.assertEqual(user_login.status_code, 200)
#         response = json.loads(user_login.data)
#         self.assertEqual(response['message'], 'login successful')
#         token = response['auth_token']

#         update_name = self.app_client.put("api/v1/users/name/1", content_type="application/json", 
#             data=json.dumps({"first_name":"Tim",
#             "last_name":"Timo",
#             "other_name":"Timoth"}), headers={'Authorization': f'Bearer {token}'})

#         self.assertEqual(update_name.status_code, 200)
#         response = json.loads(update_name.data) 
#         self.assertEqual(response['message'], 'Your name has been updated ')


#     def test_cant_update_user_name_without_access_token(self):

#         self.sign_up()
#         user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
#             data=json.dumps(self.user_login_data))
#         self.assertEqual(user_login.status_code, 200)
#         response = json.loads(user_login.data)
#         self.assertEqual(response['message'], 'login successful')
#         token = response['auth_token']

#         update_name = self.app_client.put("api/v1/users/name/1", content_type="application/json", 
#             data=json.dumps({"name":"Timothy"}))

#         self.assertEqual(update_name.status_code, 401)
#         response = json.loads(update_name.data) 
#         self.assertEqual(response['msg'], 'Missing Authorization Header')

#     def test_cant_update_user_name_for_deactivated_account(self):

#         self.sign_up()
#         user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
#             data=json.dumps(self.user_login_data))
#         self.assertEqual(user_login.status_code, 200)
#         response = json.loads(user_login.data)
#         self.assertEqual(response['message'], 'login successful')
#         token = response['auth_token']
#         self.app_client.put('/api/v1/users/cancel/1',content_type='application/json',
#                                 headers={'Authorization': f'Bearer {token}'})
#         update_name = self.app_client.put("api/v1/users/name/1", content_type="application/json", 
#             data=json.dumps({"first_name":"Tim",
#             "last_name":"Timo",
#             "other_name":"Timoth"}), headers={'Authorization': f'Bearer {token}'})

#         self.assertEqual(update_name.status_code, 404)
#         response = json.loads(update_name.data) 
#         self.assertEqual(response['message'], 'The user with that account doesnt exist')

    
#     def test_cant_update_user_name_for_nonexistent_user(self):

#         self.sign_up()
#         user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
#             data=json.dumps(self.user_login_data))
#         self.assertEqual(user_login.status_code, 200)
#         response = json.loads(user_login.data)
#         self.assertEqual(response['message'], 'login successful')
#         token = response['auth_token']

#         update_name = self.app_client.put("api/v1/users/name/5", content_type="application/json", 
#             data=json.dumps({"first_name":"Tim",
#             "last_name":"Timo",
#             "other_name":"Timoth"}), headers={'Authorization': f'Bearer {token}'})
            
#         self.assertEqual(update_name.status_code, 404)
#         response = json.loads(update_name.data) 
#         self.assertEqual(response['message'], 'The user you are editing doesnt exist')

    
#     def test_cant_update_user_name_with_missing_fields(self):

#         self.sign_up()
#         user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
#             data=json.dumps(self.user_login_data))
#         self.assertEqual(user_login.status_code, 200)
#         response = json.loads(user_login.data)
#         self.assertEqual(response['message'], 'login successful')
#         token = response['auth_token']

#         update_name = self.app_client.put("api/v1/users/name/1", content_type="application/json", 
#             data=json.dumps({}), headers={'Authorization': f'Bearer {token}'})
            
#         self.assertEqual(update_name.status_code, 400)
#         response = json.loads(update_name.data) 
#         self.assertEqual(response['message'], 'Some fields are missing')


#     def test_cant_update_user_name_if_its_already_upto_date(self):

#         self.sign_up()
#         user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
#             data=json.dumps(self.user_login_data))
#         self.assertEqual(user_login.status_code, 200)
#         response = json.loads(user_login.data)
#         self.assertEqual(response['message'], 'login successful')
#         token = response['auth_token']

#         update_name = self.app_client.put("api/v1/users/name/2", content_type="application/json", 
#             data=json.dumps({"first_name":"aine",
#         "last_name":"kirabo",
#         "other_name":"mbabazi"}), headers={'Authorization': f'Bearer {token}'})

#         self.assertEqual(update_name.status_code, 400)
#         response = json.loads(update_name.data) 
#         self.assertEqual(response['message'], 'The name is already upto date')


#     def test_cant_update_user_name_if_its_nonstring(self):

#         self.sign_up()
#         user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
#             data=json.dumps(self.user_login_data))
#         self.assertEqual(user_login.status_code, 200)
#         response = json.loads(user_login.data)
#         self.assertEqual(response['message'], 'login successful')
#         token = response['auth_token']

#         update_name = self.app_client.put("api/v1/users/name/1", content_type="application/json", 
#             data=json.dumps({"first_name":"12345",
#             "last_name":"kirabo",
#             "other_name":"mbabazi",}), headers={'Authorization': f'Bearer {token}'})

#         self.assertEqual(update_name.status_code, 400)
#         response = json.loads(update_name.data) 
#         self.assertEqual(response['message'], 'name must be a string')


#     # def test_cant_update_user_name_if_missing_access_rights(self):

        
#     #     create_user1= self.app_client.post("/api/v1/auth/signup", content_type='application/json', 
#     #         data=json.dumps(self.user1))
#     #     print(self.user1['user_role'])
#     #     user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
#     #         data=json.dumps({"email":"admin5@admin.com","password":"password"}))

#     #     self.assertEqual(user_login.status_code, 200)
#     #     response = json.loads(user_login.data)
#     #     print(response)
#     #     self.assertEqual(response['message'], 'login successful')
#     #     token = response['auth_token']

#     #     update_name = self.app_client.put("api/v1/users/name/1", content_type="application/json", 
#     #         data=json.dumps({"first_name":"aine",
#     #                         "last_name":"peace",
#     #                         "other_name":"mbabazi"}), headers={'Authorization': f'Bearer {token}'})

#     #     self.assertEqual(update_name.status_code, 200)
#     #     response = json.loads(update_name.data) 
#     #     self.assertEqual(response['message'], 'Unauthorised access')


#     #############################################################################################
#     #                                                                                           #
#     #                             UPDATE USERROLE TESTCASES                                     #
#     #                                                                                           #
#     #############################################################################################
#     def test_can_update_user_role_successfully(self):

#         self.sign_up()
#         user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
#             data=json.dumps(self.user_login_data))
#         self.assertEqual(user_login.status_code, 200)
#         response = json.loads(user_login.data)
#         self.assertEqual(response['message'], 'login successful')
#         token = response['auth_token']

#         update_name = self.app_client.put("api/v1/users/user_role/1", content_type="application/json", 
#             data=json.dumps({"user_role":"admin"}), headers={'Authorization': f'Bearer {token}'})
#         self.assertEqual(update_name.status_code, 200)
#         response = json.loads(update_name.data) 
#         self.assertEqual(response['message'], 'User_role has been updated')


#     def test_cant_update_user_role_without_access_token(self):

#         self.sign_up()
#         user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
#             data=json.dumps(self.user_login_data))
#         self.assertEqual(user_login.status_code, 200)
#         response = json.loads(user_login.data)
#         self.assertEqual(response['message'], 'login successful')
#         token = response['auth_token']

#         update_name = self.app_client.put("api/v1/users/user_role/1", content_type="application/json", 
#             data=json.dumps({"user_role":"admin"}))

#         self.assertEqual(update_name.status_code, 401)
#         response = json.loads(update_name.data) 
#         self.assertEqual(response['msg'], 'Missing Authorization Header')

#     def test_cant_update_user_role_for_deactivated_account(self):

#         self.sign_up()
#         user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
#             data=json.dumps(self.user_login_data))
#         self.assertEqual(user_login.status_code, 200)
#         response = json.loads(user_login.data)
#         self.assertEqual(response['message'], 'login successful')
#         token = response['auth_token']
#         self.app_client.put('/api/v1/users/cancel/1',content_type='application/json',
#                                 headers={'Authorization': f'Bearer {token}'})

#         update_name = self.app_client.put("api/v1/users/user_role/1", content_type="application/json", 
#             data=json.dumps({"user_role":"admin"}), headers={'Authorization': f'Bearer {token}'})

#         self.assertEqual(update_name.status_code, 404)
#         response = json.loads(update_name.data) 
#         self.assertEqual(response['message'], 'The user with that account doesnt exist')

    
#     def test_cant_update_user_role_for_nonexistent_user(self):

#         self.sign_up()
#         user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
#             data=json.dumps(self.user_login_data))
#         self.assertEqual(user_login.status_code, 200)
#         response = json.loads(user_login.data)
#         self.assertEqual(response['message'], 'login successful')
#         token = response['auth_token']

#         update_name = self.app_client.put("api/v1/users/user_role/4", content_type="application/json", 
#             data=json.dumps({"user_role": "admin"}), headers={'Authorization': f'Bearer {token}'})
            
#         self.assertEqual(update_name.status_code, 404)
#         response = json.loads(update_name.data) 
#         self.assertEqual(response['message'], 'The user you are editing doesnt exist')
    
#     def test_cant_update_user_role_with_missing_fields(self):

#         self.sign_up()
#         user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
#             data=json.dumps(self.user_login_data))
#         self.assertEqual(user_login.status_code, 200)
#         response = json.loads(user_login.data)
#         self.assertEqual(response['message'], 'login successful')
#         token = response['auth_token']

#         update_name = self.app_client.put("api/v1/users/user_role/1", content_type="application/json", 
#             data=json.dumps({}), headers={'Authorization': f'Bearer {token}'})
            
#         self.assertEqual(update_name.status_code, 400)
#         response = json.loads(update_name.data) 
#         self.assertEqual(response['message'], 'Some fields are missing')

#     def test_cant_update_user_role_if_its_already_upto_date(self):

#         self.sign_up()
#         user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
#             data=json.dumps(self.user_login_data))
#         self.assertEqual(user_login.status_code, 200)
#         response = json.loads(user_login.data)
#         self.assertEqual(response['message'], 'login successful')
#         token = response['auth_token']

#         update_name = self.app_client.put("api/v1/users/user_role/2", content_type="application/json", 
#             data=json.dumps({"user_role" : "superadmin"}), headers={'Authorization': f'Bearer {token}'})

#         self.assertEqual(update_name.status_code, 400)
#         response = json.loads(update_name.data) 
#         self.assertEqual(response['message'], 'The user_role is already upto date')

#     def test_cant_update_user_role_if_its_nonstring(self):

#         self.sign_up()
#         user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
#             data=json.dumps(self.user_login_data))
#         self.assertEqual(user_login.status_code, 200)
#         response = json.loads(user_login.data)
#         self.assertEqual(response['message'], 'login successful')
#         token = response['auth_token']

#         update_name = self.app_client.put("api/v1/users/user_role/1", content_type="application/json", 
#             data=json.dumps({"user_role" : "11111111"}), headers={'Authorization': f'Bearer {token}'})

#         self.assertEqual(update_name.status_code, 400)
#         response = json.loads(update_name.data) 
#         self.assertEqual(response['message'], 'user role must be a string')

#     def test_cant_update_user_role_if_its_not_in_user_groups(self):

#         self.sign_up()
#         user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
#             data=json.dumps(self.user_login_data))
#         self.assertEqual(user_login.status_code, 200)
#         response = json.loads(user_login.data)
#         self.assertEqual(response['message'], 'login successful')
#         token = response['auth_token']

#         update_name = self.app_client.put("api/v1/users/user_role/1", content_type="application/json", 
#             data=json.dumps({"user_role" : "superuser"}), headers={'Authorization': f'Bearer {token}'})

#         self.assertEqual(update_name.status_code, 400)
#         response = json.loads(update_name.data) 
#         self.assertEqual(response['message'], 'invalid user role')

#     # def test_cant_update_user_role_if_missing_access_rights(self):

#     #     self.sign_up()
#     #     user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
#     #         data=json.dumps(self.user_login_data))
#     #     self.assertEqual(user_login.status_code, 200)
#     #     response = json.loads(user_login.data)
#     #     self.assertEqual(response['message'], 'login successful')
#     #     token = response['auth_token']

#     #     create_user1= self.app_client.post("/api/v1/auth/signup", content_type='application/json', 
#     #         data=json.dumps(self.user1))
        
#     #     update_name = self.app_client.put("api/v1/users/user_role/2", content_type="application/json", 
#     #         data=json.dumps({"user_role" : "admin"}), headers={'Authorization': f'Bearer {token}'})

#     #     self.assertEqual(update_name.status_code, 400)
#     #     response = json.loads(update_name.data) 
#     #     self.assertEqual(response['message'], 'Unauthorised access')


# #     #############################################################################################
# #     #                                                                                           #
# #     #                             DELETE USER TESTCASES                                         #
# #     #                                                                                           #
# #     #############################################################################################
#     def test_can_delete_user_successfully(self):

#         self.sign_up()
#         user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
#             data=json.dumps(self.user_login_data))
#         self.assertEqual(user_login.status_code, 200)
#         response = json.loads(user_login.data)
#         self.assertEqual(response['message'], 'login successful')
#         token = response['auth_token']

#         update_name = self.app_client.put("api/v1/users/delete/1", content_type="application/json", 
#             headers={'Authorization': f'Bearer {token}'})
#         self.assertEqual(update_name.status_code, 200)
#         response = json.loads(update_name.data) 
#         self.assertEqual(response['message'], 'User has been deleted')


#     def test_cant_delete_user_without_access_token(self):

#         self.sign_up()
#         user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
#             data=json.dumps(self.user_login_data))
#         self.assertEqual(user_login.status_code, 200)
#         response = json.loads(user_login.data)
#         self.assertEqual(response['message'], 'login successful')
#         token = response['auth_token']

#         update_name = self.app_client.put("api/v1/users/delete/1", content_type="application/json")

#         self.assertEqual(update_name.status_code, 401)
#         response = json.loads(update_name.data) 
#         self.assertEqual(response['msg'], 'Missing Authorization Header')

#     def test_cant_delete_user_for_deactivated_account(self):

#         self.sign_up()
#         user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
#             data=json.dumps(self.user_login_data))
#         self.assertEqual(user_login.status_code, 200)
#         response = json.loads(user_login.data)
#         self.assertEqual(response['message'], 'login successful')
#         token = response['auth_token']
#         self.app_client.put('/api/v1/users/cancel/1',content_type='application/json',
#                                 headers={'Authorization': f'Bearer {token}'})

#         update_name = self.app_client.put("api/v1/users/delete/1", content_type="application/json", 
#              headers={'Authorization': f'Bearer {token}'})

#         self.assertEqual(update_name.status_code, 404)
#         response = json.loads(update_name.data) 
#         self.assertEqual(response['message'], 'Account has been deactivated')
    
#     def test_cant_delete_user_for_nonexistent_user(self):

#         self.sign_up()
#         user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
#             data=json.dumps(self.user_login_data))
#         self.assertEqual(user_login.status_code, 200)
#         response = json.loads(user_login.data)
#         self.assertEqual(response['message'], 'login successful')
#         token = response['auth_token']

#         update_name = self.app_client.put("api/v1/users/delete/5", content_type="application/json", 
#             data=json.dumps({"user_role": "admin"}), headers={'Authorization': f'Bearer {token}'})
            
#         self.assertEqual(update_name.status_code, 404)
#         response = json.loads(update_name.data) 
#         self.assertEqual(response['message'], 'The user with that id doesnt exist')

# #     def test_cant_delete_user_if_missing_access_rights(self):

# #         self.sign_up()
# #         user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
# #             data=json.dumps(self.user_login_data))
# #         self.assertEqual(user_login.status_code, 200)
# #         response = json.loads(user_login.data)
# #         self.assertEqual(response['message'], 'login successful')
# #         token = response['auth_token']

# #         create_user1= self.app_client.post("/api/v1/auth/signup", content_type='application/json', 
# #             data=json.dumps(self.user1))
        
# #         update_name = self.app_client.put("api/v1/users/delete/2", content_type="application/json", 
# #             data=json.dumps({"user_role" : "admin"}), headers={'Authorization': f'Bearer {token}'})

# #         self.assertEqual(update_name.status_code, 400)
# #         response = json.loads(update_name.data) 
# #         self.assertEqual(response['message'], 'Unauthorised access')

    

# #     #############################################################################################
# #     #                                                                                           #
# #     #                             UPDATE PASSWORD TESTCASES                                     #
# #     #                                                                                           #
# #     #############################################################################################
#     def test_can_update_password_successfully(self):

#         self.sign_up()
        
#         update = self.app_client.post("/api/v1/auth/forgot_password", content_type="application/json", 
#             data=json.dumps(self.user_login_data3))

#         self.assertEqual(update.status_code, 200)
#         response = json.loads(update.data) 
#         self.assertEqual(response['message'], 'password successfully updated')

#     def test_cant_update_password_for_deactivated_account(self):
    
#         self.sign_up()

#         user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
#             data=json.dumps(self.user_login_data))
        
#         response = json.loads(user_login.data)
#         token = response['auth_token']

#         cancel = self.app_client.put('/api/v1/users/cancel/2',content_type='application/json',
#                                 headers={'Authorization': f'Bearer {token}'})

#         update = self.app_client.post("/api/v1/auth/forgot_password", content_type="application/json", 
#             data=json.dumps(self.user_login_data3))
        
#         response = json.loads(update.data) 
#         self.assertEqual(response['message'], 'Account has been deactivated')
#         self.assertEqual(update.status_code, 400)

#     def test_cant_update_password_for_nonexistent_user(self):

#         update = self.app_client.post("/api/v1/auth/forgot_password", content_type="application/json", 
#             data=json.dumps(self.user_login_data4))
        
#         response = json.loads(update.data) 
#         self.assertEqual(update.status_code, 404)
#         self.assertEqual(response['message'], 'User with that email doesnot exist')

#     def test_cant_update_password_with_missing_data(self):

#         update = self.app_client.post("/api/v1/auth/forgot_password", content_type="application/json", data=json.dumps(self.user_login_data7))
        
#         response = json.loads(update.data) 
#         self.assertEqual(update.status_code, 400)
#         self.assertEqual(response['message'], 'Some fields are missing')
    
#     def test_cant_update_password_for_user_with_invalid_password(self):

#         update = self.app_client.post("/api/v1/auth/forgot_password", content_type="application/json", 
#             data=json.dumps(self.user_login_data5))
        
#         response = json.loads(update.data) 
#         self.assertEqual(update.status_code, 400)
#         self.assertEqual(response['message'], 'invalid email')

#     def test_cant_update_password_for_user_with_invalid_email(self):

#         update = self.app_client.post("/api/v1/auth/forgot_password", content_type="application/json", 
#             data=json.dumps(self.user_login_data6))
        
#         response = json.loads(update.data) 
#         self.assertEqual(update.status_code, 400)
#         self.assertEqual(response['message'], 'invalid password')

   

# if "__name__" == "__main__":
#     unittest.main()
