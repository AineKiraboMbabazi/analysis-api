import datetime
import pymysql
from password_generator import PasswordGenerator
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity)
from flask import request, jsonify
from validations import Validator
from ..models.government import Government
from .database import DatabaseConnection
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .users import User_Controller
con = DatabaseConnection()

def generate_password():
        password = PasswordGenerator()
        password.excludeschars = "!$%^,>+.*_-()#&~`?=<>" 
        return password.generate()

def sendmail(toaddr,update_url,password):
        fromaddr = "weatherstationsecure@gmail.com"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Administrator account creation"
        body ="Your password is" +password+ "Follow the link below to update your user credentials \n"+update_url
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(fromaddr, "W1meaict.")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
        return jsonify({"message":"email notification has been sent"}),200

class Government_Controller:

    def create_government():
        """
            controller to create a government

            :return object of created government:
        """

        current_user = get_jwt_identity()

        request_data = request.get_json(force=True)

        if len(request_data.keys()) != 5:
            return jsonify({"message": "Some fields are missing"}), 400

        
        user = con.get_single_user(current_user)
        
        if user['status'] == 0 or user['status'] == '0':
            return jsonify({"message": "User account has been deactivated"}), 400
        
        email = request_data['email']
        role = request_data['user_role']
        update_url = request_data['update_url']
        creation_date = datetime.date.today().strftime('%Y-%m-%d')
        updated_at = datetime.date.today().strftime('%Y-%m-%d')
        name = request_data['name']
        status = 'active'
        photo = request_data['photo']
        
        created_by= current_user
        updated_by = current_user
        validate_input = Validator()

        if not (validate_input.validate_string_input(name)):
            return jsonify({"message": "Name field should contain strings "}), 400
                            
        government=con.fetch_governments_by_name(name)
        
        if government:
            return jsonify({"message":"A government with that name already exists"}), 400
        
        government = Government(name, photo, status, created_by, creation_date, updated_by, updated_at).__dict__

        governmentId = con.create_government(government['name'], government['photo'], government['status'], government['created_by'], government['creation_date'], government['updated_by'], government['updated_at'])
        password = generate_password()
        user = User_Controller.create_admin_user(governmentId,role,email,password,name,created_by,creation_date,updated_by,updated_at)
        sendmail(email,update_url,password)
        
        return jsonify({"message": "Your government has been created", "government":request_data}), 201

    def fetch_all_governments():
        """
            controller fetch all governments
            :return governments list:
        """

        current_user_id = get_jwt_identity()

        User = con.get_single_user(current_user_id)
        
        role = User['user_role']
        
        if  role == 'super_admin':
            governments = con.get_all_governments()

            if governments == [] or len(governments) ==0:
                return jsonify({"message": "No governments found"}), 404

            return jsonify({
            'columns': [
            {
              'label': 'Name',
              'field': 'table_name',
              'sort': 'asc'
            },{
              'label': 'Flag',
              'field': 'photo',
              'sort': 'asc'
            },{
              'label': 'Created On',
              'field': 'creation_date',
              'sort': 'asc'
            }],
            
                'rows': governments
            
            }), 200
            
        
        return jsonify({"message":"Unauthorised access"}),401

    def fetch_pending_government():
        """
            controller fetch pending government
            :return government:
        """

        current_user_id = get_jwt_identity()
        
        user = con.get_single_user(current_user_id)
        user_role = user['user_role']

        if user['status'] == 0 or user['status'] == '0':
            return jsonify({"message": "Trying to edit government using a deactivated account"}), 400
            
        if user_role == 'super_admin':
            governments = con.fetch_pending_government()

            if  len(governments) == 0 or governments == []:
                return jsonify({"message": "No pending governments found "}), 404

            return jsonify({'government': governments}), 200

        return jsonify({"message":"Unauthorised access"}),401

    

    def fetch_specific_government(governmentId):
        """
            controller fetch specific government
            :return government:
        """

        single_government = con.get_single_government(governmentId)
        if not single_government:
            return jsonify({"message": "government with that id doesnot exist"}), 404
        return jsonify({'government': single_government}), 200


    def cancel_specific_government(governmentId):
        """
            controller cancel government
            :return success message:
        """

        current_user_id = get_jwt_identity()

        government_to_edit = con.get_single_government(governmentId)
        

        if government_to_edit == None :
            return jsonify({"message": "Cant update nonexistent government "}), 400
        
        if government_to_edit['status'] == '0':
            return jsonify({"message":"Cant update an inactive government "}),400
 
        User = con.get_single_user(current_user_id)
        role = User['user_role']
       
        if User['status'] == 0 or User['status'] == '0':
            return jsonify({"message": "Trying to edit government using a deactivated account"}), 400
            
        if role == 'super_admin':
            con.cancel_government(governmentId)
            return jsonify({"message": "Your government has been cancelled"}), 200

        return jsonify({"message": "Unauthorised access"}), 401         

  
    def update_name(governmentId):
        """
            Function update name
            :param governmentid:
            :return success message:
        """

        current_user_id = get_jwt_identity()

        if not current_user_id:
            return jsonify({'message': 'Missing token in the Authorization Header'}), 401

        User = con.get_single_user(current_user_id)
        role = User['user_role']
        if User['status'] == 0 or User['status'] == '0':
            return jsonify({"message": "user account inactive"}), 400
            
        government = con.get_single_government(governmentId)
        
        if not government or government['status'] == 0:
            return jsonify({"message": "Government not found"}), 404
                            
        request_data=request.get_json(force=True)
        
        if len(request_data.keys()) != 1:
            return jsonify({"message": "Some fields are missing"}), 400

        name = request_data['name']
        updated_at =  datetime.date.today().strftime('%Y-%m-%d')
        updated_by = current_user_id
        
        if (government['name'] == name):
            return jsonify({"message": "The name is already upto date"}), 400
            
        validate_name = Validator().validate_string_input(name)

        if not validate_name:
            return jsonify({"message": "name must be a non empty string"}), 400

        if  role == 'super_admin' or role == 'govt_super_admin' or role == 'govt_admin':
            con.update_govt_name(governmentId, name,updated_by,updated_at)
            government1 = con.get_single_government(governmentId)
            return jsonify({"message": "Your name has been updated ",
                        "updated government": government1}), 200

        return jsonify({"message": "unauthorised access"}), 401

    def update_photo(governmentId):
        """
            Function update name
            :param governmentid:
            :return success message:
        """

        current_user_id = get_jwt_identity()

        if not current_user_id:
            return jsonify({'message': 'Missing token in the Authorization Header'}), 401

        User = con.get_single_user(current_user_id)
        role = User['user_role']
        if User['status'] == 0 or User['status'] == '0':
            return jsonify({"message": "user account inactive"}), 400
            
        government = con.get_single_government(governmentId)
        
        if not government or government['status'] == 0:
            return jsonify({"message": "Government not found"}), 404
                            
        request_data=request.get_json(force=True)
        
        if len(request_data.keys()) != 1:
            return jsonify({"message": "Some fields are missing"}), 400

        photo = request_data['photo']
        updated_at =  datetime.date.today().strftime('%Y-%m-%d')
        updated_by = current_user_id
        
        if (government['photo'] == photo):
            return jsonify({"message": "The photo is already upto date"}), 400
            

        if  role == 'super_admin' or role == 'govt_super_admin' or role == 'govt_admin':
            con.update_govt_photo(photo, updated_by,updated_at,governmentId )
            government1 = con.get_single_government(governmentId)
            return jsonify({"message": "Your name has been updated ",
                        "updated government": government1}), 200

        return jsonify({"message": "unauthorised access"}), 401

    def delete_government(governmentId):
        """
            controller to delete
            :param governmentid:
            :return success message:
        """

        current_user_id = get_jwt_identity()

        government_to_edit = con.get_single_government(governmentId)
        if government_to_edit == None:
            return jsonify({"message": "The government doesnt exist"}), 400
            
        government_status = government_to_edit['status']
        
        if government_status == '0':
            return jsonify({"message": "Cant update an inactive government "}), 400
 
        User = con.get_single_user(current_user_id)
        if User['status'] == 0 or User['status'] == '0':
            return jsonify({"message": "user with id not found"}), 404
            
        role = User['user_role']

        if role == 'super_admin'or role == 'govt_super_admin' or role == 'govt_admin':
            con.delete_government(governmentId)
            return jsonify({"message": "Your government has been deleted"}), 200

        return jsonify({"message": "unauthorised access"}), 400
        

    