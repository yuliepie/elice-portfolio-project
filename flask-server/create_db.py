import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", passwd="root")
print("connected!")

cur = mydb.cursor()
# cur.execute("CREATE DATABASE elice_portfolio_db")
cur.execute("SHOW DATABASES")
for db in cur:
    print(db)
