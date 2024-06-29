from grpc_channel_manager import OrderManager, CatalogManager
import order_pb2
import order_pb2_grpc
import catalog_pb2
import catalog_pb2_grpc
import grpc
from LRUCache import LRUCache
from config import CACHE_CAPACITY

class ProductBL:
    _instance = None
    
    def __new__(self, *args, **kwargs):
        # Create a singleton instance for ProductBL
        if self._instance is None:
            self._instance = super().__new__(self)
        return self._instance
    
    def __init__(self, port):
        self.port = port
        order_manager = OrderManager(port)
        self.order_channel = order_manager.get_channel(port)
        self.catalog_channel = CatalogManager.get_channel()
        self.cache = LRUCache(CACHE_CAPACITY)
    
    def order(self, name, qty):
        # self._instance.cache.print_all_values()
        try:
            # Create gRPC stub for the order service
            stub = order_pb2_grpc.OrderStub(self._instance.order_channel)
            # Make an order request and receive response
            response = stub.buyOrder(order_pb2.BuyRequest(ToyName=name, ToyQuantity=qty))
            return response
        except grpc.RpcError as e:
            # Handle gRPC errors
            print(e.details())  # Print error details
            return order_pb2.BuyResponse(OrderNumber=-2, Message="Could not place an order")

    def get_catalog(self, name):
        # self._instance.cache.print_all_values()
        cache_val = self._instance.cache.get(name)
        if cache_val:
            return cache_val
        try:
            # Create gRPC stub for the catalog service
            stub = catalog_pb2_grpc.CatalogStub(self._instance.catalog_channel)
            # Query the catalog for the specified item
            response = stub.Query(catalog_pb2.QueryRequest(ItemName=name))
            self._instance.cache.put(name, response)
            return response
        except grpc.RpcError as e:
            # Handle gRPC errors
            print(e.details())  # Print error details
            return catalog_pb2.QueryResponse(Name="")
        
    def get_order(self, order_no):
        try:
            # Create gRPC stub for the order service
            stub = order_pb2_grpc.OrderStub(self._instance.order_channel)
            # Make an get order request and receive response
            response = stub.GetOrder(order_pb2.GetRequest(OrderNumber=order_no))
            return response
        except grpc.RpcError as e:
            # Handle gRPC errors
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                # Print error details
                print(e.details())
                return order_pb2.GetResponse(OrderNumber=-1)
            else:
                return order_pb2.GetResponse(OrderNumber=-2)
        
    def clear_cache(self, names):
        for name in names:
            self._instance.cache.clear(name)

