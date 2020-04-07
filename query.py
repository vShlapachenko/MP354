"""
This program tests the database by performing queries
"""
import time
import datetime
import sqlite3
from sqlite3 import Error

def create_connection(path):
    # create a database connection to the SQLite database specified by path
    conn = None
    try:
        conn = sqlite3.connect(path)
        return conn
    except Error as e:
        print(e)
 
    return conn


def execute_query(conn, query):
    cur = conn.cursor()
    cur.execute(query)
 
    rows = cur.fetchall()
 
    for row in rows:
        print(row)


def print_welcome_header():
    print("\n")
    print("<><><><><><><><><><><><><><><><><><>")
    print("|      WELCOME TO OUR LIBRARY      |")
    print("><><><><><><><><><><><><><><><><><><")
    print("\n")


def print_menu():
    print("\n")
    print("Enter a number to execute one of the actions:")
    print("1. Find an item in the library")
    print("2. Borrow an item from the library")
    print("3. Return a borrowed item")
    print("4. Donate an item to the library")
    print("5. Find an event in the library")
    print("6. Register for an event in the library")
    print("7. Volunteer for the library")
    print("8. Ask for help from a librarian")
    print("0. leave library")
    print("")


def sub_menu_1():
    print(" \n")


def find_item():
    db_path = r"library.db"
    conn = create_connection(db_path)
    print("Opened database successfully \n")

    while True: 
        try:
            print("what item are you looking for ? \n")
            item_id = int(input("Please enter an item ID:"))
        except ValueError:
            print("Please enter a valid item id\n")
            continue

    # look for specified item 
    query = "SELECT libNumber FROM Person WHERE libNumber = :lib_number; \n"
    execute_query(conn, query)

    # commit and close db
    if conn:
        conn.commit()
        print("Committed Changes!\n")
        conn.close()
        print("Closed database successfully")


def borrow():
    db_path = r"library.db"
    conn = create_connection(db_path)
    print("Opened database successfully \n")
    while True: 
        try:
            lib_number = int(input("What is your linrary number ?\n"))
        except ValueError:
            print("Please enter a valid library number\n")
            continue
        else: 
            # check if entered library id exists
            query = "SELECT libNumber FROM Person WHERE libNumber = :lib_number; \n"
            try:
                cur = conn.cursor()
                cur.execute(query,{"lib_number":lib_number})
                result = cur.fetchall()
                if len(result) == 0:
                    print("library number does not exist, please enter a valid library number \n") 
                    continue
            except Error as e:
                print(e)
            else:
                # valid input was entered
                break

    while True:
        try:
            print("Please hand in your desired borrowed item to be scanned: \n")
            item_id = int(input("Please enter an itemID:"))
        except ValueError:
            print("Please enter a valid itemID\n")
            continue
        else:
            # check if entered item id exists
            query = "SELECT itemID FROM ItemRecords WHERE itemID = :item_id; \n"
            try:
                cur = conn.cursor()
                cur.execute(query,{"item_id":item_id})
            except Error as e:
                print(e)
                print("library number does not exist, please enter a valid library number \n") 
            else:
                # valid input was entered
                break

    # borrow item from library
    query = ""
    try:
        cur = conn.cursor()
        conn.execute(query,{" ":})
    except Error as e:
        print(e)

    # commit and close db
    if conn:
        conn.commit()
        print("Committed Changes!\n")
        conn.close()
        print("Closed database successfully")


def return_item():
    db_path = r"library.db"
    conn = create_connection(db_path)
    print("Opened database successfully \n")

    while True: 
        try:
            print("What item would you like to return ?\n")
            item_id = int(input("Enter item_id:"))
        except ValueError:
            print("Please enter a valid item ID\n")
            continue

    # update Borrow table and ItemRecords table

    # commit and close db
    if conn:
        conn.commit()
        print("Committed Changes!\n")
        conn.close()
        print("Closed database successfully")


def donate():
    db_path = r"library.db"
    conn = create_connection(db_path)
    print("Opened database successfully \n")



    # commit and close db
    if conn:
        conn.commit()
        print("Committed Changes!\n")
        conn.close()
        print("Closed database successfully")


def find_event():
    db_path = r"library.db"
    conn = create_connection(db_path)
    print("Opened database successfully \n")

    # fidn event
    query = " \n"
    execute_query(conn, query)

    # commit and close db
    if conn:
        conn.commit()
        print("Committed Changes!\n")
        conn.close()
        print("Closed database successfully")


def attend_event():
    db_path = r"library.db"
    conn = create_connection(db_path)
    print("Opened database successfully \n")



    # commit and close db
    if conn:
        conn.commit()
        print("Committed Changes!\n")
        conn.close()
        print("Closed database successfully")


def volunteer():
    db_path = r"library.db"
    conn = create_connection(db_path)
    print("Opened database successfully \n")



    # commit and close db
    if conn:
        conn.commit()
        print("Committed Changes!\n")
        conn.close()
        print("Closed database successfully")


def ask_librarian():
    db_path = r"library.db"
    conn = create_connection(db_path)
    print("Opened database successfully \n")



    # commit and close db
    if conn:
        conn.commit()
        print("Committed Changes!\n")
        conn.close()
        print("Closed database successfully")


def main():
    print_welcome_header() 

    while (1): 
        print_menu()
        action = input("What would you like to do ? \n")
        if action == "1":
            find_item()
        elif action == "2":
            borrow()
        elif action == "3":
            reutrn_item()
        elif action == "4":
            donate()
        elif action == "5":
            find_event()
        elif action == "6":
            attend_event()
        elif action == "7":
            volunteer()
        elif action == "8":
            ask_librarian()
        elif action == "0":
            break
        else:
            print("Invalid input, please try again\n")
            time.sleep(1)

    # create a database connection
    conn = create_connection(database)
    with conn:
       execute_query(conn, query1)
 
 
if __name__ == '__main__':
    main()