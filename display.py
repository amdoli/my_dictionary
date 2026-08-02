import textwrap
from database import *
from menu_config import *
from flags import *

def print_table(cursor, isSource = False):

    rows = cursor.fetchall()

    if not rows:
        print("\nNo words found in the database yet!")
        return

    #headers = [description[0] for description in cursor.description]
    
    # --- PRINT THE HEADERS ---
    print("=" * (ID_W + NAME_W + DEF_W + NATIVE_W + TIME_W + 12))
    print(f"{'ID':<{ID_W}} | {'NAME':<{NAME_W}} | {'DEFINITION':<{DEF_W}} | {'FREQ':<{FREQ_W}} | {'INSERT DATE':<{TIME_W}} | {'NATIVE WORD':<{NATIVE_W}}", end="")

    # if the user add Source flag
    print(f" | {'SOURCE':<{SRC_W}}") if isSource else print() # next line

    # --- PRINT THE CONTENT ---
    for row in rows:
        counter = -1
        definition = str(row[2])
        # limit the definition size into width of DEF_W
        def_lines = textwrap.wrap(definition, width=DEF_W)

        print(f"{str(row[0]):<{ID_W}} | ", end="")
        print(f"{str(row[1]):<{NAME_W}} | ", end="")
        print(f"{def_lines[0]:<{DEF_W}} | ", end="")
        print(f"{str(row[4]):<{FREQ_W}} | ",  end="")
        print(f"{str(row[5]):<{TIME_W}} | ", end="")
        print(f"{str(row[3]):<{NATIVE_W}}", end="")
        # if user add Source flag
        print(f" | {str(row[6]):<{SRC_W}}") if isSource else print()

        # if definition size exceeded 35
        if len(def_lines) > 1:
            for extra_line in def_lines[1:]:
                print(f"{' ':<{ID_W}} | ", end="")
                print(f"{' ':<{NAME_W}} | ", end="")
                print(f"{extra_line:<{DEF_W}} | ", end="")
                print(f"{' ':<{FREQ_W}} | ", end="")
                print(f"{' ':<{TIME_W}} | ", end="")
                print(f"{' ':<{NATIVE_W}}", end="")
                # if Source flag applied
                print(f" | {' ':<{SRC_W}}") if isSource else print()

    src_w = SRC_W if isSource else 0
    print("-" * (ID_W + NAME_W + DEF_W + NATIVE_W + TIME_W + src_w + 12))




def main_menu():
    app_should_close = False

    init_db()

    user_input = ""
    print("\033[2J\033[H", end="")

    while not app_should_close:
        user_input = input(""" 
=====================
1- insert word
2- show
3- check word
4- stop
=====================
:""")    
        
        parts = user_input.split()
        if not parts:
            continue
        command = parts[0] # 'show'
        flag = parts[1] if len(parts) > 1 else None 
        
        print("\033[2J\033[H", end="")

        # /-- INSERT --/
        if command.lower() in INSERT_NAME:

            word = input("enter name: ")
            definition = input("enter definition: ")
            native_word = input("enter the native word: ")

            check_flag(command.lower(), WRITE_OPTIONS, flag)             

            # we will process every flag if enabled
            source = identify_flag(flag)
            if source:
                source = input("Enter from where you got this word: ")
                                
            write_db(word, definition, native_word, source)

        # /-- SHOW --/
        elif command.lower() in SHOW_NAME:

            check_flag(command.lower(), SHOW_OPTIONS, flag)
                    
            cursor, flags = show(flag) # TEMPORARLY need to change its 
            print_table(cursor, flags.isSource)

        # /-- CHECK --/
        elif command.lower() in CHECK_NAME:
            user_input = input("Enter the name:")
            check_word(user_input)

        # /-- STOP --/
        elif command.lower() in STOP_NAME:
            app_should_close = True

        else:
            print(f"\nUnidentified answer. Please try again.\n")