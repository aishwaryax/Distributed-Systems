from grpc_channel_manager import OrderManager, CatalogManager
import order_pb2
import order_pb2_grpc
import catalog_pb2
import catalog_pb2_grpc
import grpc

class ProductBL:
    _instance = None
    
    def __new__(self):
        # Create a singleton instance for ProductBL
        if self._instance is None:
            self._instance = super().__new__(self)
            # Get gRPC channels for order and catalog services
            self._instance.order_channel = OrderManager.get_channel()
            self._instance.catalog_channel = CatalogManager.get_channel()
        return self._instance
    
    def order(self, name, qty):
        try:
            # Create gRPC stub for the order service
            stub = order_pb2_grpc.OrderStub(self._instance.order_channel)
            # Make an order request and receive response
            response = stub.buyOrder(order_pb2.BuyRequest(ToyName=name, ToyQuantity=qty))
            return response
        except grpc.RpcError as e:
            # Handle gRPC errors
            print(e.details())  # Print error details
            return order_pb2.BuyResponse(OrderNumber=-1, Message="Could not place an order")

    def get_catalog(self, name):
        try:
            # Create gRPC stub for the catalog service
            stub = catalog_pb2_grpc.CatalogStub(self._instance.catalog_channel)
            # Query the catalog for the specified item
            response = stub.Query(catalog_pb2.QueryRequest(ItemName=name))
            return response
        except grpc.RpcError as e:
            # Handle gRPC errors
            print(e.details())  # Print error details
            return catalog_pb2.QueryResponse(Name="")
