from enum import Enum

class eLogLevel(Enum):
    DEBUG = 0 # Gives debug information not specifically usefull for the end-user but more of a way to test parts of a system. #000000
    INFO  = 1 # Highlights information usefull for the end-user and shows progress info.
    WARN  = 2 # Potentially harmful situations.
    ERROR = 3 # Error events that should be paid attention to but would still allow the application to continue running. 
    FATAL = 4 # Very servere error events that will most likely abort the application or 

enabled = True

def log_global_on():
    if enabled == False:
        enabled = True 
        print("Enabled logging on!")
    elif enabled == True:
        print("Logging is already enabled!")

