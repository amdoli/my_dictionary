import sqlite3
import os

DB_FILE = "saveFile.db"

def get_connection():
    """ Create and return a database connection. """
    return sqlite3.connect(DB_FILE)

def init_db():
    """ Initialise the table and ensures if exists """
    isFIleExists = os.path.exists(DB_FILE)
    with get_connection() as conn:
        cursor = conn.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dictionary (
                word_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                insert_date DATE DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS definition (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                defi TEXT NOT NULL,
                native_word TEXT,
                insert_date DATE DEFAULT CURRENT_TIMESTAMP,
                word_id INTEGER,
                FOREIGN KEY (word_id) REFERENCES dictionary(id)
            )
        """)

    except sqlite3.Error as e:
        print(f"ERROR::INIT: {e}")

    finally:
        conn.commit()
        if not isFIleExists:
            print("## Database initialized successfully! ##\n")

def write_db(name, defintion, native):
    """ Insert Data """
        
    if not DB_FILE:
        print("ERROR::WRITING: file not exists!")
        return

    with get_connection() as conn:
        cursor = conn.cursor()
    
    try:
        # First, check if the word already exists
        cursor.execute(""" 
            SELECT * FROM dictionary
            WHERE name = ?
        """, (name,))
        
        if row:
            #
            wordID = row[0]
            print(wordID)

        else:
            cursor.execute(""" 
                INSERT INTO dictionary (name)
                VALUES (?)
            """,(name, ))
        
        row = cursor.fetchone()

        if row:
            wordID = row[0]
            print(wordID)

    except sqlite3.Error as e:
        print(f"ERROR::WRITING: {e}")

    finally: 
        conn.commit()




    
    # We will check first if data already exists
    # if yes then we will increase the Frequency for the word by 1
    # Also 

if __name__ == "__main__":
    init_db()
    user_input = ""
    while True:
        user_input = input("enter: ")
        write_db(user_input, "", "")
