import datetime
import pymysql
from flask import request, jsonify
from validations import Validator
from ..models.users import User
from ..models.associations import Association
from .database import DatabaseConnection
con = DatabaseConnection()


class User_Controller:
      
    
    def create_user():
        """
            function to create a user
        """
        # userid = get_jwt_identity()
        # if not userid:
        #     return jsonify({'msg': 'Missing Authorization Header'}), 401
        
        request_data = request.get_json(force=True)
        if len(request_data.keys()) != 5:
            return jsonify({"message": "Some fields are missing"}), 400
        
        associationId = request_data['associationId']
        country = request_data['country']
        name = request_data['name']
        status = 1
        user_group = request_data['user_group']
        user_role = request_data['user_role']
        created_by=name
        creation_date = datetime.date.today().strftime('%Y-%m-%d')
        validate_input = Validator()
        if not (validate_input.validate_string_input(name)):
            return jsonify({"message": "name Field should\
                            contain strings"}), 400
        if not (validate_input.validate_string_input(country)):
            return jsonify({"message": "location Field should\
                            contain strings"}), 400
        if not (validate_input.validate_string_input(user_group)):
            return jsonify({"message": "userid Field should contain strings"}), 400
        if not (validate_input.validate_string_input(user_role)):
            return jsonify({"message": "userid Field should contain strings"}), 400
        association = con.get_single_association(associationId)
        if (not association):
            return jsonify({"message":"The association with that id doesnot exist"}),400
        
        user=User(associationId, name, status, country, user_group,user_role,created_by,creation_date).__dict__
        con.add_user(user['associationId'], user['name'],user['status'], user['country'], user['user_group'],user['user_role'],user['created_by'],user['creation_date'])

        return jsonify({"message": "Your account has been created","account":request_data}), 201

    def fetch_all_users():
        """
            Function fetch all users
            :return users list:
        """
        
        users = con.get_all_users()
        if users == []:
            return jsonify({"message": "No users found"}), 404
        return jsonify({'users': users}), 200
        # user = User()
        # userid = get_jwt_identity()
        # if not userid:
        #     return jsonify({'msg': 'Missing Authorization Header'}), 401
        # get_user = user.get_user_by_id(userid)
        # if not get_user:
        #     return jsonify({"message": " No user with that id"}), 404
        # if get_user['role'] == 'admin':
        #     parcel = Parcel()
        #     parcels = parcel.get_all_parcels()
        #     if parcels == []:
        #         return jsonify({"message": "No parcels found"}), 404
        #     return jsonify({'parcels': parcels}), 200

        # return jsonify({"message": "Only administrators can view parcels"}), 400

    def fetch_specific_user(userId):
        """
            Function fetch specific user
            :return user:
        """
        # userId = get_jwt_identity()
        # if not userId:
        #     return({"message": "Missing authentication header"}), 401
        
        single_user = con.get_single_user(userId)
        if not single_user:
            return jsonify({"message": "user with that id doesnot exist"}), 404
        if single_user['status'] == 0:
            return jsonify({"message":"The user with that account doesnt exist"}),404
        return jsonify({'user': single_user}), 200


    def cancel_specific_user(userId):
        """
            Function cancel user
            :return success message:
        """
        # userid = get_jwt_identity()
        
        user_to_edit = con.get_single_user(userId)
        print(user_to_edit)
        if not user_to_edit:
            return jsonify({"message":"The user with that id doesnt exist"}),404
        if user_to_edit['status'] == 0:
            return jsonify({"message":"The user with that account doesnt exist"}),404
        # if not Parcel_to_edit:
        #     return jsonify({"message": " parcel doesnot exist"}), 404
        # parcel_owner_id = Parcel_to_edit['userId']
        # if parcel_owner_id != userid:
        #     return jsonify({"message": "You can only cancel an \
        #                     order you created"}), 400
        
        if not user_to_edit:
            return jsonify({"message": "user with that id doesnt exist"}), 400
        con.cancel_user(userId)
        return jsonify({"message": "User has been cancelled"}), 200

    def update_usergroup(userId):
        """
            Function to update user_group
            :return success message:
        """
        request_data = request.get_json(force=True)
        user_group = request_data['user_group']
        
        # if not get_jwt_identity():
        #     return jsonify({"message": "Some fields are missing"}), 400
        if len(request_data.keys()) != 1:
            return jsonify({"message": "Some fields are missing"}), 400
        validate_input = Validator().validate_string_input(user_group)
        if not validate_input:
            return jsonify({"message": "The user_group should be a none\
                            empty string"}), 400
        # userid = get_jwt_identity()
        
        # user = User()
        # editor = user.get_user_by_id(userid)['role']
        # if editor != 'admin':
        #     return jsonify({"message": "You can only update the present location\
        #                      if you are an admin"}), 400
        user_to_edit=con.get_single_user(userId)
        if user_to_edit['status'] == 0:
            return jsonify({"message":"The user with that account doesnt exist"}),404
        if not user_to_edit :
            return jsonify({"message": "The user you are trying to edit doesnt\
                    exist"}), 400
        if user_to_edit['user_group'] == user_group:
            return jsonify({"message": "user_group is already upto date"}), 400
        
        con.update_usergroup(userId, user_group)
        edited_data = con.get_single_user(userId)
        
        return jsonify({"message": "Your user-group has been updated ", "Updated user informtion": edited_data}), 200
        
    def update_user_name(userId):
        """
            Function update name
            :return success message:
        """
        # userid = get_jwt_identity()
     
        # user = User()
        # if not userid:
        #     return jsonify({"message": "Unauthorised access"}), 401

        # editor = user.get_user_by_id(userid)['role']
        user = con.get_single_user(userId)
        if user['status'] == 0:
            return jsonify({"message":"The user with that account doesnt exist"}),404
        if not user:
            return jsonify({"message": "The user you are editing doesnt\
                            exist"}), 404
        # if not editor:
        #     return jsonify({"message": "You are not a registered user of the \
        #                     system"}), 401
        # if editor != 'user' or parcel['userid'] != userid:
        #     return jsonify({"message": "You can only update destination of the\
        #                      parcel you have created "}), 400
        request_data = request.get_json(force=True)
        if len(request_data.keys()) != 1:
            return jsonify({"message": "Some fields are missing"}), 400
        name = request_data['name']
        if (user['name'] == name):
            return jsonify({"message":"The name is already upto date"}),400
        validate_destination = Validator().validate_string_input(name)
        if not validate_destination:
            jsonify({"message": "name must be a non empty string"}), 400
        
        con.update_user_name(userId ,name)
        edited_data = con.get_single_user(userId)
        
        return jsonify({"message": "Your name has been updated ",
                        "updated user credentials": edited_data}), 200


    def update_user_role(userId):
        """
            Function update user_role
            :param userId:
            :param user_role:
            :return success message:
        """
        # userid = get_jwt_identity()
        
        # user = User()
        # if not userid:
        #     return jsonify({"message": "Unauthorised access"}), 401

        # editor = user.get_user_by_id(userid)['role']
        user = con.get_single_user(userId)
        if user['status'] == 0:
            return jsonify({"message":"The user with that account doesnt exist"}),404
        if not user:
            return jsonify({"message": "The user you are editing doesnt\
                            exist"}), 404
        # if not editor:
        #     return jsonify({"message": "You are not a registered user of the \
        #                     system"}), 401
        # if editor != 'user' or parcel['userid'] != userid:
        #     return jsonify({"message": "You can only update destination of the\
        #                      parcel you have created "}), 400
        request_data = request.get_json(force=True)
        if len(request_data.keys()) != 1:
            return jsonify({"message": "Some fields are missing"}), 400
        user_role = request_data['user_role']
        if (user['user_role'] == user_role):
            return jsonify({"message":"The user_role is already upto date"}),400
        validate_destination = Validator().validate_string_input(user_role)
        if not validate_destination:
            jsonify({"message": "user_role must be a non empty string"}), 400
        
        con.update_userrole(userId ,user_role)
        edited_data = con.get_single_user(userId)
        
        return jsonify({"message": "Your user_role has been updated ",
                        "updated user credentials": edited_data}), 200

                        
    def update_country(userId):
        """
            Function update country
            :param userId:
            :param country:
            :return success message:
        """
        # userid = get_jwt_identity()
        
        # user = User()
        # if not userid:
        #     return jsonify({"message": "Unauthorised access"}), 401

        # editor = user.get_user_by_id(userid)['role']
        user = con.get_single_user(userId)
        if user['status'] == 0:
            return jsonify({"message":"The user with that account doesnt exist"}),404
        if not user:
            return jsonify({"message": "The user you are editing doesnt\
                            exist"}), 404
        # if not editor:
        #     return jsonify({"message": "You are not a registered user of the \
        #                     system"}), 401
        # if editor != 'user' or parcel['userid'] != userid:
        #     return jsonify({"message": "You can only update destination of the\
        #                      parcel you have created "}), 400
        request_data = request.get_json(force=True)
        if len(request_data.keys()) != 1:
            return jsonify({"message": "Some fields are missing"}), 400
        country = request_data['country']
        if (user['country'] == country):
            return jsonify({"message":"The country is already upto date"}),400
        validate_destination = Validator().validate_string_input(name)
        if not validate_destination:
            jsonify({"message": "country must be a non empty string"}), 400
        
        con.update_userrole(userId ,country)
        edited_data = con.get_single_user(userId)
        
        return jsonify({"message": "Your country has been updated ",
                        "updated user credentials": edited_data}), 200
    def delete_user(userId):
        """
            Function delete
            :return success message:
        """
        # userid = get_jwt_identity()
        # if not userid:
        #     return jsonify({"message": "unauthorised access"}), 401
        # user = User()
        
        user_to_delete = con.get_single_user(userId)
        if user_to_delete['status'] == 0:
            return jsonify({"message":"The user with that account doesnt exist"}),404
        if not user_to_delete:
            return jsonify({"message": "The user you are trying to edit doesnt exist"}), 400

        con.delete_user(userId)
        return jsonify({"message": "Your account has been deleted"}), 200
        # editor = user.get_user_by_id(userid)['role']
        # if editor == 'admin':
        #     parcel.delete_parcel(parcelId)
        #     return jsonify({"message": "Your parcel has been deleted"}), 200
        # return jsonify({"message": "only administrators can delete parcels"}), 400
