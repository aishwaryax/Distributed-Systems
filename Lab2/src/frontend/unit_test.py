import sys
import json
import unittest
from config import HTTP_PORT, HTTP_SERVER, GET_PRODUCT, PLACE_ORDER
import requests


"""Test case for the client methods."""
class TestFunctions(unittest.TestCase):
    def setUp(self):
        self.queryUrl = "http://"+HTTP_SERVER+":"+str(HTTP_PORT)+GET_PRODUCT
        self.orderUrl = "http://"+HTTP_SERVER+":"+str(HTTP_PORT)+PLACE_ORDER
        
        
    def test_successful_query(self):
        print('Frontend Service Testing case 1: Testing valid toyname query in ')
        response = requests.get(self.queryUrl+'Tux')

        # Assert response status
        self.assertEqual(response.status_code, 200)

        # Assert response keys
        expected_keys = {'name', 'price', 'quantity'}
        response_keys = response.json()["data"].keys()        
        self.assertEqual(response_keys, expected_keys)

        print('Tested valid toyname query \n\n')

    def test_invalid_toyname_query(self):
        print('Frontend Service Testing case 2:Testing invalid toyname query ')
        response = requests.get(self.queryUrl+'tuxA')
        expected = {
            "error": {
                "code": 404,
                "message": "product not found"
            }
        }
        data = response.json()
        # Assert response status
        self.assertEqual(response.status_code, 200)
        # Assert response
        self.assertEqual(data, expected)
        print('Tested invalid toyname query \n\n')

    def test_successful_buy(self):
        print('Frontend Service Testing case 3: Testing successful toyname buy ')
        body = {
            "name": "Tux",
            "quantity": 1
        }
        response = requests.post(self.orderUrl, json=body)
        
        # Assert response status
        self.assertEqual(response.status_code, 200)

        # Assert response
        expected_keys = {'order_number'}
        response_keys = response.json()["data"].keys()  
        self.assertEqual(response_keys, expected_keys)

        print('Tested successful buy \n\n')
    
    def test_insufficient_quantity_buy(self):
        print('Frontend Service Testing case 4: Testing insufficient quantity buy ')
        body = {
            "name": "Tux",
            "quantity": 1000000
        }
        response = requests.post(self.orderUrl, json=body)
        
        expected_response = {
            "error": {
                "code": 304,
                "message": "could not post order"
            }
        }
        # Assert response status
        self.assertEqual(response.status_code, 200)

        # Assert response
        self.assertEqual(response.json(), expected_response)

        print('Tested insufficient quantity buy \n\n')

    def test_invalid_toyname_buy(self):
        print('Frontend Service Testing case 5: Testing invalid toyname buy ')
        body = {
            "name": "ABC",
            "quantity": 1
        }
        response = requests.post(self.orderUrl, json=body)
        
        expected_response = {
            "error": {
                "code": 304,
                "message": "could not post order"
            }
        }
        # Assert response status
        self.assertEqual(response.status_code, 200)

        # Assert response
        self.assertEqual(response.json(), expected_response)

        print('Tested invalid toyname buy \n\n')

if __name__ == '__main__':
      unittest.main()