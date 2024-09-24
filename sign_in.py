import mysql.connector
from db_connection import connection as c

if c and c.is_connected():
    print("Sign in")
    while True:
        user = input("username: ")
        pwd = input("password: ")
        with c.cursor() as cursor:
            query = f"""SELECT username, pwd FROM users
            WHERE username LIKE '{user}' AND pwd LIKE {pwd}"""
            result = cursor.execute(query)
            rows = cursor.fetchmany(1)
            if len(rows) > 0:
                if user == rows[0][0] and int(pwd) == rows[0][1]:
                    print("signing in...")
                    break
            print("Error typing username and password, or does not exist.")

c.close()