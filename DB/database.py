import csv
import Scripts.config as config

class Customer:
    def __init__(self, id, name, lastname):
        self.id = id
        self.name = name
        self.lastname = lastname

    def __str__(self):
        return f"({self.id}) {self.name} {self.lastname}"
    
class Customers:
    list = []
    with open(config.DATABASE_PATH, newline='\n') as file:
        reader = csv.reader(file, delimiter=';')
        for id, name, lastname in reader:
            customer = Customer(id, name, lastname)
            list.append(customer)

    @staticmethod
    def search(id):
        for customer in Customers.list:
            if customer.id == id:
                return customer

    @staticmethod      
    def add(id, name, lastname):
        customer = Customer(id, name, lastname)
        Customers.list.append(customer)
        Customers.save()
        return customer
    
    @staticmethod
    def modify(id, name, lastname):
        for index, customer in enumerate(Customers.list):
            if customer.id == id:
                Customers.list[index].name = name
                Customers.list[index].lastname = lastname
                Customers.save()
                return Customers.list[index]
            
    @staticmethod
    def delete(id):
        for index, customer in enumerate(Customers.list):
            if customer.id == id:
                customer_d = Customers.list.pop(index)
                Customers.save()
                return customer_d
            
    @staticmethod
    def save():
        with open(config.DATABASE_PATH, 'w', newline='\n') as file:
            writer = csv.writer(file, delimiter=';')
            for customer in Customers.list:
                writer.writerow((customer.id, customer.name, customer.lastname))