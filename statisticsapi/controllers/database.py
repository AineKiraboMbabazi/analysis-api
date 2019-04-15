#!/usr/bin/python3
import pymysql
import os

from flask import Flask,jsonify



app = Flask(__name__)


class DatabaseConnection:

    #################################################################################################
    #                                                                                               #
    #                              functions to setup the database                                  #
    #                                                                                               #
    ################################################################################################
    def __init__(self):
        """
            constructor to create a db connection
            :param dbname:
            :param user:
            :param password :
            :param host :
        """
        try:
            db = 'myfarm_test'
            if os.getenv('APP_SETTINGS') == 'testing':
                db = 'test_db'
            self.con_parameter = dict(
                database=db,
                user="root",
                password="",
                host="localhost"
            )
            self.con = pymysql.connect(**self.con_parameter)
            self.con.autocommit(True)
            self.cursor = self.con.cursor()
            self.dict_cursor = self.con.cursor(pymysql.cursors.DictCursor)
            

        except Exception:
            return jsonify({"message": "Cant connect to database"}),500

    def create_db_tables(self):
        """
            Create users table
        """
        create_users_table = 'CREATE TABLE  IF NOT EXISTS statistic_user (userId INT NOT NULL AUTO_INCREMENT PRIMARY KEY,name VARCHAR(50),associationId VARCHAR(10),governmentId VARCHAR(10),user_group VARCHAR(20),status VARCHAR(20),user_role VARCHAR(20),email VARCHAR(50),password VARCHAR(200),country VARCHAR(100),created_by VARCHAR(50),creation_date TIMESTAMP )'
                
        # ,CONSTRAINT assoc_id FOREIGN KEY fk_association_id(associationId) REFERENCES statistic_association (associationId) ON UPDATE CASCADE
            
        

        create_associations_table = 'CREATE TABLE IF NOT EXISTS statistic_association(associationId INT NOT NULL AUTO_INCREMENT PRIMARY KEY,userId VARCHAR(20),status VARCHAR(20),creation_date TIMESTAMP,name VARCHAR(50),Location VARCHAR(100),created_by VARCHAR(50))'

        create_government_table = 'CREATE TABLE IF NOT EXISTS statistic_government(governmentId INT NOT NULL AUTO_INCREMENT PRIMARY KEY,userId VARCHAR(10),associationId VARCHAR(10),status VARCHAR(20),creation_date TIMESTAMP,name VARCHAR(50),Location VARCHAR(100),created_by VARCHAR(50))'
                
        # ,CONSTRAINT user_id FOREIGN KEY fk_user_id(userId) REFERENCES statistic_user(userId) ON UPDATE CASCADE
                
                
        # create_blacklist_table = 'CREATE TABLE IF NOT EXISTS blacklist(token VARCHAR(200))'

                

        """
            execute cursor object to create tables
        """
        self.cursor.execute(create_users_table)
        self.cursor.execute(create_associations_table)
        self.cursor.execute(create_government_table)
        # self.cursor.execute(create_blacklist_table)

    def drop_table(self, table_name):
        """
            truncate a table
            :param table_name:
        """
        self.cursor.execute(
            "TRUNCATE TABLE {} ".format(table_name))

    #################################################################################################
    #                                                                                               #
    #                              functions for the associations model                             #
    #                                                                                               #
    ################################################################################################

    def create_association(self, userId, name, Location, status,created_by,creation_date):
        """
            Function to create an association

            :param userId:
            :param creation_date:
            :param status :
            :param name :
            :param location :
            :param associationId:
            :param created_by:
            :return created association: 
        """
        add_association = "INSERT INTO statistic_association (userId, name,  Location, status,created_by,creation_date ) VALUES (%s,%s,%s,%s,%s,%s)"
        val =(userId, name,  Location, status,created_by,creation_date)
        self.cursor.execute(add_association, val)
        

    def get_all_associations(self):
        """
            Function to fetch all associations
            
            :return all associations:
        """

        get_all = "SELECT * FROM statistic_association"
        self.dict_cursor.execute(get_all)
        associations = self.dict_cursor.fetchall()
        return associations

    def get_single_association(self, associationId):
        """
            Function to fetch all single association

            :param associationId:
            :return association:
        """

        association_query = "SELECT * FROM statistic_association WHERE associationId=%s"
        
        self.dict_cursor.execute(association_query, (associationId,))
        association = self.dict_cursor.fetchone()
        return association

    def cancel_association(self, associationId):
        """
            Function to cancel association

            :param associationId:
            :return successful cancellation message:
        """

        cancel_query = "UPDATE statistic_association SET status=%s WHERE associationId=%s"
        self.cursor.execute(cancel_query, (0, associationId))

    def approve_association(self, associationId):
        """
            Function to approve association

            :param associationId:
            :return email notification to association author:
        """

        approve_query = "UPDATE statistic_association SET status=%s WHERE associationId=%s"
        self.cursor.execute(approve_query, ('approved', associationId))

    def delete_association(self, associationId):
        """
            Function to delete association

            :param associationId:
            :return successful deletion message:
        """

        delete_query = "UPDATE  statistic_association SET status=%s WHERE associationId=%s"
        self.cursor.execute(delete_query, (0, associationId))

    def update_location(self, associationId, newlocation):
        """
            Function to update_location

            :param associationId:
            :param newlocation:
            :return updated object:
        """

        update_query = " UPDATE statistic_association SET Location=%s WHERE associationId=%s"
        self.cursor.execute(update_query, (newlocation, associationId))

    def update_association_name(self, associationId, name):
        """
            Function to update_association name

            :param associationId:
            :param newname:
            :return succeful update message:
        """

        update_query = """ UPDATE statistic_association SET name=%s WHERE associationId=%s"""
        self.cursor.execute(update_query, (name,associationId))

        
    def fetch_associations_by_user(self, userId):
        """
            Function to fetch all associations by a user

            :param userId:
            :return association:
        """

        fetch = "SELECT * FROM statistic_association WHERE userId=%s"
        self.dict_cursor.execute(fetch, (userId,))
        associations = self.dict_cursor.fetchall()
        return associations

    def fetch_associations_in_country(self, Location):
        """
            Function to fetch all associations in country

            :param Location:
            :return associations in country:
        """

        fetch = "SELECT * FROM statistic_association WHERE Location=%s"
        self.dict_cursor.execute(fetch, (Location,))
        associations = self.dict_cursor.fetchall()
        return associations

    def fetch_associations_by_name(self, name):
        """
            Function to fetch associations by name

            :param name:
            :return associations with query name:
        """

        fetch = "SELECT * FROM statistic_association WHERE name=%s"
        self.dict_cursor.execute(fetch, (name,))
        association = self.dict_cursor.fetchone()
        return association

    def fetch_pending_association(self):
        """
            Function to fetch all pending associations 

            :return all associations whose status is pending:
        """

        fetch = "SELECT * FROM statistic_association WHERE status=%s"
        self.dict_cursor.execute(fetch, ('pending',))
        associations = self.dict_cursor.fetchall()
        return associations



    #################################################################################################
    #                                                                                               #
    #                              functions for the government model                               #
    #                                                                                               #
    ################################################################################################


    def create_government(self, userId, name, Location, status,created_by,creation_date):
        """
            Function to create an government

            :param userId:
            :param creation_date:
            :param status :
            :param name :
            :param location :
            :param governmentId:
            :param created_by:
            :return created government: 
        """
        add_government = "INSERT INTO statistic_government (userId, name,  Location, status,created_by,creation_date ) VALUES (%s,%s,%s,%s,%s,%s)"
        val =(userId, name,  Location, status,created_by,creation_date)
        self.cursor.execute(add_government, val)
        

    def get_all_governments(self):
        """
            Function to fetch all governments
            
            :return all governments:
        """

        get_all = "SELECT * FROM statistic_government"
        self.dict_cursor.execute(get_all)
        governments = self.dict_cursor.fetchall()
        return governments

    def get_single_government(self, governmentId):
        """
            Function to fetch single government

            :param governmentId:
            :return government:
        """

        government_query = "SELECT * FROM statistic_government WHERE governmentId=%s"
        
        self.dict_cursor.execute(government_query, (governmentId,))
        government = self.dict_cursor.fetchone()
        return government

    def cancel_government(self, governmentId):
        """
            Function to cancel government

            :param governmentId:
            :return successful cancellation message:
        """

        cancel_query = "UPDATE statistic_government SET status=%s WHERE governmentId=%s"
        self.cursor.execute(cancel_query, (0, governmentId))

    def approve_government(self, governmentId):
        """
            Function to approve government

            :param governmentId:
            :return email notification to government author:
        """

        approve_query = "UPDATE statistic_government SET status=%s WHERE governmentId=%s"
        self.cursor.execute(approve_query, ('approved', governmentId))

    def delete_government(self, governmentId):
        """
            Function to delete government

            :param governmentId:
            :return successful deletion message:
        """

        delete_query = "UPDATE  statistic_government SET status=%s WHERE governmentId=%s"
        self.cursor.execute(delete_query, (0, governmentId))

    def update_location(self, governmentId, newlocation):
        """
            Function to update_location

            :param governmentId:
            :param newlocation:
            :return updated object:
        """

        update_query = " UPDATE statistic_government SET Location=%s WHERE governmentId=%s"
        self.cursor.execute(update_query, (newlocation, governmentId))

    def update_name(self, governmentId, newname):
        """
            Function to update_government name

            :param governmentId:
            :param newname:
            :return succeful update message:
        """

        update_query = "UPDATE statistic_government SET name=%s WHERE governmentId=%s"
        self.cursor.execute(update_query, (newname, governmentId))

    def fetch_governments_by_name(self, name):
        """
            Function to fetch all governments by a user

            :param userId:
            :return government:
        """

        fetch = "SELECT * FROM statistic_government WHERE name=%s"
        self.dict_cursor.execute(fetch, (name,))
        governments = self.dict_cursor.fetchall()
        return governments

    def fetch_governments_in_country(self, Location):
        """
            Function to fetch all governments in country

            :param Location:
            :return governments in country:
        """

        fetch = "SELECT * FROM statistic_government WHERE Location=%s"
        self.dict_cursor.execute(fetch, (Location,))
        governments = self.dict_cursor.fetchall()
        return governments

    def fetch_governments_by_name(self, name):
        """
            Function to fetch governments by name

            :param name:
            :return governments with query name:
        """

        fetch = "SELECT * FROM statistic_government WHERE name=%s"
        self.dict_cursor.execute(fetch, (name,))
        government = self.dict_cursor.fetchone()
        return government

    def fetch_pending_government(self):
        """
            Function to fetch all pending governments 

            :return all governments whose status is pending:
        """

        fetch = "SELECT * FROM statistic_government WHERE status=%s"
        self.dict_cursor.execute(fetch, ('pending',))
        governments = self.dict_cursor.fetchall()
        return governments


    #################################################################################################
    #                                                                                               #
    #                              functions for the users model                                    #
    #                                                                                               #
    ################################################################################################

    def add_user(self, associationId,governmentId, name, status,email,password,country, user_group,user_role,created_by,creation_date):
        """
            Function to add a user

            :param associationId:
            :param governmentId:
            :param name:
            :param status:
            :param email:
            :param password:
            :param country :
            :param user_group :
            :param user_role :
            :param created_by:
            :param creation_date:
        """

        add_users = "INSERT INTO statistic_user ( associationId,governmentId, name, status,email,password,country, user_group,user_role,created_by,creation_date ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val =( associationId,governmentId, name, status,email,password,country, user_group,user_role,created_by,creation_date)
        self.cursor.execute(add_users, val)
        

    def get_all_users(self):
        """
            Function to fetch all users
        """

        get_all = "SELECT * FROM statistic_user"
        self.dict_cursor.execute(get_all)
        users = self.dict_cursor.fetchall()
        return users

    def get_pending_accounts(self):
        """
            Function to fetch all pending accounts
        """

        get_all = "SELECT * FROM statistic_user WHERE status = %s"
        self.dict_cursor.execute(get_all,('pending'))
        users = self.dict_cursor.fetchall()
        return users


    def get_single_user(self, userId):
        """
            Function to fetch single user
            :param userId:
        """

        user_query = "SELECT * FROM statistic_user WHERE userId=%s"
        self.dict_cursor.execute(user_query, (userId,))
        user = self.dict_cursor.fetchone()
        return user

    def get_user_by_email(self, email):
        """
            Function to fetch user by email
            :param email:
        """

        user_query = "SELECT * FROM statistic_user WHERE email=%s"
        self.dict_cursor.execute(user_query, (email,))
        user = self.dict_cursor.fetchone()
        return user

    def cancel_user(self, userId):
        """
            Function to cancel user
            :param userId:
        """

        cancel_query = "UPDATE statistic_user SET status=%s WHERE userId=%s"
        self.cursor.execute(cancel_query, (0, userId))
    
    def reset_password(self, email, newpassword):
        """
            Function to cancel user
            :param email:
            :param newpassword:
        """

        reset_query = "UPDATE statistic_user SET password=%s WHERE email=%s"
        self.cursor.execute(reset_query, (newpassword,email))

    def delete_user(self, userId):
        """
            Function to delete user
            :param userId:
        """

        delete_query = "UPDATE  statistic_user SET status=%s WHERE userId=%s"
        self.cursor.execute(delete_query, (0, userId))

    def update_usergroup(self, userId, user_group):
        """
            Function to update_usergroup
            :param userId:
            :param user_group:
        """

        update_query = " UPDATE statistic_user SET user_group=%s WHERE userId=%s"
        self.cursor.execute(update_query, (user_group, userId))

    def update_userrole(self, userId, user_role):
        """
            Function to update_user role
            :param user_role:
            :param userId:
        """

        update_query = "UPDATE statistic_user SET user_role=%s WHERE userId=%s"
        self.cursor.execute(update_query, (userId, user_role))

    def update_country(self, userId, country):
        """
            Function to update_user country
            :param userId:
            :param country:
        """

        update_query = "UPDATE statistic_user SET country=%s WHERE userId=%s"
        self.cursor.execute(update_query, (userId, country))

    def update_user_name(self, userId, name):
        """
            Function to update_user name
            :param userId:
            :param name:
        """

        update_query = "UPDATE statistic_user SET name=%s WHERE userId=%s"
        self.cursor.execute(update_query, (userId, name))


    #################################################################################################
    #                                                                                               #
    #                              functions for the users logout                                   #
    #                                                                                               #
    ################################################################################################


    def add_to_blacklist(self, token):
        """
            function to add tokens to blacklist on logout
            :param token:
            :return successful logout message:
        """

        add_to_blacklist = "INSERT INTO blacklist ( token ) VALUES (%s)"
        val =( token)
        self.cursor.execute(add_to_blacklist, val)


if __name__ == '__main__':
    con = DatabaseConnection()
    con.create_db_tables()


