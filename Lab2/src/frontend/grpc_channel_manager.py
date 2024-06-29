import grpc
import os
from config import CATALOG_PORT, ORDER_PORT, CATALOG_SERVER, ORDER_SERVER

class OrderManager:
    instance = None

    def __new__(self):
        # Create a new instance if it doesn't exist
        if self.instance is None:
            self.instance = super().__new__(self)
            order_service = os.getenv("ORDER_SERVER", ORDER_SERVER)
            # Create a gRPC channel for communication with the order service
            self.instance.channel = grpc.insecure_channel(order_service + ':' + str(ORDER_PORT))
        return self.instance

    @classmethod
    def get_channel(self):
        # Get the channel for the order service
        if self.instance is None:
            self.instance = self()
        return self.instance.channel
    

class CatalogManager:
    instance = None

    def __new__(self):
        # Create a new instance if it doesn't exist
        if self.instance is None:
            self.instance = super().__new__(self)
            catalog_service = os.getenv("CATALOG_SERVER", CATALOG_SERVER)
            # Create a gRPC channel for communication with the catalog service
            self.instance.channel = grpc.insecure_channel(catalog_service + ':' + str(CATALOG_PORT))
        return self.instance

    @classmethod
    def get_channel(self):
        # Get the channel for the catalog service
        if self.instance is None:
            self.instance = self()
        return self.instance.channel
