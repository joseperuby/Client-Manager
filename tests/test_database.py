import copy
import unittest
import DB.database as db
import Scripts.helpers as helpers
import Scripts.config as config
import csv

class TestDatabase(unittest.TestCase):
    def setUp(self):
        db.Customers.list = [
            db.Customer('15J', 'Pepe', 'Ramirez'),
            db.Customer('48H', 'Leo', 'Larios'),
            db.Customer('42O', 'Javier', 'Molina')
        ]
    
    def test_search_customer(self):
        e_customer = db.Customers.search('15J')
        non_customer = db.Customers.search('99X')
        self.assertIsNotNone(e_customer)
        self.assertIsNone(non_customer)

    def test_add_customer(self):
        new_customer = db.Customers.add('39X', 'Hector', 'Costa')
        self.assertEqual(len(db.Customers.list), 4)
        self.assertEqual(new_customer.id,'39X')
        self.assertEqual(new_customer.name,'Hector')
        self.assertEqual(new_customer.lastname, 'Costa')

    def test_modify_customer(self):
        target_customer = copy.copy(db.Customers.search('48H'))
        modify_costumer = db.Customers.modify('48H', 'Leonardo', 'Larios')
        self.assertEqual(target_customer.name,'Leo')
        self.assertEqual(modify_costumer.name,'Leonardo')

    def test_delete_customer(self):
        customer_deleted = db.Customers.delete('48H')
        non_customer = db.Customers.search('48H')
        self.assertEqual(customer_deleted.id, '48H')
        self.assertIsNone(non_customer)

    def test_valid_id(self):
        self.assertTrue(helpers.valid_id('48R', db.Customers.list))
        self.assertFalse(helpers.valid_id('258788T', db.Customers.list))
        self.assertFalse(helpers.valid_id('F45', db.Customers.list))
        self.assertFalse(helpers.valid_id('48H', db.Customers.list))

    def test_csv(self):
        db.Customers.delete('48H')
        db.Customers.delete('15J')
        db.Customers.modify('42O', 'Jav', 'Molina')

        id, name, lastname = None, None, None
        with open(config.DATABASE_PATH, newline='\n') as file:
            reader = csv.reader(file, delimiter=';')
            id, name, lastname = next(reader)

        self.assertEqual(id, '42O')
        self.assertEqual(name, 'Jav')
        self.assertEqual(lastname, 'Molina')
