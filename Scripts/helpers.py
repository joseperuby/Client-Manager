import os
import re
import platform

def clean_terminal():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def read_text(min_len=0, max_len=100, message=None):
    if message:
        print(message)
    else:
        None
    while True:
        text = input(" > ")
        if len(text) >= min_len and len(text) <= max_len:
            return text
        print(f"Error! The permitted length is {min_len}.")
        
def valid_id(id, list):
    if not re.match('[0-9]{2}[A-Z]$', id):
        print("Incorrect ID, please use the correct format")
        return False
    for customer in list:
        if customer.id == id:
            print("ID used, please try another one")
            return False
    return True