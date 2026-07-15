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
            CREATE TABLE IF NOT EXISTS words (
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
        while(True):
            cursor.execute(""" 
                SELECT * FROM words
                WHERE name = ?
            """, (name,))
        
            row = cursor.fetchone()

            if row:
                #
                wordID = row[0]
                print(wordID)
                break

            else:
                cursor.execute(""" 
                    INSERT INTO words (name)
                    VALUES (?)
                """,(name, ))

        cursor.execute(""" 
            INSERT INTO definition (defi, native_word, word_id)
            VALUES (?, ?, ?)
        """,(defintion, native, wordID))

        
    except sqlite3.Error as e:
        print(f"ERROR::WRITING: {e}")

    finally: 
        conn.commit()


def show():
    if not DB_FILE:
        print("ERROR::SHOWING: file not exists!")
        return

    with get_connection() as conn:
        cursor = conn.cursor()
    
    try:
        cursor.execute(""" 
            SELECT d.id, w.name, d.defi, d.native_word, d.insert_date
            FROM definition AS d
            INNER JOIN words as w 
            ON d.id = w.word_id
        """)

        rows = cursor.fetchall()
        
        headers = [description[0] for description in cursor.description]

        print("=" * 15 * len(headers))
        # 3. Print headers and rows using a fixed width (e.g., 15 characters)
        print(" | ".join(f"{col:<15}" for col in headers))
        print("-" * 15 * len(headers))
        for row in rows:
            print(" | ".join(f"{str(item):<15}" for item in row))

        print("=" * 15 * len(headers))
    
    except sqlite3.Error as e:
        print(f"ERROR::SHOW: {e}")

    finally:
        conn.commit()
    
    # We will check first if data already exists
    # if yes then we will increase the Frequency for the word by 1
    # Also 

if __name__ == "__main__":
    init_db()
    user_input = ""
    while True:
        user_input = input(""" 
=====================
1- insert word
2- show
3- stop
=====================
:""")    

        if user_input == '1':
            word = input("enter name: ")
            definition = input("enter definition: ")
            native_word = input("enter the native word: ")

            write_db(word, definition, native_word)
        
        elif user_input == '2':
            show()

        elif user_input == '3':
            break

        else:
            break
