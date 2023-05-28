import os
import pymysql
from flask import jsonify

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')



unix_socket = '/cloudsql/{}'.format('turing-micron-387618:asia-south1:flaskbackend')
try:
        if os.environ.get('GAE_ENV') == 'standard':
            conn = pymysql.connect(user='priyank',
                                   password=12345,
                                   unix_socket=unix_socket,
                                   db='gfg',
                                   cursorclass=pymysql.cursors.DictCursor
                                   )
            print("Connection Successfully Established")

except pymysql.MySQLError as e:
    print(e)

    

