"""
This program tests the database by performing queries
"""
import time
import datetime
import sqlite3
from sqlite3 import Error

def create_connection_to_lib_db():
    # create a database connection to the SQLite database specified by path
    db_path = r"library.db"
    conn = None

    try:
        conn = sqlite3.connect(db_path)
    except Error as e:
        print(e)
 
    print("Opened database successfully")
 
    return conn


def commit_and_close_connection(conn):
    # commit and close db
    if conn:
        conn.commit()
        print("Committed Changes!")
        conn.close()
        print("Closed database successfully")


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


def print_sub_menu_1():
    print("What would you liek to ask?")
    print("1. I would like to borrow a book")
    print("0. back")
    print("")


def find_item():
    conn = create_connection_to_lib_db()

    while True: 
        try:
            print("what item are you looking for ?")
            item_id = int(input("Please enter an item ID:"))
        except ValueError:
            print("Please enter a valid item id")
            continue
        # look for specified item 
        try:
            cur = conn.cursor()
            query = "SELECT itemID FROM ItemRecords WHERE itemID = :item_id;\n"
            cur.execute(query,{"item_id":item_id})
            result = cur.fetchall()
            if len(result) == 0:
                print("Item does not exist.\n") 
                continue
        except Error as e:
            print(e)

    for row in result:
        print(row)

    commit_and_close_connection(conn)


def borrow():
    conn = create_connection_to_lib_db()
    while True: 
        try:
            lib_number = int(input("What is your linrary number ?\n"))
        except ValueError:
            print("Please enter a valid library number")
            continue
        else: 
            # check if entered library id exists
            query = "SELECT libNumber FROM Person WHERE libNumber = :lib_number; \n"
            try:
                cur = conn.cursor()
                cur.execute(query,{"lib_number":lib_number})
                result = cur.fetchall()
                if len(result) == 0:
                    print("library number does not exist, please enter a valid library number") 
                    continue
            except Error as e:
                print(e)
            else:
                # valid input was entered
                break

    while True:
        try:
            print("Please hand in your desired borrowed item to be scanned:")
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
                result = cur.fetchall()
                if len(result) == 0:
                    print("item ID does not exist, please enter a valid item ID ") 
                    continue
            except Error as e:
                print(e)
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

    commit_and_close_connection(conn)


def return_item():
    conn = create_connection_to_lib_db()

    while True: 
        try:
            print("What item would you like to return ?")
            item_id = int(input("Enter item_id:"))
        except ValueError:
            print("Please enter a valid item ID")
            continue

    # update Borrow table and ItemRecords table

    commit_and_close_connection(conn)



def donate():
    conn = create_connection_to_lib_db()




    commit_and_close_connection(conn)



def find_event():
    conn = create_connection_to_lib_db()


    # fidn event
    query = " \n"
    execute_query(conn, query)

    commit_and_close_connection(conn)



def attend_event():
    conn = create_connection_to_lib_db()




    commit_and_close_connection(conn)



def volunteer():
    conn = create_connection_to_lib_db()




    commit_and_close_connection(conn)



def ask_librarian(input):
    conn = create_connection_to_lib_db()

    if input == "1":

    else


    commit_and_close_connection(conn)


def main():
    print_welcome_header() 

    while (1): 
        print_menu()
        action = input("Enter a number to execute one of the actions\n")
        if action == "1":
            find_item()
        elif action == "2":
            borrow()
        elif action == "3":
            return_item()
        elif action == "4":
            donate()
        elif action == "5":
            find_event()
        elif action == "6":
            attend_event()
        elif action == "7":
            volunteer()
        elif action == "8":
            while (1):
                print_sub_menu_1()
                sub_menu_input = input("What would you like to ask ?")
                if sub_menu_input == "0":
                    ask_librarian(sub_menu_input)
                else: 
                    print("Invalid input, please try again\n")
                    time.sleep(1)
        elif action == "0":
            break
        else:
            print("Invalid input, please try again\n")
            time.sleep(1)

    # create a database connection
    # conn = create_connection(database)
    # with conn:
    #    execute_query(conn, query1)
 
 
if __name__ == '__main__':
    main()