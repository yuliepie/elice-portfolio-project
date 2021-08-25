import mysql.connector
import os

DB_NAME = os.getenv("DATABASE_NAME", default="elice_portfolio_db")
DB_HOST = os.getenv("DATABASE_NAME", default="localhost")
DB_USER = os.getenv("DATABASE_NAME", default="root")
DB_PASSWORD = os.getenv("DATABASE_NAME", default="root")

mydb = mysql.connector.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD)
print("connected!")

mydb.database = DB_NAME
cursor = mydb.cursor()

# Seed eduation status codes
statuses = ["재학중", "학사졸업", "석사졸업", "박사졸업"]
for status in statuses:
    cursor.execute(f"INSERT INTO education_status(status_name) VALUES('{status}')")

mydb.commit()
cursor.close()

mydb.close()
