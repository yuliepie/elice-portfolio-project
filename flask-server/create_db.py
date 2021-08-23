import mysql.connector

DB_NAME = "elice_portfolio_db"

mydb = mysql.connector.connect(host="localhost", user="root", passwd="root")
print("connected!")

cursor = mydb.cursor()

# cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
# print("Database {} created successfully.".format(DB_NAME))

mydb.database = DB_NAME

# Seed eduation status codes
statuses = ["재학중", "학사졸업", "석사졸업", "박사졸업"]
for status in statuses:
    cursor.execute(f"INSERT INTO education_status(status_name) VALUES('{status}')")

mydb.commit()
cursor.close()

mydb.close()
