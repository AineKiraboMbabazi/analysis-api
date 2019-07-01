import datetime
import pymysql
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity)
from flask import request, jsonify
from validations import Validator
from ..models.associations import Association
from .users import User_Controller
from .government import sendmail,generate_password
from .database import DatabaseConnection
con = DatabaseConnection()


class Association_Controller:
    def index():
        """
            controller for the index page

        """

        return jsonify({"message": "Welcome to statistics API"}), 200      
    
    def create_association():
        """
            controller to create a association

            :return object of created association:
        """

        current_user = get_jwt_identity()

        request_data = request.get_json(force=True)
       
        if len(request_data.keys()) != 6:
            return jsonify({"message": "Some fields are missing"}), 400

        
        user = con.get_single_user(current_user)
        userId = current_user
        status  = user['status']
        
        if  status == 0 or status == '0':
            return jsonify({"message": "The user account has been deactivated"}), 400
            
        role = user['user_role']

        if role == 'super_admin':
            status = 'active'

        status = 'pending'
        email = request_data['email']
        role = request_data['user_role']
        update_url = request_data['update_url']
        creation_date = datetime.date.today().strftime('%Y-%m-%d')
        name = request_data['name']
        photo = request_data['photo']
        created_by = userId
        governmentId =request_data['governmentId'] 
        updated_by = userId
        updated_at = creation_date
        
        validate_input = Validator()

        if not (validate_input.validate_string_input(name)):
            return jsonify({"message": "Name field should contain strings "}), 400
                            
        association=con.fetch_associations_by_name(name)
        
        if association:
            return jsonify({"message":"An association with that name already exists"}),400
        
        association = Association(name, photo, status, governmentId, created_by, creation_date, updated_by, updated_at).__dict__

        associationId = con.create_association(association['name'], association['photo'], association['status'], association['governmentId'], association['created_by'], association['creation_date'], association['updated_by'], association['updated_at'])
        password = generate_password()
        user = User_Controller.create_association_admin_user(associationId,governmentId,role,email,password,name,created_by,creation_date,updated_by,updated_at)
        sendmail(email,update_url,password)
        return jsonify({"message": "Your association has been created","association":request_data}), 201

    def fetch_all_associations():
        """
            controller fetch all associations
            :return associations list:
        """

        current_user_id = get_jwt_identity()

        User = con.get_single_user(current_user_id)
        
        role = User['user_role']
        
        country = User['country']

        associations = con.get_all_associations()
     
        
        if role == 'super_admin':
            if len (associations) == 0 or associations == None or associations == []:
                return jsonify({"message": "No associations found"}), 404
        
            return jsonify({
            'columns': [
            # {
            #   'label': 'associationId',
            #   'field': 'associationId',
            #   'sort': 'asc'
            # },
            # {
            #   'label': 'governmentId',
            #   'field': 'associationId',
            #   'sort': 'asc'
            # },
            {
              'label': 'name',
              'field': 'name',
              'sort': 'asc'
            },{
              'label': 'photo',
              'field': 'photo',
              'sort': 'asc'
            },{
              'label': 'created_by',
              'field': 'created_by',
              'sort': 'asc'
            }
            # ,{
            #   'label': 'updated-by',
            #   'field': 'updated_by',
            #   'sort': 'asc'
            # },
            # {
            #   'label': 'updated-at',
            #   'field': 'updated_at',
            #   'sort': 'asc'
            # }
            ],
            
                'rows' :associations
                
            
            }), 200
       
        # if user_group == 'government':
        #     if len (associations) == 0 or associations == None or associations == []:
        #         return jsonify({"message": "No associations found"}), 404
        
        #     return jsonify({'associations': associations}), 200  
            
        
        return jsonify({"message":"Unauthorised access"}),401

    def fetch_pending_association():
        """
            controller fetch pending association
            :return association:
        """

        current_user_id = get_jwt_identity()
        
        user = con.get_single_user(current_user_id)
        
        if user['status'] == 0 or user['status'] == '0':
            return jsonify({"message":"Trying to edit association using a deactivated account"}),400
        
        user_role = user['user_role']

        associations = con.fetch_pending_association()

        if user_role == 'super_admin':
            if  len (associations) == 0 or associations == None or associations == []:
                return jsonify({"message": "No pending associations found "}), 404

            return jsonify({'associations': associations}), 200

        return jsonify({"message":"Unauthorised access"}),400

    

    def fetch_specific_association(associationId):
        """
            controller fetch specific association
            :return association:
        """

        single_association = con.get_single_association(associationId)
        if not single_association or single_association == [] or len(single_association) == 0:
            return jsonify({"message": "association with that id doesnot exist"}), 404

        return jsonify({'association': single_association}), 200
    
    def fetch_association_users(associationId):
        """
            controller fetch specific association
            :return association:
        """

        single_association = con.get_single_association(associationId)
        if not single_association or single_association == [] or len(single_association) == 0:
            return jsonify({"message": "association with that id doesnot exist"}), 404

        association_users = con.get_all_association_users(associationId)
        if not association_users or association_users == [] or len(association_users) == 0:
            return jsonify({"message": "association with that id has no users"}), 404

        return jsonify({'columns': [
            {
              'label': 'userId',
              'field': 'userId',
              'sort': 'asc'
            },{
              'label': 'first_name',
              'field': 'first_name',
              'sort': 'asc'
            },{
              'label': 'last_name',
              'field': 'last_name',
              'sort': 'asc'
            },{
              'label': 'other_name',
              'field': 'other_name',
              'sort': 'asc'
            },{
              'label': 'associationId',
              'field': 'associationId',
              'sort': 'asc'
            },{
              'label': 'governmentId',
              'field': 'governmentId',
              'sort': 'asc'
            },{
              'label': 'photo',
              'field': 'photo',
              'sort': 'asc'
            },{
              'label': 'email',
              'field': 'email',
              'sort': 'asc'
            },{
              'label': 'country',
              'field': 'country',
              'sort': 'asc'
            },{
              'label': 'created_by',
              'field': 'created_by',
              'sort': 'asc'
            },
            {
              'label': 'updated-by',
              'field': 'updated_by',
              'sort': 'asc'
            },{
              'label': 'updated-at',
              'field': 'updated_at',
              'sort': 'asc'
            }],
            'rows': association_users}), 200


    def cancel_specific_association(associationId):
        """
            controller cancel association
            :return success message:
        """

        current_user_id = get_jwt_identity()

        association_to_edit = con.get_single_association(associationId)
        if not association_to_edit or association_to_edit == []:
            return jsonify({"message": "Association with that id doesnt exist"}), 404

        if association_to_edit['status'] == '0':
            return jsonify({"message": "Cant update an inactive association "}), 400
 
        User = con.get_single_user(current_user_id)
        role = User['user_role']
        if User['status'] == 0 or User['status'] == '0':
            return jsonify({"message":"Trying to edit association using a deactivated account"}),400

        if role == 'super_admin':
            con.cancel_association(associationId)
            return jsonify({"message": "Your association has been cancelled"}), 200

        return jsonify({"message": "unauthorised access"}), 401           

    def update_photo(associationId):
        """
            Function update name
            :param associationid:
            :return success message:
        """

        current_user_id = get_jwt_identity()

        User = con.get_single_user(current_user_id)
        if User == []:
            return jsonify({"message": "User not found"}), 404
            
        if User['status'] == 0 or User['status'] == '0':
            return jsonify({"message": "user account inactive"}), 400
            
        role = User['user_role']

        association = con.get_single_association(associationId)
        if association == [] or not association or association['status'] == 0:
            return jsonify({"message": "association not found"}), 404

                            
        request_data=request.get_json(force=True)
        
        if len(request_data.keys()) != 1:
            return jsonify({"message": "Some fields are missing"}), 400

        photo = request_data['photo']
        updated_by = current_user_id
        updated_at =  datetime.date.today().strftime('%Y-%m-%d')
        if (association['photo'] == photo):
            return jsonify({"message": "The name is already upto date"}), 400
            
        validate_name = Validator().validate_string_input(name)

        if not validate_name:
            return jsonify({"message": "name must be a non empty string"}), 400

        if association['created_by'] == current_user_id or role == 'super_admin':
            con.update_photo(photo, updated_by,updated_at,associationId )
            association1 = con.get_single_association(associationId)
            return jsonify({"message": "Your name has been updated ",
                        "updated association": association1}), 200

        return jsonify({"message": "unauthorised access"}), 401
        
    def update_name(associationId):
        """
            Function update name
            :param associationid:
            :return success message:
        """

        current_user_id = get_jwt_identity()

        User = con.get_single_user(current_user_id)
        if User == []:
            return jsonify({"message": "User not found"}), 404
            
        if User['status'] == 0 or User['status'] == '0':
            return jsonify({"message": "user account inactive"}), 400
            
        role = User['user_role']

        association = con.get_single_association(associationId)
        if association == [] or not association or association['status'] == 0:
            return jsonify({"message": "association not found"}), 404

                            
        request_data=request.get_json(force=True)
        
        if len(request_data.keys()) != 1:
            return jsonify({"message": "Some fields are missing"}), 400

        name = request_data['name']
        updated_by = current_user_id
        updated_at =  datetime.date.today().strftime('%Y-%m-%d')
        if (association['name'] == name):
            return jsonify({"message": "The name is already upto date"}), 400
            
        validate_name = Validator().validate_string_input(name)

        if not validate_name:
            return jsonify({"message": "name must be a non empty string"}), 400

        if association['created_by'] == current_user_id or role == 'super_admin':
            con.update_association_name(name, updated_by,updated_at,associationId )
            association1 = con.get_single_association(associationId)
            return jsonify({"message": "Your name has been updated ",
                        "updated association": association1}), 200

        return jsonify({"message": "unauthorised access"}), 401
    

    def delete_association(associationId):
        """
            controller to delete
            :param associationid:
            :return success message:
        """

        current_user_id = get_jwt_identity()

        association_to_edit = con.get_single_association(associationId)
        if not association_to_edit:
            return jsonify({"message": "The association doesnt exist"}), 404
            
        association_status = association_to_edit['status']

        if association_status == '0':
            return jsonify({"message": "Cant update an inactive association "}), 400
 
        User = con.get_single_user(current_user_id)
        if User['status'] == 0 or User == None or User['status'] == '0':
            return jsonify({"message":"user with id not found"}),404
        role = User['user_role']

        if role == 'super_admin':
            con.delete_association(associationId)
            return jsonify({"message": "Your association has been deleted"}), 200

        return jsonify({"message": "unauthorised access"}), 400
        

    def approve_association(associationId):
        """

            Function to approve association
            :param associationId:
            :return success message:
        """

        current_user_id = get_jwt_identity()

        association_to_approve = con.get_single_association(associationId)

        if not association_to_approve or association_to_approve['status'] == '0':
            return jsonify({"message": "The association you are trying to approve doesnt exist"}), 404

        if association_to_approve['status'] == 'approved':
            return jsonify({"message": "The association is already approved"}), 400

        user = con.get_single_user(current_user_id)

        if user['user_role'] == 'super_admin':
            con.approve_association(associationId)
            return jsonify({"message": "The association has been approved"}), 200

        return jsonify({"message": "unauthorised access"}), 400
        