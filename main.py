import mysql.connector

connection = mysql.connector.connect(user="root", password="Lujazoo6538#", host="127.0.0.1", database="clothes_store")

if connection and connection.is_connected():
    with connection.cursor() as cursor:
        result = cursor.execute("SELECT * FROM brands")
        rows = cursor.fetchall()

        for row in rows:
            print(row)

connection.close()