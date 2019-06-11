import json
import unittest
from statisticsapi import app
from statisticsapi.routes.associations import Association
from statisticsapi.routes.auth import Auth
from statisticsapi.routes.users import User
from statisticsapi.controllers.database import DatabaseConnection

db = DatabaseConnection()

class TestBase(unittest.TestCase):
    """Base class for tests. 
    This class defines a common `setUp` method that defines attributes which 
    are used in the various tests.
    """
    user = {
	"first_name":"aine",
	"last_name":"kirabo",
	"other_name":"mbabazi",
	"photo":"some photo",
	"associationId":1,
	"governmentId":1,
	"user_role":"superadmin",
	"email":"admin1@admin.com",
	"password":"password",
	"country":"Uganda"
}
    
    user1 = {
    "associationId": '1',
    "governmentId":'none',
    "country":"Uganda",
    "name" : "eve1",
    "email" : "new@gmail.com",
    "user_group": "association",
    "user_role":"user",
	"password": "mine1234",
    "confirm_password":"mine1234"
    }

    user_login_data2 = {
        "email": "new@gmail.com",
        "password": "mine1234"
    }
    user_login_data3 = {
        "email" : "new@gmail.com",
        "newpassword": "mine12343"
    }
    user_login_data4 = {
        "email" : "none@gmail.com",
        "newpassword": "mine12343"
    }
    user_login_data44 = {
        "email" : "none@gmail.com",
        "password": "mine12343"
    }
    user_login_data5 = {
        "email" : "nonegmail.com",
        "newpassword": "mine12343"
    }
    user_login_data6 = {
        "email" : "none@gmail.com",
        "newpassword": "mine12"
    }
    user_login_data7 = {
        "email" : "none@gmail.com"
        
    }
    user2 = {
    "associationId": '1',
    "governmentId":'none',
    "country":"Uganda",
    "name" : "eve1",
    "email" : "new@gmail.com",
    "user_group": "association",
    "user_role":"superadmin",
	"password": "mine1234",
    "confirm_password":"mine1234"
    }
    user_login_data = {
        "email" : "admin1@admin.com",
        "password": "password"
    }
    recover = {
        "email" : "eve@gmail.com",
        "newpassword": "mine1234"
    }
    user_login_datai = {
        "email" : "eve@gmail.com",
        "password": "mine12344"
    }
    user_login_datae= {
        "email" : "evegmail.com",
        "password": "mine1234"
    }
    user_login_datap= {
        "email" : "eve@gmail.com",
        "password": "mine12"
    }
    user_login_datam = {
        "email" : "eve@gmail.com"
        
    }

    user_login_data1 = {
        "email" : "new@gmail.com",
        "password": "mine1234"
    }

    admin_user = {
        "associationId": '1',
        "governmentId":'none',
        "country":"Uganda",
        "name" : "eves",
        "email" : "admin@admin.com",
        "user_group": "association",
        "user_role":"admin",
        "password": "mine1234",
        "confirm_password":"mine1234"
    }
    super_admin_user_data = {
        "email": "super@super.com",
        "password": "mine1234"
    }
    
    super_admin_user = {
        "associationId": '1',
        "governmentId":'none',
        "country":"Uganda",
        "name" : "evea",
        "email" : "super@super.com",
        "user_group": "association",
        "user_role":"superadmin",
        "password": "mine1234",
        "confirm_password":"mine1234"
    }


    user_missing_fields={
        "associationId": '1',
        "governmentId": 'null',
        "country":"Uganda",
        "name" : "eae",
        "email" : "eve@gmail.com",
        "user_group": "association",
        "user_role":"admin",
        "password": "mine1234"
    }

    user_with_invalid_password = {
        "associationId": '1',
        "governmentId": 'null',
        "country":"Uganda",
        "name" : "ever",
        "email" : "eve@gmail.com",
        "user_group": "association",
        "user_role":"admin",
        "password": "mine123",
        "confirm_password":"mine123"
    }

    user_with_mismatched_password = {
        "associationId": '1',
        "governmentId": 'null',
        "country":"Uganda",
        "name" : "even",
        "email" : "eve@gmail.com",
        "user_group": "association",
        "user_role":"admin",
        "password": "mine1234",
        "confirm_password":"mine1235"
    }

    user_with_invalid_name = {
        "associationId": '1',
        "governmentId": 'null',
        "country":"Uganda",
        "name" : '1234',
        "email" : "eve@gmail.com",
        "user_group": "association",
        "user_role":"admin",
        "password": "mine1234",
        "confirm_password":"mine1234"
    }

    user_with_invalid_email= {
        "associationId": '1',
        "governmentId": 'null',
        "country":"Uganda",
        "name" : "evem",
        "email" : "eve.com",
        "user_group": "association",
        "user_role":"admin",
        "password": "mine1234",
        "confirm_password":"mine1234"
    }

    user_with_invalid_country = {
        "associationId": '1',
        "governmentId": 'null',
        "country":'1234',
        "name" : "evep",
        "email" : "eve@gmail.com",
        "user_group": "association",
        "user_role":"admin",
        "password": "mine1234",
        "confirm_password":"mine1234"
    }

    user_with_none_string_group= {
        "associationId": '1',
        "governmentId": 'null',
        "country":"Uganda",
        "name" : "evet",
        "email" : "eve@gmail.com",
        "user_group": '1234',
        "user_role":"admin",
        "password": "mine1234",
        "confirm_password":"mine1234"
    }

    user_with_invalid_group= {
        "associationId": '1',
        "governmentId": 'null',
        "country":"Uganda",
        "name" : "eveh",
        "email" : "eve@gmail.com",
        "user_group": "farmers",
        "user_role":"admin",
        "password": "mine1234",
        "confirm_password":"mine1234"
    }

    user_with_non_string_role = {
        "associationId": '1',
        "governmentId": 'null',
        "country":"Uganda",
        "name" : "eveg",
        "email" : "eve@gmail.com",
        "user_group": "association",
        "user_role":'1234',
        "password": "mine1234",
        "confirm_password":"mine1234"
    }

    user_with_invalid_role = {
        "associationId": '1',
        "governmentId": 'null',
        "country":"Uganda",
        "name" : "eves",
        "email" : "eve@gmail.com",
        "user_group": "association",
        "user_role":"superuser",
        "password": "mine1234",
        "confirm_password":"mine1234"
    }

    user_with_duplicate_mail = {
        "associationId": '1',
        "governmentId": 'null',
        "country":"Uganda",
        "name" : "eve",
        "email" : "eve@gmail.com",
        "user_group": "association",
        "user_role":"admin",
        "password": "mine1234",
        "confirm_password":"mine1234"
    }

    user_with_invalid_associationId= {
        "associationId": 44444444444,
        "governmentId": 'null',
        "country":"Uganda",
        "name" : "eve",
        "email" : "eve@gmail.com",
        "user_group": "association",
        "user_role":"superuser",
        "password": "mine1234",
        "confirm_password":"mine1234"
    }

    association_data= {
        "governmentId": 1,
        "name": "myfarm2",
        "photo": "photo2"
    }

    government_data= {
        "name": "myfarm2",
        "photo": "photo2"
    }
    update_name_data = {
        "name":"Agrofrost"
    }
    gov_name = {
        "name":"Kenya"
    }
    gov_name2 = {
        "name":"123"
    }
    gov_name1 = {
        
    }

    update_name_data2 = {
        "name": '1234'
    }
    update_name_data1 = {
        
    }
    association_with_missing_fields = {
        "name": "Agribus"
    }

    association_with_invalid_name = {
        "name": '1234',
        "Location": "Uganda"
    }

    association_with_invalid_location = {
        "name": 'Agribuz',
        "Location": '23495'
    }


    

    def setUp(self):
        self.app_client = app.test_client()
        db.create_db_tables()

    def tearDown(self):
        db.drop_table('statistic_user')
        db.drop_table('statistic_association')
        db.drop_table('statistic_government')

    def admin_login(self):
        admin_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
            data=json.dumps(admin_user))
        self.assertEqual(admin_login.status_code, 200)
        response = json.loads(admin_login.data)
        self.assertEqual(response['message'], 'login successful')
        self.admin_access_token = response['auth_token']
        

    def superadmin_login(self):
        super_admin_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
            data=json.dumps(self.super_admin_user_data))
        self.assertEqual(super_admin_login.status_code, 200)
        response = json.loads(super_admin_login.data)
        self.assertEqual(response['message'], 'login successful')
        self.super_admin_access_token = response['auth_token']
        return(self.super_admin_access_token)
        
    def user_login_government_user(self):
        user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
            data=json.dumps({
                "email" : "eve@gmail.com",
                "password": "mine1234"
                }))
    
        self.assertEqual(user_login.status_code, 200)
        response = json.loads(user_login.data)
        self.assertEqual(response['message'], 'login successful')
        self.user_access_token = response['auth_token']
        return self.user_access_token      
    
    def user_login(self):
        user_login = self.app_client.post("api/v1/auth/login", content_type="application/json", 
            data=json.dumps(self.user_login_data))
        
        self.assertEqual(user_login.status_code, 200)
        response = json.loads(user_login.data)
        self.assertEqual(response['message'], 'login successful')
        self.user_access_token = response['auth_token']
        return self.user_access_token

    def sign_up(self):
        self.app_client.post("/api/v1/auth/signup", content_type='application/json', 
            data=json.dumps(self.user))
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', 
            data=json.dumps(self.user))
        
        self.assertEqual(create_user.status_code, 201)
        response = json.loads(create_user.data)
        self.assertEqual(response['message'], 'Your account has been created')
    
    def sign_up_government(self):
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', 
            data=json.dumps({
            "associationId": '1',
            "governmentId":'1',
            "country":"Uganda",
            "name" : "eve1",
            "email" : "eve@gmail.com",
            "user_group": "government",
            "user_role":"user",
            "password": "mine1234",
            "confirm_password":"mine1234"
            }))
        
        self.assertEqual(create_user.status_code, 201)
        response = json.loads(create_user.data)
        self.assertEqual(response['message'], 'Your account has been created')

    def sign_up1(self):
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', 
            data=json.dumps(self.user1))
        
        self.assertEqual(create_user.status_code, 201)
        response = json.loads(create_user.data)
        self.assertEqual(response['message'], 'Your account has been created')

        
        

    def sign_up_admin(self):
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', 
            data=json.dumps(admin_user))
            
        self.assertEqual(create_user.status_code, 201)

        response = json.loads(create_user.data)
        self.assertEqual(response['message'], 'Your account has been created')

    def sign_up_superadmin(self):
        create_user = self.app_client.post("/api/v1/auth/signup", content_type='application/json', 
            data=json.dumps(self.super_admin_user))
     
        self.assertEqual(create_user.status_code, 201)
        response = json.loads(create_user.data)
        self.assertEqual(response['message'], 'Your account has been created')

    def create_association(self,):
        association = self.app_client.post("/api/v1/association", content_type='application/json', 
            data=json.dumps(association_data))
        response = json.loads(association.data)
        
        self.assertEqual(association.status_code, 201)
        
        self.assertEqual(response['message'], 'Your association has been created')
        self.assertEqual(response['association'], {
            "name": "Agribus",
            "Location": "Uganda"
            })

    def create_government(self,):
        government = self.app_client.post("/api/v1/government", content_type='application/json', 
            data=json.dumps(government_data))
        response = json.loads(government.data)
        
        self.assertEqual(government.status_code, 201)
        
        self.assertEqual(response['message'], 'Your association has been created')
        self.assertEqual(response['association'], {
            "name": "Ugandan",
            "Location": "Uganda"
            })