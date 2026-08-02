import sqlite3
import os
from menu_config import *
from flags import identify_flag


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
                    source TEXT DEFAULT "General",
                    FOREIGN KEY (word_id) 
                    REFERENCES words(word_id) ON DELETE CASCADE
                )
            """)

            if not isFIleExists:
                print("## Database initialized successfully! ##\n")

        except sqlite3.Error as e:
            print(f"ERROR::INIT: {e}")

def write_db(name, defintion, native, source = "General"):
    """ Insert Data """
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
                INSERT INTO definition (defi, native_word, word_id, source)
                VALUES (?, ?, ?, ?)
            """,(defintion, native, wordID, source))
            
        except sqlite3.Error as e:
            print(f"ERROR::WRITING: {e}")        

def show(flag = None):
    """ Show all rows """
    with get_connection() as conn:
        cursor = conn.cursor()
    
        try:
            flag = identify_flag(flag)
            
            # check for any flag is on
            from types import SimpleNamespace
            flags = SimpleNamespace()

            flags.isSource = True if flag in SOURCE_FLAGS else False
            flags.isHelp = True if flag in HELP_FLAGS else False


            cursor.execute(""" 
                SELECT 
                    d.id, 
                    w.name, 
                    d.defi, 
                    d.native_word,
                    COUNT(w.word_id) OVER(PARTITION BY w.word_id) AS total_definition, 
                    d.insert_date,
                    d.source
                FROM definition AS d
                INNER JOIN words AS w ON d.word_id = w.word_id
            """)
        
        except sqlite3.Error as e:
            print(f"ERROR::SHOW: {e}")

    return cursor, flags

def check_word(name):
    with get_connection() as conn:
        cursor = conn.cursor()

        try:
            cursor.execute(""" 
            SELECT 
                d.id, 
                w.name, 
                d.defi, 
                d.native_word,
                COUNT(w.word_id) OVER(PARTITION BY w.word_id) AS total_definition, 
                d.insert_date
                d.source
            FROM definition AS d
            INNER JOIN words as w ON d.word_id = w.word_id
            WHERE w.name = (?)
            """,(name,))

        except sqlite3.Error as e:
            print(f"ERROR::CHECKING: {e}")

    return cursor