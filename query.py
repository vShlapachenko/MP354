"""
This program test the database by performing queries
"""

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


def main():
    database = r"library.db"

    query1 = """
    """
 
    # create a database connection
    conn = create_connection(database)
    with conn:
       execute_query(conn, query1)
 
 
if __name__ == '__main__':
    main()