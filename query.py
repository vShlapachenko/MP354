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
 
    return conn


def commit_and_close_connection(conn):
    # commit and close db
    if conn:
        conn.commit()
        conn.close()


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


def print_goodbye():
    print("")
    print("<><><><><><><><")
    print("|!! GOODBYE !!|")
    print("><><><><><><><>")
    print("")


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
    print("1. I would like find a specific book")
    print("2. I would like to find a specific CD")
    print("3. I would like to find a specific magazine")
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
            query = "SELECT * FROM ItemRecords WHERE itemID = :item_id;\n"
            cur.execute(query,{"item_id":item_id})
            result = cur.fetchall()
            if len(result) == 0:
                print("Item does not exist.\n") 
                commit_and_close_connection(conn)
                return
            break
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
        
        try:
            cur = conn.cursor()

            # check if entered library id exists
            query = "SELECT libNumber FROM Person WHERE libNumber = :lib_number; \n"
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
        try:
            cur = conn.cursor()

            # check if entered item id exists
            query = "SELECT itemID FROM ItemRecords WHERE itemID = :item_id; \n"
            cur.execute(query,{"item_id":item_id})
            result = cur.fetchall()
            if len(result) == 0:
                print("item ID does not exist, please enter a valid item ID ") 
                continue

            # check if item is already borrowed
            query = "SELECT * FROM ItemRecords WHERE itemID = :item_id AND available = :false; \n"
            cur.execute(query,{"item_id":item_id, "false":False})
            result = cur.fetchall()
            if len(result) >= 1:
                print("item has already been borrowed") 
                commit_and_close_connection(conn)
                return
        except Error as e:
            print(e)
        else:
            # valid input was entered
            break
    
    # borrow item from library
    query = "INSERT INTO Borrow(libNumber, itemID) VALUES (?, ?); \n"
    values = (lib_number, item_id)
    try:
        cur = conn.cursor()
        conn.execute(query, values)
    except Error as e:
        print(e)

    print("item with id %d succesfully borrowed by %d", format(item_id, lib_number))

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
        try:
            cur = conn.cursor()

            # check if entered item id exists
            query = "SELECT itemID FROM ItemRecords WHERE itemID = :item_id; \n"
            cur.execute(query,{"item_id":item_id})
            result = cur.fetchall()
            if len(result) == 0:
                print("item ID does not exist, please enter a valid item ID ") 
                continue

            # check if item was never borrowed
            query = "SELECT * FROM borrow WHERE itemID = :item_id; \n"
            cur.execute(query,{"item_id":item_id})
            result = cur.fetchall()
            if len(result) == 0:
                print("Cannot return item that was not borrowed") 
                commit_and_close_connection(conn)
                return
            break
        except Error as e:
            print(e)
        else:
            # valid input was entered
            break

    # update Borrow table and ItemRecords table
    query = "DELETE FROM Borrow WHERE itemID = :item_id; \n"
    try:
        cur = conn.cursor()
        conn.execute(query, {"item_id":item_id})
    except Error as e:
        print(e)

    print("item with id %d succesfully returned", format(item_id))

    commit_and_close_connection(conn)


def donate_book():
    conn = create_connection_to_lib_db()

    while(1):
        try:
            cur = conn.cursor()
            item_id = input("Enter a unique ID for the book: ")

            # check if entered item id exists
            query = "SELECT itemID FROM ItemRecords WHERE itemID = :item_id; \n"
            cur.execute(query,{"item_id":item_id})
            result = cur.fetchall()
            if len(result) > 0:
                print("item ID already exists, please enter anotther unique item ID ") 
                continue

            break
        except Error as e:
            print(e)

    title = input("Enter book title: ")
    author = input("Enter author of the book: ")
    publisher = input("Enter publisher of book: ")

    # insert book 
    query = "INSERT INTO Book(itemID, title, author, publisher) VALUES (?, ?, ?, ?); \n"
    values = (item_id, title, author, publisher)
    try:
        cur = conn.cursor()
        conn.execute(query, values)
    except Error as e:
        print(e)

    print("Book successfully donated")

    commit_and_close_connection(conn)


def donate_cd():
    conn = create_connection_to_lib_db()

    while(1):
        try:
            cur = conn.cursor()
            item_id = input("Enter a unique ID for the CD: ")

            # check if entered item id exists
            query = "SELECT itemID FROM ItemRecords WHERE itemID = :item_id; \n"
            cur.execute(query,{"item_id":item_id})
            result = cur.fetchall()
            if len(result) > 0:
                print("item ID already exists, please enter anotther unique item ID ") 
                continue

            break
        except Error as e:
            print(e)

    title = input("Enter CD title: ")
    producer = input("Enter producer of the CD: ")
    director = input("Enter director of CD: ")

    # insert book 
    query = "INSERT INTO CD(itemID, title, producer, director) VALUES (?, ?, ?, ?); \n"
    values = (item_id, title, producer, director)
    try:
        cur = conn.cursor()
        conn.execute(query, values)
    except Error as e:
        print(e)
    
    print("CD successfully donated")

    commit_and_close_connection(conn)


def donate_mag():
    conn = create_connection_to_lib_db()

    while(1):
        try:
            cur = conn.cursor()
            item_id = input("Enter a unique ID for the magazine: ")

            # check if entered item id exists
            query = "SELECT itemID FROM ItemRecords WHERE itemID = :item_id; \n"
            cur.execute(query,{"item_id":item_id})
            result = cur.fetchall()
            if len(result) > 0:
                print("item ID already exists, please enter anotther unique item ID ") 
                continue

            break
        except Error as e:
            print(e)

    name = input("Enter magazine name: ")
    publisher = input("Enter publisher of the magazine: ")

    # insert book 
    query = "INSERT INTO Magazine(itemID, name, publisher) VALUES (?, ?, ?); \n"
    values = (item_id, name, publisher)
    try:
        cur = conn.cursor()
        conn.execute(query, values)
    except Error as e:
        print(e)
    
    print("Magazine successfully donated")

    commit_and_close_connection(conn)


def donate():

    while (1):
        print("What type of item whould you like to donate?")
        print("1. Book")
        print("2. CD")
        print("3. Magazine")
        print("0. back")
        print("")

        type = input("Enter type:")
        if type == "1":
            donate_book()
        elif type == "2":
            donate_cd()
        elif type == "3":
            donate_mag()
        elif type == "0":
            break
        else:
            print("Invalid input, please try again\n")
            time.sleep(1)


def find_event():
    conn = create_connection_to_lib_db()

    while True: 
        try:
            print("Enter the event ID of the event you wish to look for ?")
            event_id = int(input("Enter event_id:"))
            break
        except ValueError:
            print("Please enter a valid event ID")
            continue

    # look for specified event 
    try:
        cur = conn.cursor()
        query = "SELECT * FROM Event WHERE eventID = :event_id;\n"
        cur.execute(query,{"event_id":event_id})
        result = cur.fetchall()
        if len(result) == 0:
            print("Event does not exist.\n")
    except Error as e:
            print(e)

    commit_and_close_connection(conn)


def attend_event():
    conn = create_connection_to_lib_db()

    while True: 
        try:
            lib_number = int(input("What is your linrary number ?\n"))
        except ValueError:
            print("Please enter a valid library number")
            continue 
        
        try:
            cur = conn.cursor()

            # check if entered library id exists
            query = "SELECT libNumber FROM Person WHERE libNumber = :lib_number; \n"
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
            print("Which event would you like to attent?")
            event_id = int(input("Enter event ID:"))
        except ValueError:
            print("Please enter a validevent ID")
            continue 
        
        try:
            cur = conn.cursor()

            # check if entered event id exists
            query = "SELECT eventID FROM Event WHERE eventID = :event_id; \n"
            cur.execute(query,{"eventID":event_id})
            result = cur.fetchall()
            if len(result) == 0:
                print("Event does not exist") 
                commit_and_close_connection(conn)
                return
        except Error as e:
            print(e)
        else:
            # valid input was entered
            break

    # attend event
    query = "INSERT INTO Attend(libNumber, eventID) VALUES (?, ?) \n"
    values = (lib_number, event_id)
    try:
        cur = conn.cursor()
        conn.execute(query, values)
    except Error as e:
        print(e)

    print("Person with library number %d is going to attend event with event ID %d", format(lib_number, event_id))

    commit_and_close_connection(conn)


def volunteer():
    conn = create_connection_to_lib_db()

    while True: 
        try:
            print("Who would like to volunteer?")
            lib_number = int(input("Enter library number:"))
        except ValueError:
            print("Please enter a valid library number")
            continue 
        
        try:
            cur = conn.cursor()

            # check if entered library number exists
            query = "SELECT libNumber FROM Person WHERE libNumber = :lib_number; \n"
            cur.execute(query,{"lib_number":lib_number})
            result = cur.fetchall()
            if len(result) == 0:
                print("library number does not exist") 
                commit_and_close_connection(conn)
                return
        except Error as e:
            print(e)
        else:
            # valid input was entered
            break

    # insert into Personnel and set salary and ssn to null
    query = "INSERT INTO Personnel(libNumber, ssn, salary) VALUES (?, ?) \n"
    values = (lib_number, None, 0)
    try:
        cur = conn.cursor()
        conn.execute(query, values)
    except Error as e:
        print(e)

    print("Person with library number %d has volunteered!", format(lib_number))

    commit_and_close_connection(conn)


def ask_librarian():
    while (1):
        print_sub_menu_1()
        sub_menu_input = input("What would you like to ask ? \n")
        if sub_menu_input == "1":
            find_book()
        elif sub_menu_input == "2":
            find_cd()
        elif sub_menu_input == "3":
            find_mag()
        elif sub_menu_input == "0":
            break
        else:
            print("Invalid input, please try again\n")
            time.sleep(1)


def find_book():
    conn = create_connection_to_lib_db()

    print("What book would you like to find ?")
    book_name = input("Enter book Name:")

    try:
        cur = conn.cursor()

        # check if entered library number exists
        query = "SELECT * FROM Book WHERE title = :book_name; \n"
        cur.execute(query,{"book_name":book_name})
        result = cur.fetchall()
        if len(result) == 0:
            print("Requested book does not exist") 
            commit_and_close_connection(conn)
            return
        else:
            for row in result:
                print(row)
    except Error as e:
        print(e)

    commit_and_close_connection(conn)


def find_cd():
    conn = create_connection_to_lib_db()

    print("What CD would you like to find ?")
    cd_title = input("Enter CD title:")

    try:
        cur = conn.cursor()

        # check if entered library number exists
        query = "SELECT * FROM CD WHERE title = :cd_title; \n"
        cur.execute(query,{"cd_title":cd_title})
        result = cur.fetchall()
        if len(result) == 0:
            print("Requested CD does not exist") 
            commit_and_close_connection(conn)
            return
        else:
            for row in result:
                print(row)
    except Error as e:
        print(e)

    commit_and_close_connection(conn)


def find_mag():
    conn = create_connection_to_lib_db()

    print("What magazine would you like to find ?")
    mag_name = input("Enter magazine name:")

    try:
        cur = conn.cursor()

        # check if entered library number exists
        query = "SELECT * FROM Magazine WHERE name = :mag_name; \n"
        cur.execute(query,{"mag_name":mag_name})
        result = cur.fetchall()
        if len(result) == 0:
            print("Requested magazine does not exist") 
            commit_and_close_connection(conn)
            return
        else:
            for row in result:
                print(row)
    except Error as e:
        print(e)

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
            ask_librarian()
        elif action == "0":
            print_goodbye()
            break
        else:
            print("Invalid input, please try again\n")
            time.sleep(1)
 
 
if __name__ == '__main__':
    main()