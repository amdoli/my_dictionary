from menu_config import *

def identify_command(command):

    if command in INSERT_NAME:
        return "insert"

    elif command in SHOW_NAME:
        return "show"

    elif command in CHECK_NAME:
        return "check"

    elif command in STOP_NAME:
        return "stop"

    else: 
        return None     


def identify_flag(flag):
    if flag in SOURCE_FLAGS:
        return SOURCE_FLAGS[0]
    
    elif flag in HELP_FLAGS:
        return HELP_FLAGS[0]

    else:
        return  


def check_flag(command, command_options, flag = None):

    command = identify_command(command)
    flag = identify_flag(flag)

    if not flag:
        return
        
    # I want to let the printed command to be clear 
    isFlag = any(flag in option_list for option_list in command_options)
    if not isFlag and flag != "General": # other condition are TEMPORARLY
        print(f"there are no {command} {flag}.")
        print(f"You can write {command} -help to see all the fetures.")

        return 
    

def help(command_option = None):
    """ Under Maintaining """
    print("### IN DEVOLOPMENT ### ")

