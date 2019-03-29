import datetime
import pymysql
from .database import DatabaseConnection
con = DatabaseConnection()


class Association:       
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
        con.cursor.execute(add_association, val)
        

    def get_all_associations(self):
        """
            Function to fetch all associations
        """
        get_all = "SELECT * FROM statistic_association"
        con.dict_cursor.execute(get_all)
        associations = con.dict_cursor.fetchall()
        return associations
    def get_single_association(self, associationId):
        """
            Function to fetch all single association
            :param associationId:
        """
        association_query = "SELECT * FROM statistic_association WHERE associationId=%s"
        
        con.dict_cursor.execute(association_query, (associationId,))
        association = con.dict_cursor.fetchone()
        return association

    def cancel_association(self, associationId):
        """
            Function to cancel association
            :param associationId:
        """
        cancel_query = "UPDATE statistic_association SET status=%s WHERE associationId=%s"
        con.cursor.execute(cancel_query, (0, associationId))

    def delete_association(self, associationId):
        """
            Function to delete association
            :param associationId:
        """
        delete_query = "UPDATE  statistic_association SET status=%s WHERE associationId=%s"
        con.cursor.execute(delete_query, (0, associationId))

    def update_location(self, associationId, newlocation):
        """
            Function to update_location
            :param associationId:
            :param newlocation:
        """
        update_query = " UPDATE statistic_association SET Location=%s WHERE associationId=%s"
        con.cursor.execute(update_query, (newlocation, associationId))

    def update_name(self, associationId, newname):
        """
            Function to update_association name
            :param associationId:
            :param newname:
        """
        update_query = "UPDATE statistic_association SET name=%s WHERE associationId=%s"
        con.cursor.execute(update_query, (newname, associationId))

    def fetch_associations_by_user(self, userId):
        """
            Function to fetch all associations by a user
            :param userId:
        """
        fetch_parcels_by_user = "SELECT * FROM statistic_association WHERE userId=%s"
        con.dict_cursor.execute(fetch_parcels_by_user, (userId,))
        parcels = con.dict_cursor.fetchall()
        return parcels
