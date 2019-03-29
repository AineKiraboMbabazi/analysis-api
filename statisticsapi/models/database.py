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
                associationId   INTERGER,
                Location VARCHAR(100),
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


if __name__ == '__main__':
    con = DatabaseConnection()
    con.create_db_tables()


