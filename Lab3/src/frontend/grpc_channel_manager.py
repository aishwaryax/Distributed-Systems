import grpc
import os
from config import CATALOG_PORT, ORDER_PORT, CATALOG_SERVER, ORDER_SERVER

class OrderManager:
    _instance = None

    def __init__(self, port):
        self.port = port
        order_service = os.getenv("ORDER_SERVER", ORDER_SERVER)
        # Create a gRPC channel for communication with the order service
        self._instance.channel = grpc.insecure_channel(order_service + ':' + str(self._instance.port))

    def __new__(self, *args, **kwargs):
        # Create a new instance if it doesn't exist
        if self._instance is None:
            self._instance = super().__new__(self)
        return self._instance

    @classmethod
    def get_channel(self, port):
        # Get the channel for the order service
        if self._instance is None:
            self._instance = self(port)
        return self._instance.channel

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
