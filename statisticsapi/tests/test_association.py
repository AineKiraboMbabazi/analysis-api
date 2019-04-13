import json
import unittest
from statisticsapi import app
from statisticsapi.routes.associations import Association
from statisticsapi import app
from statisticsapi.routes.auth import Auth
from statisticsapi.routes.users import User
from statisticsapi.routes.government import Government_Controller
from statisticsapi.controllers.database import DatabaseConnection
from .test_base import TestBase


class TestAssociation(TestBase):
    #############################################################################################
    #                                                                                           #
    #                                INDEX TESTCASES                                            #
    #                                                                                           #
    #############################################################################################
    def test_index(self):

        index = self.app_client.get("/index", content_type="application/json")
        self.assertEqual(index.status_code, 200)
        response = json.loads(index.data)
        self.assertEqual(response['message'], 'Welcome to statistics API')

    def test_index1(self):
     
        index = self.app_client.get("/", content_type="application/json")
        self.assertEqual(index.status_code, 200)
        response = json.loads(index.data)
        self.assertEqual(response['message'], 'Welcome to statistics API')

    #############################################################################################
    #                                                                                           #
    #                               CREATE ASSOCIATION TESTCASES                                #
    #                                                                                           #
    #############################################################################################

    def test_can_create_association_successfully(self):

        self.sign_up()
        token = self.user_login()
        association = self.app_client.post("/api/v1/associations", content_type="application/json", 
            data=json.dumps(self.association_data), headers={'Authorization': f'Bearer {token}'})
            
        self.assertEqual(association.status_code, 201)
        response = json.loads(association.data)
        self.assertEqual(response['message'], "Your association has been created")
        self.assertEqual(response['association'],
        {
        "name": "Agribus",
        "Location": "Uganda"
        })

    def test_cant_create_association_with_missing_fields(self):

        self.sign_up()
        token = self.user_login()
        association = self.app_client.post("/api/v1/associations", content_type="application/json", 
            data=json.dumps(self.association_with_missing_fields), headers = {'Authorization': f'Bearer {token}'})

        self.assertEqual(association.status_code, 400)
        response = json.loads(association.data)
        self.assertEqual(response['message'], "Some fields are missing")
        
    def test_cant_create_association_with_missing_token(self):

        self.sign_up()
        token = self.user_login()
        association = self.app_client.post("/api/v1/associations", content_type="application/json", 
            data=json.dumps(self.association_with_missing_fields))

        self.assertEqual(association.status_code, 401)
        response = json.loads(association.data)
        self.assertEqual(response['msg'], "Missing Authorization Header")
        
    def test_cant_create_association_with_inactivated_account(self):

        self.sign_up()
        token = self.user_login()

        self.app_client.put('/api/v1/users/delete/1',content_type='application/json',
                                headers={'Authorization': f'Bearer {token}'})
        
        association = self.app_client.post("/api/v1/associations", content_type="application/json", 
            data=json.dumps(self.association_data), headers={'Authorization': f'Bearer {token}'})
        
        self.assertEqual(association.status_code, 400)
        response = json.loads(association.data)
        self.assertEqual(response['message'], "The user account has been deactivated")
        
    def test_cant_create_association_with_invalid_name(self):

        self.sign_up()
        token = self.user_login()

        association = self.app_client.post("/api/v1/associations", content_type="application/json", 
            data=json.dumps(self.association_with_invalid_name), headers={'Authorization': f'Bearer {token}'})

        self.assertEqual(association.status_code, 400)
        response = json.loads(association.data)
        self.assertEqual(response['message'], "Name field should contain strings ")
        
    def test_cant_create_association_with_duplicate_name(self):

        self.sign_up()
        token = self.user_login()
        self.app_client.post("/api/v1/associations", content_type="application/json", 
            data=json.dumps(self.association_data), headers={'Authorization': f'Bearer {token}'})

        association = self.app_client.post("/api/v1/associations", content_type="application/json", 
            data=json.dumps(self.association_data), headers={'Authorization': f'Bearer {token}'})

        self.assertEqual(association.status_code, 400)
        response = json.loads(association.data)
        self.assertEqual(response['message'], "An association with that name already exists")

    def test_cant_create_association_with_invalid_location(self):

        self.sign_up()
        token = self.user_login()

        association = self.app_client.post("/api/v1/associations", content_type="application/json", 
            data=json.dumps(self.association_with_invalid_location), headers={'Authorization': f'Bearer {token}'})

        self.assertEqual(association.status_code, 400)
        response = json.loads(association.data)
        self.assertEqual(response['message'], "location Field should contain strings ")


    #############################################################################################
    #                                                                                           #
    #                               FETCH ALL ASSOCIATIONs TESTCASES                            #
    #                                                                                           #
    #############################################################################################

    def test_can_get_all_associations(self):
        self.sign_up_superadmin()
        token = self.superadmin_login()

        create = self.app_client.post("/api/v1/associations", content_type="application/json", 
            data=json.dumps(self.association_data), headers={'Authorization': f'Bearer {token}'})

        self.assertEqual(create.status_code, 201)
        association = self.app_client.get("/api/v1/associations", content_type="application/json", headers={'Authorization': f'Bearer {token}'})

        self.assertEqual(association.status_code, 200)
        response = json.loads(association.data)
        self.assertEqual(len(response),1)
        
    def test_cant_get_all_associations_without_token(self):
        self.sign_up_superadmin()
        token = self.superadmin_login()

        create = self.app_client.post("/api/v1/associations", content_type="application/json", 
            data=json.dumps(self.association_data), headers={'Authorization': f'Bearer {token}'})

        self.assertEqual(create.status_code, 201)
        association = self.app_client.get("/api/v1/associations", content_type="application/json")

        self.assertEqual(association.status_code, 401)
        response = json.loads(association.data)
        self.assertEqual(response['msg'], "Missing Authorization Header")

    def test_cant_get_empty_associations(self):
        self.sign_up_superadmin()
        token = self.superadmin_login()

        association = self.app_client.get("/api/v1/associations", content_type="application/json", headers={'Authorization': f'Bearer {token}'})
        
        self.assertEqual(association.status_code, 404)
        response = json.loads(association.data)
        self.assertEqual(response['message'],'No associations found')

    def test_cant_get_empty_associations_with_inactive_account(self):
        self.sign_up_superadmin()

        token = self.superadmin_login()
        self.app_client.put("/api/v1/users/", content_type="application/json", headers={'Authorization': f'Bearer {token}'})

        association = self.app_client.get("/api/v1/associations", content_type="application/json", headers={'Authorization': f'Bearer {token}'})
        
        self.assertEqual(association.status_code, 404)
        response = json.loads(association.data)
        self.assertEqual(response['message'],'No associations found')
        
    def test_cant_get_associations_as_government(self):
        self.sign_up_government()
        token = self.user_login_government_user()
        self.app_client.post("/api/v1/governments", content_type='application/json', 
            data=json.dumps({
                "name": "Ugandan",
                "Location": "Uganda"}), headers ={'Authorization': f'Bearer {token}'} )

        association = self.app_client.get("/api/v1/associations", content_type="application/json", headers={'Authorization': f'Bearer {token}'})
        
        self.assertEqual(association.status_code, 404)
        response = json.loads(association.data)
        self.assertEqual(response['message'], "No associations found")

    def test_can_get_associations_as_government(self):
        self.sign_up_government()
        token = self.user_login_government_user()
        create = self.app_client.post("/api/v1/associations", content_type="application/json", 
            data=json.dumps(self.association_data), headers={'Authorization': f'Bearer {token}'})

        self.app_client.post("/api/v1/governments", content_type='application/json', 
            data=json.dumps({
                "name": "Ugandan",
                "Location": "Uganda"}), headers ={'Authorization': f'Bearer {token}'} )

        association = self.app_client.get("/api/v1/associations", content_type="application/json", headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(association.status_code, 200)
        response = json.loads(association.data)
        

    def test_cant_get_associations_without_authorisation(self):
        self.sign_up()
        token = self.user_login()

        association = self.app_client.get("/api/v1/associations", content_type="application/json", headers={'Authorization': f'Bearer {token}'})
        
        self.assertEqual(association.status_code, 400)
        response = json.loads(association.data)
        self.assertEqual(response['message'], "Unauthorised access")
        
    # ############################################################################################
    #                                                                                           #
    #                          FETCH PENDINIG ASSOCIATIONS TESTCASES                            #
    #                                                                                           #
    # ############################################################################################
    def test_can_get_all_pending_associations(self):
        self.sign_up_superadmin()
        self.sign_up()
        token = self.user_login()
        token1 = self.superadmin_login()

        create = self.app_client.post("/api/v1/associations", content_type="application/json", 
            data=json.dumps(self.association_data), headers={'Authorization': f'Bearer {token}'})

        self.assertEqual(create.status_code, 201)
        association = self.app_client.get("/api/v1/associations/pending", content_type="application/json", headers={'Authorization': f'Bearer {token1}'})

        self.assertEqual(association.status_code, 200)
        response = json.loads(association.data)
        self.assertEqual(len(response),1)
        
    
    def test_cant_get_pending_associations_with_inactive_account(self):
        self.sign_up_superadmin()

        token = self.superadmin_login()
        self.app_client.put('/api/v1/users/delete/1',content_type='application/json',
                                headers={'Authorization': f'Bearer {token}'})


        association = self.app_client.get("/api/v1/associations/pending", content_type="application/json", headers={'Authorization': f'Bearer {token}'})

        association = self.app_client.get("/api/v1/associations/pending", content_type="application/json", headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(association.status_code, 400)
        response = json.loads(association.data)
        self.assertEqual(response['message'], 'Trying to edit association using a deactivated account')
        
    def test_cant_get_pending_associations_without_token(self):
        self.sign_up_superadmin()

        token = self.superadmin_login()

        association = self.app_client.get("/api/v1/associations/pending", content_type="application/json")

        self.assertEqual(association.status_code, 401)
        response = json.loads(association.data)
        self.assertEqual(response['msg'], 'Missing Authorization Header')
        
    def test_cant_get_pending_associations_without_token(self):
        self.sign_up_superadmin()

        token = self.superadmin_login()

        association = self.app_client.get("/api/v1/associations/pending", content_type="application/json", headers={'Authorization': f'Bearer {token}'})

        self.assertEqual(association.status_code, 404)
        response = json.loads(association.data)
        self.assertEqual(response['message'], 'No pending associations found ')
        
    def test_can_get_all_pending_associations_without_acess_rights(self):
        self.sign_up_superadmin()
        self.sign_up()
        token = self.user_login()
        token1 = self.superadmin_login()

        create = self.app_client.post("/api/v1/associations", content_type="application/json", 
            data=json.dumps(self.association_data), headers={'Authorization': f'Bearer {token}'})

        self.assertEqual(create.status_code, 201)
        association = self.app_client.get("/api/v1/associations/pending", content_type="application/json", headers={'Authorization': f'Bearer {token}'})

        self.assertEqual(association.status_code, 400)
        response = json.loads(association.data)
        self.assertEqual(response['message'], 'Unauthorised access')


    #############################################################################################
    #                                                                                           #
    #                          FETCH specific ASSOCIATIONS TESTCASES                            #
    #                                                                                           #
    #############################################################################################
    def test_can_get_specific_association(self):
        self.sign_up()
        token = self.user_login()

        create = self.app_client.post("/api/v1/associations", content_type="application/json", 
            data=json.dumps(self.association_data), headers={'Authorization': f'Bearer {token}'})

        association = self.app_client.get("/api/v1/associations/1", content_type="application/json")

        self.assertEqual(association.status_code, 200)
        response = json.loads(association.data)
        self.assertEqual(len(response),1)
        
    
    def test_cant_get_association_with_nonexistent_id(self):
        self.sign_up()
        token = self.user_login()

        association = self.app_client.get("/api/v1/associations/1", content_type="application/json")

        self.assertEqual(association.status_code, 404)
        response = json.loads(association.data)
        self.assertEqual(response['message'], 'association with that id doesnot exist')
        
    #############################################################################################
    #                                                                                           #
    #                          CANCEL specific ASSOCIATIONS TESTCASES                           #
    #                                                                                           #
    #############################################################################################
    def test_can_cancel_specific_association(self):
        self.sign_up_superadmin()
        token = self.superadmin_login()

        create = self.app_client.post("/api/v1/associations", content_type="application/json", 
            data=json.dumps(self.association_data), headers={'Authorization': f'Bearer {token}'})

        association = self.app_client.put("/api/v1/associations/cancel/1", content_type="application/json", headers={'Authorization': f'Bearer {token}'})
        
        self.assertEqual(association.status_code, 200)
        response = json.loads(association.data)
        self.assertEqual(response['message'], 'Your association has been cancelled')
        
    
    def test_cant_cancel_association_without_token(self):
        self.sign_up_superadmin()
        token = self.superadmin_login()

        create = self.app_client.post("/api/v1/associations", content_type="application/json", 
            data=json.dumps(self.association_data), headers={'Authorization': f'Bearer {token}'})

        association = self.app_client.put("/api/v1/associations/cancel/1", content_type="application/json")

        self.assertEqual(association.status_code, 401)
        response = json.loads(association.data)
        self.assertEqual(response['msg'], 'Missing Authorization Header')
        

    def test_cant_cancel_nonexistent_association(self):
        self.sign_up_superadmin()
        token = self.superadmin_login()

        create = self.app_client.post("/api/v1/associations", content_type="application/json",             data=json.dumps(self.association_data), headers={'Authorization': f'Bearer {token}'})

        association = self.app_client.put("/api/v1/associations/cancel/2", content_type="application/json", headers={'Authorization': f'Bearer {token}'})

        self.assertEqual(association.status_code, 404)
        response = json.loads(association.data)
        self.assertEqual(response['message'], 'Association with that id doesnt exist')
        
    def test_cant_cancel_inactive_association(self):
        self.sign_up_superadmin()
        token = self.superadmin_login()

        create = self.app_client.post("/api/v1/associations", content_type="application/json", 
            data=json.dumps(self.association_data), headers={'Authorization': f'Bearer {token}'})

        self.app_client.put("/api/v1/associations/delete/1", content_type="application/json", headers={'Authorization': f'Bearer {token}'})
        association = self.app_client.put("/api/v1/associations/cancel/1", content_type="application/json", headers={'Authorization': f'Bearer {token}'})
        
        self.assertEqual(association.status_code, 400)
        response = json.loads(association.data)
        self.assertEqual(response['message'], 'Cant update an inactive association ')
        

    def test_cant_cancel_association_with_inactive_users(self):
        self.sign_up_superadmin()
        token = self.superadmin_login()

        create = self.app_client.post("/api/v1/associations", content_type="application/json", 
            data=json.dumps(self.association_data), headers={'Authorization': f'Bearer {token}'})

        self.app_client.put("/api/v1/users/delete/1", content_type="application/json", headers={'Authorization': f'Bearer {token}'})

        association = self.app_client.put("/api/v1/associations/cancel/1", content_type="application/json", headers={'Authorization': f'Bearer {token}'})

        self.assertEqual(association.status_code, 400)
        response = json.loads(association.data)
        self.assertEqual(response['message'], 'Trying to edit association using a deactivated account')
    
    def test_cant_cancel_association_without_admin_rights(self):
        self.sign_up()
        token = self.user_login()

        create = self.app_client.post("/api/v1/associations", content_type="application/json", 
            data=json.dumps(self.association_data), headers={'Authorization': f'Bearer {token}'})

        association = self.app_client.put("/api/v1/associations/cancel/1", content_type="application/json", headers={'Authorization': f'Bearer {token}'})

        self.assertEqual(association.status_code, 400)
        response = json.loads(association.data)
        self.assertEqual(response['message'], 'unauthorised access')
        

    #############################################################################################
    #                                                                                           #
    #                            UPDATE ASSOCIATION TESTCASES                                   #
    #                                                                                           #
    #############################################################################################

    def test_can_update_association_successfully(self):

        self.sign_up_superadmin()
        token = self.superadmin_login()
        self.app_client.post("/api/v1/associations", content_type="application/json", 
            data=json.dumps(self.association_data), headers = {'Authorization': f'Bearer {token}'})
        association = self.app_client.put("/api/v1/associations/name/1", content_type="application/json", 
            data=json.dumps(self.update_name_data), headers = {'Authorization': f'Bearer {token}'})
        
        self.assertEqual(association.status_code, 200)
        response = json.loads(association.data)
        self.assertEqual(response['message'], "Your name has been updated ")
    
    def test_cant_update_association_without_token(self):

        self.sign_up()
        token = self.user_login()
        self.app_client.post("/api/v1/associations", content_type="application/json", 
            data=json.dumps(self.association_data), headers = {'Authorization': f'Bearer {token}'})
        association = self.app_client.put("/api/v1/associations/name/1", content_type="application/json", 
            data=json.dumps(self.update_name_data))

        self.assertEqual(association.status_code, 401)
        response = json.loads(association.data)
        self.assertEqual(response['msg'], 'Missing Authorization Header')

    def test_cant_update_association_with_missing_fields(self):

        self.sign_up()
        token = self.user_login()
        self.app_client.post("/api/v1/associations", content_type="application/json", 
            data=json.dumps(self.association_data), headers = {'Authorization': f'Bearer {token}'})
        association = self.app_client.put("/api/v1/associations/name/1", content_type="application/json", 
            data=json.dumps(self.update_name_data1), headers = {'Authorization': f'Bearer {token}'})

        self.assertEqual(association.status_code, 400)
        response = json.loads(association.data)
        self.assertEqual(response['message'], 'Some fields are missing')
        
    def test_cant_update_association_with_invalid_name(self):

        self.sign_up()
        token = self.user_login()
        self.app_client.post("/api/v1/associations", content_type="application/json", 
            data=json.dumps(self.association_data), headers = {'Authorization': f'Bearer {token}'})
        association = self.app_client.put("/api/v1/associations/name/1", content_type="application/json", 
            data=json.dumps(self.update_name_data2), headers = {'Authorization': f'Bearer {token}'})

        self.assertEqual(association.status_code, 400)
        response = json.loads(association.data)
        self.assertEqual(response['message'], 'name must be a non empty string')
        
    def test_cant_update_association_with_missing_association(self):

        self.sign_up()
        token = self.user_login()
   
        association = self.app_client.put("/api/v1/associations/name/1", content_type="application/json", 
            data=json.dumps(self.update_name_data), headers = {'Authorization': f'Bearer {token}'})

        self.assertEqual(association.status_code, 404)
        response = json.loads(association.data)
        self.assertEqual(response['message'], 'association not found')
        
    def test_cant_update_association_with_inactive_account(self):

        self.sign_up()
        token = self.user_login()
        self.app_client.post("/api/v1/associations", content_type="application/json", 
            data=json.dumps(self.association_data), headers={'Authorization': f'Bearer {token}'})

        self.app_client.put("/api/v1/users/delete/1", content_type="application/json", headers={'Authorization': f'Bearer {token}'})

        association = self.app_client.put("/api/v1/associations/name/1", content_type="application/json", 
            data=json.dumps(self.update_name_data), headers = {'Authorization': f'Bearer {token}'})
       
        self.assertEqual(association.status_code, 400)
        response = json.loads(association.data)
        self.assertEqual(response['message'], 'user account inactive')

    def test_cant_update_updated_association(self):

        self.sign_up_superadmin()
        token = self.superadmin_login()
        self.app_client.post("/api/v1/associations", content_type="application/json", 
            data=json.dumps(self.association_data), headers={'Authorization': f'Bearer {token}'})
       
        self.app_client.put("/api/v1/associations/name/1", content_type="application/json", 
            data=json.dumps(self.update_name_data), headers={'Authorization': f'Bearer {token}'})

        association = self.app_client.put("/api/v1/associations/name/1", content_type="application/json", 
            data=json.dumps(self.update_name_data), headers = {'Authorization': f'Bearer {token}'})
        self.assertEqual(association.status_code, 400)
        response = json.loads(association.data)
        self.assertEqual(response['message'], 'The name is already upto date')

    def test_cant_update_association_name_without_authorisation(self):

        self.sign_up_superadmin()
        token = self.superadmin_login()
        self.app_client.post("/api/v1/associations", content_type="application/json", 
            data=json.dumps(self.association_data), headers={'Authorization': f'Bearer {token}'})
        
        self.sign_up()
        token = self.user_login()
        association = self.app_client.put("/api/v1/associations/name/1", content_type="application/json", 
            data=json.dumps(self.update_name_data), headers={'Authorization': f'Bearer {token}'})
        
       
        self.assertEqual(association.status_code, 400)
        response = json.loads(association.data)
        self.assertEqual(response['message'], 'unauthorised access')


    #############################################################################################
    #                                                                                           #
    #                            DELETE ASSOCIATION TESTCASES                                   #
    #                                                                                           #
    #############################################################################################

    def test_can_delete_association_successfully(self):

        self.sign_up_superadmin()
        token = self.superadmin_login()
        self.app_client.post("/api/v1/associations", content_type="application/json", 
            data=json.dumps(self.association_data), headers = {'Authorization': f'Bearer {token}'})
        association = self.app_client.put("/api/v1/associations/delete/1", content_type="application/json", 
            data=json.dumps(self.update_name_data), headers = {'Authorization': f'Bearer {token}'})
        
        self.assertEqual(association.status_code, 200)
        response = json.loads(association.data)
        self.assertEqual(response['message'], "Your association has been deleted")

    def test_cant_delete_association_without_token(self):

        self.sign_up_superadmin()
        token = self.superadmin_login()
        self.app_client.post("/api/v1/associations", content_type="application/json", 
            data=json.dumps(self.association_data), headers = {'Authorization': f'Bearer {token}'})
        association = self.app_client.put("/api/v1/associations/delete/1", content_type="application/json", 
            data=json.dumps(self.update_name_data))
        
        self.assertEqual(association.status_code, 401)
        response = json.loads(association.data)
        self.assertEqual(response['msg'], "Missing Authorization Header")

    def test_cant_delete_association_which_doesnt_exist(self):

        self.sign_up_superadmin()
        token = self.superadmin_login()
        self.app_client.post("/api/v1/associations", content_type="application/json", 
            data=json.dumps(self.association_data), headers = {'Authorization': f'Bearer {token}'})
        association = self.app_client.put("/api/v1/associations/delete/2", content_type="application/json", 
            data=json.dumps(self.update_name_data), headers = {'Authorization': f'Bearer {token}'})
        
        self.assertEqual(association.status_code, 404)
        response = json.loads(association.data)
        self.assertEqual(response['message'], "The association doesnt exist")

    def test_cant_delete_association_which_doesnt_exist(self):

        self.sign_up_superadmin()
        token = self.superadmin_login()
        self.app_client.post("/api/v1/associations", content_type="application/json", 
            data=json.dumps(self.association_data), headers={'Authorization': f'Bearer {token}'})

        self.app_client.put("/api/v1/associations/delete/1", content_type="application/json", 
            data=json.dumps(self.update_name_data), headers={'Authorization': f'Bearer {token}'})
            
        association = self.app_client.put("/api/v1/associations/delete/1", content_type="application/json", 
            data=json.dumps(self.update_name_data), headers = {'Authorization': f'Bearer {token}'})
        
        self.assertEqual(association.status_code, 400)
        response = json.loads(association.data)
        self.assertEqual(response['message'], "Cant update an inactive association ")

    def test_cant_delete_association_with_non_exist_user_account(self):

        self.sign_up_superadmin()
        token = self.superadmin_login()
        self.app_client.post("/api/v1/associations", content_type="application/json", 
            data=json.dumps(self.association_data), headers={'Authorization': f'Bearer {token}'})

        self.app_client.put("/api/v1/users/delete/1", content_type="application/json", headers={'Authorization': f'Bearer {token}'})
            
        association = self.app_client.put("/api/v1/associations/delete/1", content_type="application/json", 
            data=json.dumps(self.update_name_data), headers = {'Authorization': f'Bearer {token}'})
        
        self.assertEqual(association.status_code, 404)
        response = json.loads(association.data)
        self.assertEqual(response['message'], "user with id not found")

    
    def test_cant_delete_association_without_authorisation(self):

        self.sign_up_superadmin()
        token = self.superadmin_login()
        self.app_client.post("/api/v1/associations", content_type="application/json", 
            data=json.dumps(self.association_data), headers={'Authorization': f'Bearer {token}'})
        self.sign_up()
        token = self.user_login()
        association = self.app_client.put("/api/v1/associations/delete/1", content_type="application/json", 
            data=json.dumps(self.update_name_data), headers = {'Authorization': f'Bearer {token}'})
        
        self.assertEqual(association.status_code, 400)
        response = json.loads(association.data)
        self.assertEqual(response['message'], "unauthorised access")

    #############################################################################################
    #                                                                                           #
    #                            APPROVE ASSOCIATION TESTCASES                                  #
    #                                                                                           #
    #############################################################################################
    def test_can_approve_association_successfully(self):

        self.sign_up_superadmin()
        token = self.superadmin_login()
        self.app_client.post("/api/v1/associations", content_type="application/json", 
            data=json.dumps(self.association_data), headers={'Authorization': f'Bearer {token}'})
     
        association = self.app_client.put("/api/v1/associations/approve/1", content_type="application/json", 
            data=json.dumps(self.update_name_data), headers = {'Authorization': f'Bearer {token}'})
        self.assertEqual(association.status_code, 200)
        response = json.loads(association.data)
        self.assertEqual(response['message'], "The association has been approved")

    def test_cant_approve_association_without_authorisation(self):

        self.sign_up_superadmin()
        token = self.superadmin_login()
        self.app_client.post("/api/v1/associations", content_type="application/json", 
            data=json.dumps(self.association_data), headers={'Authorization': f'Bearer {token}'})
        self.sign_up()
        token = self.user_login()
        association = self.app_client.put("/api/v1/associations/approve/1", content_type="application/json", 
            data=json.dumps(self.update_name_data), headers = {'Authorization': f'Bearer {token}'})
        self.assertEqual(association.status_code, 400)
        response = json.loads(association.data)
        self.assertEqual(response['message'], "unauthorised access")

    def test_cant_approve_association_which_is_upto_date(self):

        self.sign_up_superadmin()
        token = self.superadmin_login()
        self.app_client.post("/api/v1/associations", content_type="application/json",data=json.dumps(self.association_data), headers={'Authorization': f'Bearer {token}'})

        self.app_client.put("/api/v1/associations/approve/1", content_type="application/json",data=json.dumps(self.update_name_data), headers={'Authorization': f'Bearer {token}'})
            
        association = self.app_client.put("/api/v1/associations/approve/1", content_type="application/json", 
            data=json.dumps(self.update_name_data), headers={'Authorization': f'Bearer {token}'})
            
        self.assertEqual(association.status_code, 400)
        response = json.loads(association.data)
        self.assertEqual(response['message'], "The association is already approved")


    def test_cant_approve_association_without_token(self):

        self.sign_up_superadmin()
        token = self.superadmin_login()
        self.app_client.post("/api/v1/associations", content_type="application/json", 
            data=json.dumps(self.association_data), headers={'Authorization': f'Bearer {token}'})
     
        association = self.app_client.put("/api/v1/associations/approve/1", content_type="application/json" )
        self.assertEqual(association.status_code, 401)
        response = json.loads(association.data)
        self.assertEqual(response['msg'], "Missing Authorization Header")