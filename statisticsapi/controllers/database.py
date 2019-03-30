#!/usr/bin/python3
import pymysql
import os

from flask import Flask,jsonify



app = Flask(__name__)


class DatabaseConnection:
    def __init__(self):
        """
            constructor to create a db connection
            :param dbname:
            :param user:
            :param password :
            :param host :
        """
        try:
            self.con_parameter = dict(
                database="myfarm_test",
                user="root",
                password="",
                host="localhost"
            )
            self.con = pymysql.connect(**self.con_parameter)
            self.con.autocommit(True)
            self.cursor = self.con.cursor()
            self.dict_cursor = self.con.cursor(pymysql.cursors.DictCursor)
            

        except Exception:
            return jsonify({"message": "Cant connect to database"})

    def create_db_tables(self):
        """
            Create users table
        """
        create_users_table = (
            """CREATE TABLE IF NOT EXISTS
            statistic_user(
                userId SERIAL PRIMARY KEY NOT NULL,
                name VARCHAR(50),
                associationId   INTERGER,
                user_group VARCHAR(100),
                user_role   VARCHAR(100),
                country VARCHAR(100),
                created_by VARCHAR(50),
                creation_date TIMESTAMP,
                FOREIGN KEY (associationId) REFERENCES statistic_association(associationId)ON UPDATE CASCADE
            );"""
        )

        create_associations_table = (
            """CREATE TABLE IF NOT EXISTS
            statistic_association(
                associationId SERIAL PRIMARY KEY NOT NULL,
                userId INTEGER,
                status INTEGER,
                creation_date TIMESTAMP,
                name VARCHAR(50),
                Location VARCHAR(100),
                created_by VARCHAR(50),
                FOREIGN KEY (userId) REFERENCES statistic_user(userId)ON UPDATE CASCADE
                );""")

        """
            execute cursor object to create tables
        """
        self.cursor.execute(create_users_table)
        self.cursor.execute(create_associations_table)

    def drop_table(self, table_name):
        """
            truncate a table
            :param table_name:
        """
        self.cursor.execute(
            "TRUNCATE TABLE {} RESTART IDENTITY CASCADE".format(table_name))

    def create_association(self, userId, name, Location, status,created_by,creation_date):
        """
            Function to create parcel delivery order

            :param userId:
            :param creation_date:
            :param status :
            :param name :
            :param location :
            :param associationId:
            :param created_by:
            
        """
        add_association = "INSERT INTO statistic_association (userId, name,  Location, status,created_by,creation_date ) VALUES (%s,%s,%s,%s,%s,%s)"
        val =(userId, name,  Location, status,created_by,creation_date)
        self.cursor.execute(add_association, val)
        

    def get_all_associations(self):
        """
            Function to fetch all associations
        """
        get_all = "SELECT * FROM statistic_association"
        self.dict_cursor.execute(get_all)
        associations = self.dict_cursor.fetchall()
        return associations
    def get_single_association(self, associationId):
        """
            Function to fetch all single association
            :param associationId:
        """
        association_query = "SELECT * FROM statistic_association WHERE associationId=%s"
        
        self.dict_cursor.execute(association_query, (associationId,))
        association = self.dict_cursor.fetchone()
        return association

    def cancel_association(self, associationId):
        """
            Function to cancel association
            :param associationId:
        """
        cancel_query = "UPDATE statistic_association SET status=%s WHERE associationId=%s"
        self.cursor.execute(cancel_query, (0, associationId))

    def delete_association(self, associationId):
        """
            Function to delete association
            :param associationId:
        """
        delete_query = "UPDATE  statistic_association SET status=%s WHERE associationId=%s"
        self.cursor.execute(delete_query, (0, associationId))

    def update_location(self, associationId, newlocation):
        """
            Function to update_location
            :param associationId:
            :param newlocation:
        """
        update_query = " UPDATE statistic_association SET Location=%s WHERE associationId=%s"
        self.cursor.execute(update_query, (newlocation, associationId))

    def update_name(self, associationId, newname):
        """
            Function to update_association name
            :param associationId:
            :param newname:
        """
        update_query = "UPDATE statistic_association SET name=%s WHERE associationId=%s"
        self.cursor.execute(update_query, (newname, associationId))

    def fetch_associations_by_user(self, userId):
        """
            Function to fetch all associations by a user
            :param userId:
        """
        fetch_parcels_by_user = "SELECT * FROM statistic_association WHERE userId=%s"
        self.dict_cursor.execute(fetch_parcels_by_user, (userId,))
        parcels = self.dict_cursor.fetchall()
        return parcels

    #################################################################################################
    #                                                                                               #
    #                              functions for the users model                                    #
    #                                                                                               #
    ################################################################################################

    def add_user(self, associationId, name, status,country, user_group,user_role,created_by,creation_date):
        """
            Function to add a user

            :param associationId:
            :param name:
            :param status:
            :param country :
            :param user_group :
            :param user_role :
            :param created_by:
            :param creation_date:
            
        """
        add_users = "INSERT INTO statistic_user ( associationId, name, status,country, user_group,user_role,created_by,creation_date ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        val =( associationId, name, status,country, user_group,user_role,created_by,creation_date)
        self.cursor.execute(add_users, val)
        

    def get_all_users(self):
        """
            Function to fetch all users
        """
        get_all = "SELECT * FROM statistic_user"
        self.dict_cursor.execute(get_all)
        users = self.dict_cursor.fetchall()
        return users


    def get_single_user(self, userId):
        """
            Function to fetch all single user
            :param userId:
        """
        user_query = "SELECT * FROM statistic_user WHERE userId=%s"
        
        self.dict_cursor.execute(user_query, (userId,))
        user = self.dict_cursor.fetchone()
        return user

    def cancel_user(self, userId):
        """
            Function to cancel user
            :param userId:
        """
        cancel_query = "UPDATE statistic_user SET status=%s WHERE userId=%s"
        self.cursor.execute(cancel_query, (0, userId))

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




if __name__ == '__main__':
    con = DatabaseConnection()
    con.create_db_tables()


