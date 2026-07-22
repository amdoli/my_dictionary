import sqlite3
import os
import textwrap

DB_FILE = "saveFile.db"

def get_connection():
    """ Create and return a database connection. """
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

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
                    FOREIGN KEY (word_id) 
                    REFERENCES words(word_id) ON DELETE CASCADE
                )
            """)

            if not isFIleExists:
                print("## Database initialized successfully! ##\n")

        except sqlite3.Error as e:
            print(f"ERROR::INIT: {e}")

def write_db(name, defintion, native):
    """ Insert Data """
        
    if not os.path.exists(DB_FILE):
        print("ERROR::WRITING: file not exists!")
        return

    with get_connection() as conn:
        cursor = conn.cursor()
    
        try:
            # First, check if the word already exists
            cursor.execute("SELECT word_id FROM words WHERE name = ?", (name,))
            row = cursor.fetchone()

            if row:
                wordID = row[0]
            # If not then insert a new word ang grub the ID
            else:
                cursor.execute("INSERT INTO words (name) VALUES (?)",(name,))
                wordID = cursor.lastrowid
            # Finally, Insert in definition
            cursor.execute(""" 
                INSERT INTO definition (defi, native_word, word_id)
                VALUES (?, ?, ?)
            """,(defintion, native, wordID))

            
        except sqlite3.Error as e:
            print(f"ERROR::WRITING: {e}")

def print_table(cursor):

    ID_W = 5
    NAME_W = 15
    DEF_W = 35
    NATIVE_W = 15
    TIME_W = 20

    rows = cursor.fetchall()

    if not rows:
        print("\nNo words found in the database yet!")
        return

    headers = [description[0] for description in cursor.description]
    
    # --- PRINT THE HEADERS ---
    print("=" * (ID_W + NAME_W + DEF_W + NATIVE_W + TIME_W + 12))
    print(f"{'ID':<{ID_W}} | {'NAME':<{NAME_W}} | {'DEFINITION':<{DEF_W}} | {'INSERT DATE':<{TIME_W}} | {'NATIVE WORD':<{NATIVE_W}}")

    # --- PRINT THE CONTENT ---
    for row in rows:
        counter = -1
        definition = str(row[2])
        # limit the definition size into width of DEF_W
        def_lines = textwrap.wrap(definition, width=DEF_W)

        print(f"{str(row[0]):<{ID_W}} | ", end="")
        print(f"{str(row[1]):<{NAME_W}} | ", end="")
        print(f"{def_lines[0]:<{DEF_W}} | ", end="")
        print(f"{str(row[4]):<{TIME_W}} | ", end="")
        print(f"{str(row[3]):<{NATIVE_W}}")

        if len(def_lines) > 1:
            for extra_line in def_lines[1:]:
                print(f"{' ':<{ID_W}} | ", end="")
                print(f"{' ':<{NAME_W}} | ", end="")
                print(f"{extra_line:<{DEF_W}} | ", end="")
                print(f"{' ':<{TIME_W}} | ", end="")
                print(f"{' ':<{NATIVE_W}}")
    
    print("-" * (ID_W + NAME_W + DEF_W + NATIVE_W + TIME_W + 12))
        

def show():
    if not os.path.exists(DB_FILE):
        print("ERROR::SHOWING: file not exists!")
        return

    with get_connection() as conn:
        cursor = conn.cursor()
    
        try:
            cursor.execute(""" 
                SELECT d.id, w.name, d.defi, d.native_word, d.insert_date
                FROM definition AS d
                INNER JOIN words as w 
                ON d.word_id = w.word_id
            """)

            print_table(cursor)
        
        except sqlite3.Error as e:
            print(f"ERROR::SHOW: {e}")

def check_word(name):
    if not os.path.exists(DB_FILE):
        print("ERROR::CHECKING: file not exists!")
        return

    with get_connection() as conn:
        cursor = conn.cursor()

        try:
            cursor.execute(""" 
            SELECT d.id, w.name, d.defi, d.native_word, d.insert_date
                FROM definition AS d
                INNER JOIN words as w 
                ON d.word_id = w.word_id
                WHERE w.name = (?)
            """,(name,))

            print_table(cursor)


        except sqlite3.Error as e:
            print(f"ERROR::CHECKING: {e}")


if __name__ == "__main__":
    init_db()
    user_input = ""
    while True:
        user_input = input(""" 
=====================
1- insert word
2- show
3- check word
4- stop
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
            user_input = input("Enter the name:")
            check_word(user_input)

        elif user_input == '4':
            break
