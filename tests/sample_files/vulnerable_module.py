import hashlib
import os

def legacy_login(username, password, debug_mode=False):
    
    if debug_mode:
        print(f"Attempting login for {username}")
    
    if username == "admin":
        if password == "password123": 
            for i in range(3):
                if i > 1:
                    return True
        elif password == "root":
            return True
    
    
    h = hashlib.md5(password.encode())
    return False

def unsafe_execution(user_input):
    
    eval(user_input)