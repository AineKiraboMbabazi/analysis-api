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


class TestGovernment(TestBase):


    #############################################################################################
    #                                                                                           #
    #                               GOVERNMENT ASSOCIATION TESTCASES                            #
    #                                                                                           #
    #############################################################################################

    def test_can_create_government_successfully(self):

        self.sign_up()
        token = self.user_login()
        government = self.app_client.post("/api/v1/governments", content_type='application/json', 
            data=json.dumps({
                "name": "Ugandan",
                "Location": "Uganda"}), headers ={'Authorization': f'Bearer {token}'} )

        self.assertEqual(government.status_code, 201)
        
        response = json.loads(government.data)
        self.assertEqual(response['message'], 'Your government has been created')
        self.assertEqual(response['government'], {
            "name": "Ugandan",
            "Location": "Uganda"
            })
    def test_cant_create_government_with_missing_fields(self):

        self.sign_up()
        token = self.user_login()
        government = self.app_client.post("/api/v1/governments", content_type="application/json", 
            data=json.dumps({
            "name": "Ugandan"}), headers = {'Authorization': f'Bearer {token}'})

        self.assertEqual(government.status_code, 400)
        response = json.loads(government.data)
        self.assertEqual(response['message'], "Some fields are missing")
        
    def test_cant_create_government_with_missing_token(self):

        self.sign_up()
        token = self.user_login()
        government = self.app_client.post("/api/v1/associations", content_type="application/json", 
            data=json.dumps({
            "name": "Ugandan",
            "Location": "Uganda"
            }))

        self.assertEqual(government.status_code, 401)
        response = json.loads(government.data)
        self.assertEqual(response['msg'], "Missing Authorization Header")
        
    def test_cant_create_government_with_inactivated_account(self):

        self.sign_up()
        token = self.user_login()

        self.app_client.put('/api/v1/users/delete/1',content_type='application/json',
                                headers={'Authorization': f'Bearer {token}'})
       
        government = self.app_client.post("/api/v1/governments", content_type="application/json", 
            data=json.dumps({
            "name": "Ugandan",
            "Location": "Uganda"
            }), headers={'Authorization': f'Bearer {token}'})
        
        self.assertEqual(government.status_code, 400)
        response = json.loads(government.data)
        self.assertEqual(response['message'], "User account has been deactivated")
        
    def test_cant_create_government_with_invalid_name(self):

        self.sign_up()
        token = self.user_login()

        government = self.app_client.post("/api/v1/governments", content_type="application/json", 
            data=json.dumps({
            "name": "12345",
            "Location": "Uganda"
            }), headers={'Authorization': f'Bearer {token}'})

        self.assertEqual(government.status_code, 400)
        response = json.loads(government.data)
        self.assertEqual(response['message'], "Name field should contain strings ")
        
    def test_cant_create_government_with_duplicate_name(self):

        self.sign_up()
        token = self.user_login()
        self.app_client.post("/api/v1/governments", content_type="application/json", 
            data=json.dumps({
            "name": "Ugandan",
            "Location": "Uganda"
            }), headers={'Authorization': f'Bearer {token}'})

        government = self.app_client.post("/api/v1/governments", content_type="application/json", 
            data=json.dumps({
            "name": "Ugandan",
            "Location": "Uganda"
            }), headers={'Authorization': f'Bearer {token}'})

        self.assertEqual(government.status_code, 400)
        response = json.loads(government.data)
        self.assertEqual(response['message'], "A government with that name already exists")

    def test_cant_create_government_with_invalid_location(self):

        self.sign_up()
        token = self.user_login()

        government = self.app_client.post("/api/v1/governments", content_type="application/json", 
            data=json.dumps({
            "name": "Ugandan",
            "Location": "12233"
            }), headers={'Authorization': f'Bearer {token}'})

        self.assertEqual(government.status_code, 400)
        response = json.loads(government.data)
        self.assertEqual(response['message'], "Location field should contain strings ")


    # #############################################################################################
    # #                                                                                           #
    # #                               FETCH ALL GOVERNMENTS TESTCASES                             #
    # #                                                                                           #
    # #############################################################################################

    def test_can_get_all_governments(self):
        self.sign_up_superadmin()
        token = self.superadmin_login()

        create = self.app_client.post("/api/v1/governments", content_type="application/json", 
            data=json.dumps({
            "name": "Ugandan",
            "Location": "Uganda"
            }), headers={'Authorization': f'Bearer {token}'})

        self.assertEqual(create.status_code, 201)
        government = self.app_client.get("/api/v1/governments", content_type="application/json", headers={'Authorization': f'Bearer {token}'})

        self.assertEqual(government.status_code, 200)
        response = json.loads(government.data)
        self.assertEqual(len(response),1)
        
    def test_cant_get_all_governments_without_token(self):
        self.sign_up_superadmin()
        token = self.superadmin_login()

        create = self.app_client.post("/api/v1/governments", content_type="application/json", 
            data=json.dumps({
            "name": "Ugandan",
            "Location": "Uganda"
            }), headers={'Authorization': f'Bearer {token}'})

        self.assertEqual(create.status_code, 201)
        government = self.app_client.get("/api/v1/governments", content_type="application/json")

        self.assertEqual(government.status_code, 401)
        response = json.loads(government.data)
        self.assertEqual(response['msg'], "Missing Authorization Header")

    def test_cant_get_empty_governments(self):
        self.sign_up_superadmin()
        token = self.superadmin_login()

        government = self.app_client.get("/api/v1/governments", content_type="application/json", headers={'Authorization': f'Bearer {token}'})
        
        self.assertEqual(government.status_code, 404)
        response = json.loads(government.data)
        self.assertEqual(response['message'],'No governments found')

    def test_cant_get_empty_government_with_inactive_account(self):
        self.sign_up_superadmin()

        token = self.superadmin_login()
        self.app_client.put("/api/v1/users/delete/1", content_type="application/json", headers={'Authorization': f'Bearer {token}'})

        government = self.app_client.get("/api/v1/governments", content_type="application/json", headers={'Authorization': f'Bearer {token}'})
        
        self.assertEqual(government.status_code, 404)
        response = json.loads(government.data)
        self.assertEqual(response['message'],'No governments found')
        
    # # def test_can_get_associations_as_government(self):
    # #     self.sign_up_government()
    # #     token = self.user_login_government_user()

    # #     association = self.app_client.get("/api/v1/associations", content_type="application/json", headers={'Authorization': f'Bearer {token}'})
        
    # #     self.assertEqual(association.status_code, 200)
    # #     response = json.loads(association.data)

    def test_cant_get_governments_without_authorisation(self):
        self.sign_up()
        token = self.user_login()

        government = self.app_client.get("/api/v1/governments", content_type="application/json", headers={'Authorization': f'Bearer {token}'})
        
        self.assertEqual(government.status_code, 400)
        response = json.loads(government.data)
        self.assertEqual(response['message'], "Unauthorised access")
        
    #############################################################################################
    #                                                                                           #
    #                          FETCH PENDINIG governmentS TESTCASES                             #
    #                                                                                           #
    #############################################################################################
    def test_can_get_all_pending_governments(self):
        self.sign_up_superadmin()
        self.sign_up()
        token = self.user_login()
        token1 = self.superadmin_login()

        create = self.app_client.post("/api/v1/governments", content_type="application/json", 
            data=json.dumps({
            "name": "Ugandan",
            "Location": "Uganda"
            }), headers={'Authorization': f'Bearer {token}'})

        self.assertEqual(create.status_code, 201)
        government = self.app_client.get("/api/v1/governments/pending", content_type="application/json", headers={'Authorization': f'Bearer {token1}'})
       

        self.assertEqual(government.status_code, 200)
        response = json.loads(government.data)
        self.assertEqual(len(response),1)
        
    
    def test_cant_get_pending_governments_with_inactive_account(self):
        self.sign_up_superadmin()

        token = self.superadmin_login()
        self.app_client.put('/api/v1/users/delete/1',content_type='application/json',
                                headers={'Authorization': f'Bearer {token}'})


        government = self.app_client.post("/api/v1/governments/pending", content_type="application/json",data=json.dumps({
            "name": "Ugandan",
            "Location": "Uganda"
            }), headers={'Authorization': f'Bearer {token}'})

        government = self.app_client.get("/api/v1/governments/pending", content_type="application/json", headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(government.status_code, 400)
        response = json.loads(government.data)
        self.assertEqual(response['message'], 'Trying to edit government using a deactivated account')
        
    def test_cant_get_pending_governments_without_token(self):
        self.sign_up_superadmin()

        token = self.superadmin_login()

        government = self.app_client.get("/api/v1/governments/pending", content_type="application/json")

        self.assertEqual(government.status_code, 401)
        response = json.loads(government.data)
        self.assertEqual(response['msg'], 'Missing Authorization Header')
        
    def test_cant_get_pending_governments_without_token(self):
        self.sign_up_superadmin()

        token = self.superadmin_login()

        government = self.app_client.get("/api/v1/governments/pending", content_type="application/json", headers={'Authorization': f'Bearer {token}'})

        self.assertEqual(government.status_code, 404)
        response = json.loads(government.data)
        self.assertEqual(response['message'], 'No pending governments found ')
        
    def test_can_get_all_pending_governments_without_acess_rights(self):
        self.sign_up_superadmin()
        self.sign_up()
        token = self.user_login()
        token1 = self.superadmin_login()

        self.app_client.post("/api/v1/governments", content_type="application/json", 
            data=json.dumps({
            "name": "Ugandan",
            "Location": "Uganda"
            }), headers={'Authorization': f'Bearer {token}'})

        government = self.app_client.get("/api/v1/governments/pending", content_type="application/json", headers={'Authorization': f'Bearer {token}'})

        self.assertEqual(government.status_code, 400)
        response = json.loads(government.data)
        self.assertEqual(response['message'], 'Unauthorised access')


    #############################################################################################
    #                                                                                           #
    #                          FETCH specific GOVERNMENT TESTCASES                            #
    #                                                                                           #
    #############################################################################################
    def test_can_get_specific_government(self):
        self.sign_up()
        token = self.user_login()

        create = self.app_client.post("/api/v1/governments", content_type="application/json", 
            data=json.dumps({
            "name": "Ugandan",
            "Location": "Uganda"
            }), headers={'Authorization': f'Bearer {token}'})

        government = self.app_client.get("/api/v1/governments/1", content_type="application/json")

        self.assertEqual(government.status_code, 200)
        response = json.loads(government.data)
        self.assertEqual(len(response),1)
        
    
    def test_cant_get_government_with_nonexistent_id(self):
        self.sign_up()
        token = self.user_login()

        government = self.app_client.get("/api/v1/governments/1", content_type="application/json")

        self.assertEqual(government.status_code, 404)
        response = json.loads(government.data)
        self.assertEqual(response['message'], 'government with that id doesnot exist')
        
    #############################################################################################
    #                                                                                           #
    #                          CANCEL specific governmentS TESTCASES                           #
    #                                                                                           #
    # #############################################################################################
    def test_can_cancel_specific_government(self):
        self.sign_up_superadmin()
        token = self.superadmin_login()

        create = self.app_client.post("/api/v1/governments", content_type="application/json", 
            data=json.dumps({
            "name": "Ugandan",
            "Location": "Uganda"
            }), headers={'Authorization': f'Bearer {token}'})

        government = self.app_client.put("/api/v1/governments/cancel/1", content_type="application/json", headers={'Authorization': f'Bearer {token}'})
        
        self.assertEqual(government.status_code, 200)
        response = json.loads(government.data)
        self.assertEqual(response['message'], 'Your government has been cancelled')
        
    
    def test_cant_cancel_government_without_token(self):
        self.sign_up_superadmin()
        token = self.superadmin_login()

        create = self.app_client.post("/api/v1/governments", content_type="application/json", 
            data=json.dumps({
            "name": "Ugandan",
            "Location": "Uganda"
            }), headers={'Authorization': f'Bearer {token}'})

        government = self.app_client.put("/api/v1/governments/cancel/1", content_type="application/json")

        self.assertEqual(government.status_code, 401)
        response = json.loads(government.data)
        self.assertEqual(response['msg'], 'Missing Authorization Header')
        

    def test_cant_cancel_nonexistent_government(self):
        self.sign_up_superadmin()
        token = self.superadmin_login()

        create = self.app_client.post("/api/v1/governments", content_type="application/json",             data=json.dumps({
            "name": "Ugandan",
            "Location": "Uganda"
            }), headers={'Authorization': f'Bearer {token}'})

        government = self.app_client.put("/api/v1/governments/cancel/2", content_type="application/json", headers={'Authorization': f'Bearer {token}'})

        self.assertEqual(government.status_code, 400)
        response = json.loads(government.data)
        self.assertEqual(response['message'], 'Cant update nonexistent government ')
        
    def test_cant_cancel_inactive_government(self):
        self.sign_up_superadmin()
        token = self.superadmin_login()

        create = self.app_client.post("/api/v1/governments", content_type="application/json", 
            data=json.dumps({
            "name": "Ugandan",
            "Location": "Uganda"
            }), headers={'Authorization': f'Bearer {token}'})

        t= self.app_client.put("/api/v1/governments/delete/1", content_type="application/json", headers={'Authorization': f'Bearer {token}'})
        
        government = self.app_client.put("/api/v1/governments/cancel/1", content_type="application/json", headers={'Authorization': f'Bearer {token}'})
        
        self.assertEqual(government.status_code, 400)
        response = json.loads(government.data)
        self.assertEqual(response['message'], 'Cant update an inactive government ')
        

    def test_cant_cancel_government_with_inactive_users(self):
        self.sign_up_superadmin()
        token = self.superadmin_login()

        create = self.app_client.post("/api/v1/governments", content_type="application/json", 
            data=json.dumps({
            "name": "Ugandan",
            "Location": "Uganda"
            }), headers={'Authorization': f'Bearer {token}'})

        self.app_client.put("/api/v1/users/delete/1", content_type="application/json", headers={'Authorization': f'Bearer {token}'})
        
        government = self.app_client.put("/api/v1/governments/cancel/1", content_type="application/json", headers={'Authorization': f'Bearer {token}'})

        self.assertEqual(government.status_code, 400)
        response = json.loads(government.data)
        self.assertEqual(response['message'], 'Trying to edit government using a deactivated account')
    
    def test_cant_cancel_government_without_admin_rights(self):
        self.sign_up()
        token = self.user_login()

        create = self.app_client.post("/api/v1/governments", content_type="application/json", 
            data=json.dumps({
            "name": "Ugandan",
            "Location": "Uganda"
            }), headers={'Authorization': f'Bearer {token}'})

        self.app_client.put("/api/v1/users/delete/1", content_type="application/json", headers={'Authorization': f'Bearer {token}'})

        self.app_client.put("/api/v1/governments/delete/1", content_type="application/json", headers={'Authorization': f'Bearer {token}'})
        government = self.app_client.put("/api/v1/governments/cancel/1", content_type="application/json", headers={'Authorization': f'Bearer {token}'})

        self.assertEqual(government.status_code, 400)
        response = json.loads(government.data)
        self.assertEqual(response['message'], 'Trying to edit government using a deactivated account')
        

    #############################################################################################
    #                                                                                           #
    #                            UPDATE government TESTCASES                                   #
    #                                                                                           #
    #############################################################################################

    def test_can_update_government_successfully(self):

        self.sign_up_superadmin()
        token = self.superadmin_login()
        self.app_client.post("/api/v1/governments", content_type="application/json", 
            data=json.dumps({
            "name": "Ugandan",
            "Location": "Uganda"
            }), headers = {'Authorization': f'Bearer {token}'})
        government = self.app_client.put("/api/v1/governments/name/1", content_type="application/json", 
            data=json.dumps(self.gov_name), headers = {'Authorization': f'Bearer {token}'})
        
        self.assertEqual(government.status_code, 200)
        response = json.loads(government.data)
        self.assertEqual(response['message'], "Your name has been updated ")
    
    def test_cant_update_government_without_token(self):

        self.sign_up()
        token = self.user_login()
        self.app_client.post("/api/v1/governments", content_type="application/json", 
            data=json.dumps({
            "name": "Ugandan",
            "Location": "Uganda"
            }), headers = {'Authorization': f'Bearer {token}'})
        government = self.app_client.put("/api/v1/governments/name/1", content_type="application/json", 
            data=json.dumps(self.gov_name))

        self.assertEqual(government.status_code, 401)
        response = json.loads(government.data)
        self.assertEqual(response['msg'], 'Missing Authorization Header')

    def test_cant_update_government_with_missing_fields(self):

        self.sign_up()
        token = self.user_login()
        self.app_client.post("/api/v1/governments", content_type="application/json", 
            data=json.dumps({
            "name": "Ugandan",
            "Location": "Uganda"
            }), headers = {'Authorization': f'Bearer {token}'})
        government = self.app_client.put("/api/v1/governments/name/1", content_type="application/json", 
            data=json.dumps(self.gov_name1), headers = {'Authorization': f'Bearer {token}'})

        self.assertEqual(government.status_code, 400)
        response = json.loads(government.data)
        self.assertEqual(response['message'], 'Some fields are missing')
        
    def test_cant_update_government_with_invalid_name(self):

        self.sign_up_superadmin()
        token = self.superadmin_login()

        self.app_client.post("/api/v1/governments", content_type="application/json", 
            data=json.dumps({
            "name": "Ugandan",
            "Location": "Uganda"
            }), headers = {'Authorization': f'Bearer {token}'})
        government = self.app_client.put("/api/v1/governments/name/1", content_type="application/json", 
            data=json.dumps(self.gov_name2), headers = {'Authorization': f'Bearer {token}'})

        self.assertEqual(government.status_code, 400)
        response = json.loads(government.data)
        self.assertEqual(response['message'], 'name must be a non empty string')
        
    def test_cant_update_government_with_missing_association(self):

        self.sign_up()
        token = self.user_login()
   
        government = self.app_client.put("/api/v1/governments/name/1", content_type="application/json", 
            data=json.dumps(self.gov_name), headers = {'Authorization': f'Bearer {token}'})

        self.assertEqual(government.status_code, 404)
        response = json.loads(government.data)
        self.assertEqual(response['message'], 'Government not found')
        
    def test_cant_update_government_with_inactive_account(self):

        self.sign_up_superadmin()
        token = self.superadmin_login()

        self.app_client.post("/api/v1/governments", content_type="application/json", 
            data=json.dumps({
            "name": "Ugandan",
            "Location": "Uganda"
            }), headers={'Authorization': f'Bearer {token}'})

        self.app_client.put("/api/v1/users/delete/1", content_type="application/json", headers={'Authorization': f'Bearer {token}'})

        government = self.app_client.put("/api/v1/governments/name/1", content_type="application/json", 
            data=json.dumps(self.gov_name), headers = {'Authorization': f'Bearer {token}'})
       
        self.assertEqual(government.status_code, 400)
        response = json.loads(government.data)
        self.assertEqual(response['message'], 'user account inactive')

    def test_cant_update_updated_government(self):

        self.sign_up_superadmin()
        token = self.superadmin_login()
        self.app_client.post("/api/v1/governments", content_type="application/json", 
            data=json.dumps({
            "name": "Ugandan",
            "Location": "Uganda"
            }), headers={'Authorization': f'Bearer {token}'})
       
        self.app_client.put("/api/v1/governments/name/1", content_type="application/json", 
            data=json.dumps(self.gov_name), headers={'Authorization': f'Bearer {token}'})

        government = self.app_client.put("/api/v1/governments/name/1", content_type="application/json", 
            data=json.dumps(self.gov_name), headers = {'Authorization': f'Bearer {token}'})
        self.assertEqual(government.status_code, 400)
        response = json.loads(government.data)
        self.assertEqual(response['message'], 'The name is already upto date')

    def test_cant_update_government_name_without_authorisation(self):

        self.sign_up_superadmin()
        token = self.superadmin_login()
        self.app_client.post("/api/v1/governments", content_type="application/json", 
            data=json.dumps({
            "name": "Ugandan",
            "Location": "Uganda"
            }), headers={'Authorization': f'Bearer {token}'})
        
        self.sign_up()
        token = self.user_login()

        government = self.app_client.put("/api/v1/governments/name/1", content_type="application/json", 
            data=json.dumps(self.gov_name), headers={'Authorization': f'Bearer {token}'})
        
       
        self.assertEqual(government.status_code, 400)
        response = json.loads(government.data)
        self.assertEqual(response['message'], 'unauthorised access')


    #############################################################################################
    #                                                                                           #
    #                            DELETE ASSOCIATION TESTCASES                                   #
    #                                                                                           #
    #############################################################################################

    def test_can_delete_government_successfully(self):

        self.sign_up_superadmin()
        token = self.superadmin_login()
        self.app_client.post("/api/v1/governments", content_type="application/json", 
            data=json.dumps({
            "name": "Ugandan",
            "Location": "Uganda"
            }), headers = {'Authorization': f'Bearer {token}'})
        government = self.app_client.put("/api/v1/governments/delete/1", content_type="application/json", 
            data=json.dumps(self.gov_name), headers = {'Authorization': f'Bearer {token}'})
        
        self.assertEqual(government.status_code, 200)
        response = json.loads(government.data)
        self.assertEqual(response['message'], "Your government has been deleted")

    def test_cant_delete_government_without_token(self):

        self.sign_up_superadmin()
        token = self.superadmin_login()
        self.app_client.post("/api/v1/governments", content_type="application/json", 
            data=json.dumps({
            "name": "Ugandan",
            "Location": "Uganda"
            }), headers = {'Authorization': f'Bearer {token}'})
        government = self.app_client.put("/api/v1/governments/delete/1", content_type="application/json", 
            data=json.dumps(self.gov_name))
        
        self.assertEqual(government.status_code, 401)
        response = json.loads(government.data)
        self.assertEqual(response['msg'], "Missing Authorization Header")

    def test_cant_delete_government_which_doesnt_exist(self):

        self.sign_up_superadmin()
        token = self.superadmin_login()
        self.app_client.post("/api/v1/governments", content_type="application/json", 
            data=json.dumps({
            "name": "Ugandan",
            "Location": "Uganda"
            }), headers = {'Authorization': f'Bearer {token}'})
        government = self.app_client.put("/api/v1/governments/delete/2", content_type="application/json", 
           headers = {'Authorization': f'Bearer {token}'})
        
        self.assertEqual(government.status_code, 400)
        response = json.loads(government.data)
        self.assertEqual(response['message'], "The government doesnt exist")

    def test_cant_delete_government_which_doesnt_exist(self):

        self.sign_up_superadmin()
        token = self.superadmin_login()
        self.app_client.post("/api/v1/governments", content_type="application/json", 
            data=json.dumps({
            "name": "Ugandan",
            "Location": "Uganda"
            }), headers={'Authorization': f'Bearer {token}'})

        self.app_client.put("/api/v1/governments/delete/1", content_type="application/json", 
            headers={'Authorization': f'Bearer {token}'})
            
        government = self.app_client.put("/api/v1/governments/delete/1", content_type="application/json",headers = {'Authorization': f'Bearer {token}'})
        
        self.assertEqual(government.status_code, 400)
        response = json.loads(government.data)
        self.assertEqual(response['message'], "Cant update an inactive government ")

    def test_cant_delete_government_with_non_exist_user_account(self):

        self.sign_up_superadmin()
        token = self.superadmin_login()
        self.app_client.post("/api/v1/governments", content_type="application/json", 
            data=json.dumps({
            "name": "Ugandan",
            "Location": "Uganda"
            }), headers={'Authorization': f'Bearer {token}'})

        self.app_client.put("/api/v1/users/delete/1", content_type="application/json", headers={'Authorization': f'Bearer {token}'})
            
        government = self.app_client.put("/api/v1/governments/delete/1", content_type="application/json", 
            data=json.dumps(self.update_name_data), headers = {'Authorization': f'Bearer {token}'})
        
        self.assertEqual(government.status_code, 404)
        response = json.loads(government.data)
        self.assertEqual(response['message'], "user with id not found")

    
    def test_cant_delete_government_without_authorisation(self):

        self.sign_up_superadmin()
        token = self.superadmin_login()
        self.app_client.post("/api/v1/governments", content_type="application/json", 
            data=json.dumps({
            "name": "Ugandan",
            "Location": "Uganda"
            }), headers={'Authorization': f'Bearer {token}'})
        self.sign_up()
        token = self.user_login()
        government = self.app_client.put("/api/v1/governments/delete/1", content_type="application/json", headers = {'Authorization': f'Bearer {token}'})
        
        self.assertEqual(government.status_code, 400)
        response = json.loads(government.data)
        self.assertEqual(response['message'], "unauthorised access")

    # #############################################################################################
    # #                                                                                           #
    # #                            APPROVE ASSOCIATION TESTCASES                                  #
    #                                                                                           #
    # #############################################################################################
    def test_can_approve_government_successfully(self):

        self.sign_up_superadmin()
        token = self.superadmin_login()
        self.app_client.post("/api/v1/governments", content_type="application/json", 
            data=json.dumps({
            "name": "Ugandan",
            "Location": "Uganda"
            }), headers={'Authorization': f'Bearer {token}'})
     
        government = self.app_client.put("/api/v1/governments/approve/1", content_type="application/json", 
            headers={'Authorization': f'Bearer {token}'})
        
        self.assertEqual(government.status_code, 200)
        response = json.loads(government.data)
        self.assertEqual(response['message'], "The government has been approved")

    def test_cant_approve_government_without_authorisation(self):

        self.sign_up_superadmin()
        token = self.superadmin_login()
        self.app_client.post("/api/v1/governments", content_type="application/json", 
            data=json.dumps({
            "name": "Ugandan",
            "Location": "Uganda"
            }), headers={'Authorization': f'Bearer {token}'})
        self.sign_up()
        token = self.user_login()
        government = self.app_client.put("/api/v1/governments/approve/1", content_type="application/json", 
            headers = {'Authorization': f'Bearer {token}'})
        self.assertEqual(government.status_code, 400)
        response = json.loads(government.data)
        self.assertEqual(response['message'], "unauthorised access")

    def test_cant_approve_government_which_is_upto_date(self):

        self.sign_up_superadmin()
        token = self.superadmin_login()
        self.app_client.post("/api/v1/governments", content_type="application/json",data=json.dumps({
            "name": "Ugandan",
            "Location": "Uganda"
            }), headers={'Authorization': f'Bearer {token}'})

        self.app_client.put("/api/v1/governments/approve/1", content_type="application/json", headers={'Authorization': f'Bearer {token}'})
            
        government = self.app_client.put("/api/v1/governments/approve/1", content_type="application/json", 
            data=json.dumps(self.update_name_data), headers={'Authorization': f'Bearer {token}'})
            
        self.assertEqual(government.status_code, 400)
        response = json.loads(government.data)
        self.assertEqual(response['message'], "The government is already approved")


    def test_cant_approve_government_without_token(self):

        self.sign_up_superadmin()
        token = self.superadmin_login()
        self.app_client.post("/api/v1/governments", content_type="application/json", 
            data=json.dumps({
            "name": "Ugandan",
            "Location": "Uganda"
            }), headers={'Authorization': f'Bearer {token}'})
     
        government = self.app_client.put("/api/v1/governments/approve/1", content_type="application/json" )
        self.assertEqual(government.status_code, 401)
        response = json.loads(government.data)
        self.assertEqual(response['msg'], "Missing Authorization Header")