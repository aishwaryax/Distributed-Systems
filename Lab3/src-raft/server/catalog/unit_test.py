import unittest
import grpc
import threading
from catalog_pb2 import QueryRequest, BuyRequest
import catalog_pb2
import catalog_pb2_grpc
from catalog_pb2_grpc import CatalogStub
from catalog_service import CatalogServicer
from concurrent import futures
import multiprocessing
import time

class TestCatalogServicer(unittest.TestCase):
    def setUp(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count())) #workers set to cpu count to make maximum utilization of cpu
        self.catalog_servicer = CatalogServicer()
        catalog_pb2_grpc.add_CatalogServicer_to_server(
            CatalogServicer(), self.server
        )
        self.server.add_insecure_port("[::]:56366")
        self.server.start()
        self.channel = grpc.insecure_channel("localhost:56366")
        self.stub = CatalogStub(self.channel)

    def test_query_successful(self):
        # Test query for an existing item
        print('Catalog Service Testing case 1: Testing successful Query')
        response = self.stub.Query(QueryRequest(ItemName="Elephant"))
        self.assertEqual(response.Name, "Elephant")
        print(f'Response toyname:{response.Name} and expected toy name: Elephant, both match \n\n')


    def test_query_invalidName(self):
        # Test query for an invalid item
        try:
            print('Catalog Service Testing case 2: Testing invalid toyname Query')
            response = self.stub.Query(QueryRequest(ItemName="InValid"))
        except grpc.RpcError as e:
            self.assertEqual(e.details(), "Invalid argument provided")  # Item not found
            print('Tested invalid toyname query, giving no response, working as expected \n\n')

    def test_buy_successful(self):
        # Test buying an item with sufficient stock
        print('Catalog Service Testing case 3: Testing successful Buy')
        response = self.stub.Buy(BuyRequest(ItemName="Elephant", Quantity=1))
        self.assertEqual(response.Response, 1)  # Successful purchase
        print(f'Response:{response.Response} and expected Response: 1, both match \n\n')

    def test_buy_insufficient_stock(self):
        # Test buying an item with insufficient stock
        print('Catalog Service Testing case 4: Testing insufficient stock Buy')
        response = self.stub.Buy(BuyRequest(ItemName="Elephant", Quantity=100000))
        self.assertEqual(response.Response, 0)  # Insufficient stock
        print(f'Response:{response.Response} and expected Response: 0, both match \n\n')

    def test_buy_invalid_toyName(self): 
        # Test buying a invalid item
        print('Catalog Service Testing case 5: Testing invalid toyName Buy')
        try:
            response = self.stub.Buy(BuyRequest(ItemName="InValid", Quantity=1))
            self.assertEqual(response.Response, -1)
            print(f'Response:{response.Response} and expected Response: -1, both match \n\n')
        except grpc.RpcError as e:
            self.assertEqual(e.details(), "Invalid argument provided")  # Item not found

    def test_product_restock(self): 
        # Test buying a invalid item
        print('Catalog Service Testing case 6: Testing product restock')
        try:
            buyResponse = self.stub.Buy(BuyRequest(ItemName="Leopard", Quantity=100))
            self.assertEqual(buyResponse.Response, 1)
            print(f'Response:{buyResponse.Response} and expected Response: 1, both match \n\n')
            queryResponse = self.stub.Query(QueryRequest(ItemName="Leopard"))
            self.assertEqual(queryResponse.Stock, 0)
            print('Now Sleep for 10 sec')
            time.sleep(10)
            print('Rechecking after sleep of 10 sec')
            queryResponse = self.stub.Query(QueryRequest(ItemName="Leopard"))
            self.assertEqual(queryResponse.Stock, 100)
            print(f'Response:{queryResponse.Stock} and expected stock after restock: 100, both match \n\n')
        except grpc.RpcError as e:
            self.assertEqual(e.details(), "Invalid argument provided")  # Item not found

    def tearDown(self):
        self.server.stop(None)

if __name__ == "__main__":
    unittest.main()
