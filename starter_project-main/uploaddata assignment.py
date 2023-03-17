
#%%
import os
import sqlalchemy
SQLALCHEMY_SILENCE_UBER_WARNING = 1
SQLALCHEMY_WARN_20 = 0
import pandas as pd
import datetime
from sqlalchemy import text
import mysql.connector as msql
from mysql.connector import Error

db_host =  "34.175.28.179" # e.g. '127.0.0.1' ('172.17.0.1' if deployed to GAE Flex)
db_user =  "root" # e.g. 'my-db-user'
db_pass =   "%TGBnhy6" # e.g. 'my-db-password'
db_name =   "myflaskDB" # e.g. 'my-database'
db_port = 3306  # e.g. 3306




#creat new DB 
try:
    conn = msql.connect(host='34.175.28.179', user='root',  
                        password='%TGBnhy6')#give ur username, password
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE employee")
        print("Database is created")
except Error as e:
    print("Error while connecting to MySQL", e)
    
#Connec to exsting DB
def connect_tcp_socket(
    db_host, db_user, db_pass, db_name, db_port = 3306
    ) -> sqlalchemy.engine.base.Engine:
    """ Initializes a TCP connection pool for a Cloud SQL instance of MySQL. """

    engine = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL.create(
            drivername="mysql+pymysql",
            username=db_user,
            password=db_pass,
            host=db_host,
            port=db_port,
            database=db_name,
        ),
    )
    return engine

engine = connect_tcp_socket(db_host, db_user, db_pass, db_name, db_port)
conn = engine.connect()
print(conn)


result = conn.execute(text("SHOW TABLES;")).fetchall()
for r in result:
    print(r)

#articles = pd.read_csv("DATA/articles.csv")
#transactions_sample = pd.read_csv("DATA/transactions_sample.csv")
#customers = pd.read_csv("DATA/customers.csv")

#customers.to_sql(name = "customers", con = conn, if_exists = 'replace', index = False)
#articles.to_sql(name = "articles", con = conn, if_exists = 'replace', index = False)
#transactions_sample.to_sql(name = "transactions_sample", con = conn, if_exists = 'replace', index = False)


result = conn.execute(text("SHOW TABLES;")).fetchall()
for r in result:
    print(r)
 
# %%
query2 = text("""
            SELECT *
             FROM customers
             LIMIT 10;""")

query1= text("""
            SELECT *
            FROM articles
            LIMIT 10;""")

query3 = text("""
            SELECT *
             FROM transactions_sample
             LIMIT 10;""")

result = conn.execute(query2).fetchall()
for r in result:
    print(r)
    # print(dict(r))

# %%
