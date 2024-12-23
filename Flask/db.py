from datetime import datetime
import mysql.connector
import json

def connect():
    database = mysql.connector.connect(
        host="jakubplewa.pl",
        user="jakub",
        password="jakub",
        port=3606
    )
    return database

def get_user(username, password):
    database = connect()
    cursor = database.cursor()

    # Zapytanie do bazy danych
    query = "SELECT password FROM `lokal-kebab`.Users WHERE username = %s AND password = %s" 
    cursor.execute(query, (username, password))

    result = cursor.fetchone()

    cursor.close()
    database.close()
    return result

def get_menu():
    database = connect()
    cursor = database.cursor(dictionary=True)
    # Zapytanie do bazy danych
    query = "SELECT name, price, description, img_url FROM `lokal-kebab`.Menu" 
    cursor.execute(query)

    result = cursor.fetchall()
    result = json.dumps(result)

    cursor.close()
    database.close()
    return result

def get_user_data(user):
    database = connect()
    cursor = database.cursor(dictionary=True)

    query = "SELECT username, password, email, city, street, apartment_num, phone FROM `lokal-kebab`.Users WHERE username = %s"
    cursor.execute(query, (user,))

    result = cursor.fetchone()
    result = json.dumps(result)

    cursor.close()
    database.close()
    return result

def change_user_data(column, data, user):
    database = connect()
    cursor = database.cursor()

    if column == "email":
        query = "UPDATE `lokal-kebab`.Users SET email = %s WHERE username = %s"
    elif column == "password":
        query = "UPDATE `lokal-kebab`.Users SET password = %s WHERE username = %s"        
    elif column == "city":
        query = "UPDATE `lokal-kebab`.Users SET city = %s WHERE username = %s"
    elif column == "street":
        query = "UPDATE `lokal-kebab`.Users SET street = %s WHERE username = %s"
    elif column == "apartment_num":
        query = "UPDATE `lokal-kebab`.Users SET apartment_num = %s WHERE username = %s"
    elif column == "phone":
        query = "UPDATE `lokal-kebab`.Users SET phone = %s WHERE username = %s"

    cursor.execute(query, (data, user))
    database.commit()

    cursor.close()
    database.close()

def check_username(username):
    database = connect()
    cursor = database.cursor()

    query = "SELECT username FROM `lokal-kebab`.Users WHERE username = %s" 
    cursor.execute(query, (username,))

    result = cursor.fetchone()

    cursor.close()
    database.close()
    return result

def create_user(username, password, email, phone):
    database = connect()
    cursor = database.cursor()

    query = "INSERT INTO `lokal-kebab`.Users (username, password, email, phone) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (username, password, email, phone)) 
    database.commit()

    cursor.close()
    database.close()

    return 'success'

def make_order(username, items, city, street, apartment_num, phone):
    try:
        if username == None:
            username = create_guest(city, street, apartment_num, phone)
            if username == None:
                return 'failed'

        database = connect()
        cursor = database.cursor()

        query = "SELECT menu_id FROM `lokal-kebab`.Menu WHERE name = %s"
        menu_ids = []
        for item in items:
            cursor.execute(query, (item["name"],))
            result = cursor.fetchone()  # Pobiera jeden wynik
            if result:  # Sprawdza, czy wynik istnieje
                menu_ids.append(result[0])  # Dodaje menu_id (pierwsza kolumna w wyniku zapytania)

        query = "SELECT user_id FROM `lokal-kebab`.Users WHERE username = %s"
        cursor.execute(query, (username,)) 
        user_id = cursor.fetchone()[0]

        start_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = "In progress"

        query = "INSERT INTO `lokal-kebab`.Orders (status, Users_user_id, startDate) VALUES (%s, %s, %s)"
        cursor.execute(query, (status, user_id, start_date)) 
        order_id = cursor.lastrowid

        query = "INSERT INTO `lokal-kebab`.Order_menu (order_id, menu_id) VALUES (%s, %s)"
        for menu_id in menu_ids:
            cursor.execute(query, (order_id, menu_id)) 

        database.commit()

        cursor.close()
        database.close()

        return 'success'
    except:
        print("Cannot make an order")
        return 'failed'

def create_guest(city, street, apartment_num, phone):
    try:
        start_date = datetime.now().strftime('%d%m%Y%H%M%S')
        username = "guest" + start_date
    
        database = connect()
        cursor = database.cursor()

        query = "INSERT INTO `lokal-kebab`.Users (username, city, street, apartment_num, phone, is_temp) VALUES (%s, %s, %s, %s, %s, 'YES')"
        cursor.execute(query, (username, city, street, apartment_num, phone))

        database.commit()

        cursor.close()
        database.close()

        return username
    except:
        print("Cannot create a guest account")
        return None