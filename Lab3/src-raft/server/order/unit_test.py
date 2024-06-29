import unittest
import grpc
from order_pb2 import BuyRequest
import order_pb2_grpc
from order_pb2_grpc import OrderStub
from order_service import OrderServicer
from concurrent import futures
import multiprocessing

class TestOrderServicer(unittest.TestCase):
    def setUp(self):
        self.channel = grpc.insecure_channel("localhost:56367")
        self.stub = OrderStub(self.channel)

    def test_buy_successfully(self):
        # Test buying an item with sufficient stock
        print('Order Service Testing case 1: Testing Successful buy query')
        response = self.stub.buyOrder(BuyRequest(ToyName="Tux", ToyQuantity=1))
        self.assertGreaterEqual(response.OrderNumber, 0)  # Successful purchase
        print(f'Response OrderNumber:{response.OrderNumber} and expected OrderNumber to be greater than 0 both match \n\n')

    def test_buy_insufficient_quantity(self):
        # Test buying an item with insufficient stock
        print('Order Service Testing case 2: Testing insufficient quantity buy query')
        response = self.stub.buyOrder(BuyRequest(ToyName="Elephant", ToyQuantity=100000000))
        self.assertEqual(response.OrderNumber, -1)  # Insufficient stock
        print(f'Response OrderNumber:{response.OrderNumber} and expected OrderNumber:', -1, 'both match \n\n')


    def test_buy_invalid_toyname(self):
        # Test buying a invalid item
        try:
            print('Order Service Testing case 3: Testing invalid item name buy query')
            response = self.stub.buyOrder(BuyRequest(ToyName="InValid", ToyQuantity=1))
            self.assertEqual(response.OrderNumber, -1)  # Invalid buy item
            print(f'Response OrderNumber:{response.OrderNumber} and expected OrderNumber:', -1, 'both match \n\n')
        except grpc.RpcError as e:
            self.assertEqual(e.details(), "Invalid argument provided")  # Item not found

if __name__ == "__main__":
    unittest.main()

