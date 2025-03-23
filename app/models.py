import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Abu2019#',
        database='url_shortener'
    )
    return connection

