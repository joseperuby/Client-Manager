import os
import Scripts.helpers as helpers
import DB.database as db

def start():
    while True:
        helpers.clean_terminal()

        print("###############################")
        print("# Welcome to Customer Manager #")
        print("###############################")
        print("#    [1] List customer        #")
        print("#    [2] Search customer      #")
        print("#    [3] Add customer         #")
        print("#    [4] Modify customer      #")
        print("#    [5] Remove customer      #")
        print("#    [6] Close manager        #")
        print("###############################")

        option = input(" > ")
        helpers.clean_terminal()

        if option == "1":
            print("Listing customer(s)... \n")
            for customer in db.Customers.list:
                print(customer)

        elif option == "2":
            print("Searching customer(s)... \n")
            id = helpers.read_text(3,3,"ID (2 int and 1 char)").upper()
            customer = db.Customers.search(id)
            if customer:
                print(customer)
            else:
                print("No customer")

        elif option == "3":
            print("Adding customer(s)... \n")
            id = None
            while True:
                id = helpers.read_text(3,3,"ID (2 int and 1 char)").upper()
                if helpers.valid_id(id, db.Customers.list):
                    break

            name = helpers.read_text(2,30,"Name (2-30 chars)").capitalize()
            lastname = helpers.read_text(2,30,"Name (2-30 chars)").capitalize()
            db.Customers.add(id, name, lastname)
            print("Customer added")

        elif option == "4":
            print("Modifying customer... \n")
            id = helpers.read_text(3,3,"ID (2 int and 1 char)").upper()
            customer = db.Customers.search(id)
            if customer:
                name = helpers.read_text(2,30,f"Name (2-30 chars) [{customer.name}]").capitalize()
                lastname = helpers.read_text(2,30,f"Lastame (2-30 chars) [{customer.lastname}]").capitalize()
                db.Customers.modify(customer.id, name, lastname)
                print("Customer modified")
            else:
                print("No customer")
                

        elif option == "5":
            print("Removing customer... \n")
            id = helpers.read_text(3,3,"ID (2 int and 1 char)").upper()
            print("Customer removed") if db.Customers.delete(id) else print("No customer")

        elif option == "6":
            print("Closing... \n")
            break

        input("\nPress ENTER to continue...")