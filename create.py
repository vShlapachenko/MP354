"""
This script creates the library.db and the its tables
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
 
 
def create_table(conn, create_table_statement):
    # create a table from the create_table_statement
    try:
        c = conn.cursor()
        c.execute(create_table_statement)
    except Error as e:
        print(e)
 
 
def create_trigger(conn, create_trigger_statement):
    # create a table from the create_trigger_statement
    try:
        c = conn.cursor()
        c.execute(create_trigger_statement)
    except Error as e:
        print(e)


def main():
    database = r"library.db"
 
    """
    CREATE statements
    """
    # entity sets
    person = """
    CREATE TABLE IF NOT EXISTS Person (
        libNumber    INTEGER,
        firstName    CHAR(30),
        lstName      CHAR(30),
        PRIMARY KEY (libNumber)
    );
    """
 
    personnel = """
    CREATE TABLE IF NOT EXISTS Personnel (
        libNumber    INTEGER,
        salary       REAL,
        ssn          INTEGER,
        PRIMARY KEY (libNumber),
        FOREIGN KEY (libNumber) REFERENCES Person
    );
    """

    personnel_records = """
    CREATE TABLE IF NOT EXISTS PersonnelRecords (
        logID         INTEGER,
        messageLog    VARCHAR(50),
        PRIMARY KEY (logID)
    );
    """

    event = """
    CREATE TABLE IF NOT EXISTS Event (
        eventID     INTEGER,
        datetime    DATE,
        PRIMARY KEY (eventID)
    );
    """

    audience = """
    CREATE TABLE IF NOT EXISTS Audience (
        audienceID            INTEGER,
        audienceName          CHAR(30),
        audienceDescription   VARCHAR(50),
        PRIMARY KEY (audienceID)
    );
    """

    socail_room = """
    CREATE TABLE IF NOT EXISTS SocialRoom (
        roomNumber      INTEGER,
        roomCapacity    INTEGER,
        PRIMARY KEY (roomNumber)
    );
    """

    item_records = """
    CREATE TABLE IF NOT EXISTS ItemRecords (
        itemID        INTEGER,
        penaltyFee    REAL,
        dueDate       DATE,
        available     BOOLEAN,
        PRIMARY KEY (itemID)
    );
    """

    # types of evets
    book_club = """
    CREATE TABLE IF NOT EXISTS BookClub (
        eventID     INTEGER,
        clubName    CHAR(30),
        PRIMARY KEY (eventID),
        POREIGN KEY (eventID) REFERENCES Event
    );
    """

    art_show = """
    CREATE TABLE IF NOT EXISTS ArtShow (
        eventID    INTEGER,
        name       CHAR(30),
        PRIMARY KEY (eventID),
        FOREIGN KEY (eventID) REFERENCES Event
    );
    """

    # types of items
    book = """
    CREATE TABLE IF NOT EXISTS Book (
        itemID       INTEGER,
        title        CHAR(30),
        author       CHAR(30),
        publisher    char(30),
        PRIMARY KEY (itemID),
        FOREIGN KEY (itemID) REFERENCES ItemRecords
    );
    """

    cd = """
    CREATE TABLE IF NOT EXISTS CD (
        itemID      INTEGER,
        title       CHAR(30),
        producer    CHAR(30),
        director    CHAR(30),
        PRIMARY KEY (itemID),
        FOREIGN KEY (itemID) REFERENCES ItemRecords
    );
    """

    magazine = """
    CREATE TABLE IF NOT EXISTS Magazine (
        itemID       INTEGER,
        name         CHAR(30),
        publisher    CHAR(30) ,
        PRIMARY KEY (itemID),
        FOREIGN KEY (itemID) REFERENCES ItemRecords
    );
    """

    # relations
    borrow = """
    CREATE TABLE IF NOT EXISTS Borrow (
        libNumber    INTEGER,
        itemID       INTEGER,
        PRIMARY KEY (libNumber, itemID),
        FOREIGN KEY (libNumber) REFERENCES Person,
        FOREIGN KEY (itemID) REFERENCES ItemRecords
    );
    """

    log = """
    CREATE TABLE IF NOT EXISTS Log (
        libNumber    INTEGER,
        logID        INTEGER,
        PRIMARY KEY (libNumber, logID),
        FOREIGN KEY (libNumber) REFERENCES Personnel,
        FOREIGN KEY (logID) REFERENCES PersonnelRecords
    );
    """

    organize = """
    CREATE TABLE IF NOT EXISTS Organize (
        eventID      INTEGER,
        libNumber    INTEGER,
        PRIMARY KEY (eventID, libNumber),
        FOREIGN KEY (libNumber) REFERENCES Person,
        FOREIGN KEY (eventID) REFERENCES Event
    );
    """

    recommend = """
    CREATE TABLE IF NOT EXISTS Recommend (
        audienceID    INTEGER,
        eventID       INTEGER,
        PRIMARY KEY (audienceID, eventID),
        FOREIGN KEY (audienceID) REFERENCES Audience,
        FOREIGN KEY (eventID) REFERENCES Event
    );
    """

    held = """
    CREATE TABLE IF NOT EXISTS Held (
        eventID       INTEGER,
        roomNumber    INTEGER,
        PRIMARY KEY (eventID, roomNumber),
        FOREIGN KEY (eventID) REFERENCES Event,
        FOREIGN KEY (roomNumber) REFERENCES SocialRoom
    );
    """

    attend = """
    CREATE TABLE IF NOT EXISTS Attend (
        libNumber    INTEGER,
        eventID      INTEGER,
        PRIMARY KEY (libNumber, eventID),
        FOREIGN KEY (libNumber) REFERENCES Person,
        FOREIGN KEY (eventID) REFERENCES Event
    );
    """

    part_of = """
    CREATE TABLE IF NOT EXISTS PartOF (
        libNumber     INTEGER,
        audienceID    INTEGER,
        PRIMARY KEY (libNumber, audienceID),
        FOREIGN KEY (libNumber) REFERENCES Person,
        FOREIGN KEY (audienceID) REFERENCES Audience
    );
    """
    # triggers

 
    # create a database connection
    conn = create_connection(database)
 
    # create tables and triggers
    if conn is not None:
        # tables
        create_table(conn, person)
        create_table(conn, personnel)
        create_table(conn, personnel_records)
        create_table(conn, event)
        create_table(conn, audience)
        create_table(conn, socail_room)
        create_table(conn, item_records)
        create_table(conn, book_club)
        create_table(conn, art_show)
        create_table(conn, book)
        create_table(conn, cd)
        create_table(conn, magazine)
        create_table(conn, borrow)
        create_table(conn, log)
        create_table(conn, organize)
        create_table(conn, recommend)
        create_table(conn, held)
        create_table(conn, attend)
        create_table(conn, part_of)

        # triggers
        
    else:
        print("Error! cannot create the database connection.")
 
 
if __name__ == '__main__':
    main()