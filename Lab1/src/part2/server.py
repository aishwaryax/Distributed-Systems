from toy import Toy
from collections import defaultdict
from concurrent import futures
import grpc
import toy_store_pb2
import toy_store_pb2_grpc
import logging
import threading
import multiprocessing
import random
from config import PORT

class ToyStoreServicer(toy_store_pb2_grpc.ToyStoreServicer):
    def __init__(self):
        self.db = defaultdict(Toy) #toy store database
        for toy in [Toy(name="Elephant", stock=random.randint(100, 1000), price=random.randint(1000, 10000)),
                    Toy(name="Whale", stock=random.randint(100, 1000), price=random.randint(1000, 10000)),
                    Toy(name="Dolphin", stock=random.randint(100, 1000), price=random.randint(1000, 10000)),
                    Toy(name="Tux", stock=random.randint(100, 1000), price=random.randint(1000, 10000))]:
            self.db[toy.name.lower()] = toy
        self.lock = threading.Lock() #lock for read and write operation


    """
        Queries the toy store for information about a specific toy.

        Args:
            request (toy_store_pb2.QueryRequest): gRPC request containing the item name.
            context (grpc.ServicerContext): context of the gRPC call.

        Returns:
            toy_store_pb2.QueryResponse: gRPC response containing the cost and stock information.

        Raises:
            grpc.RpcError: If an invalid argument is provided or the item is not found.
    """
    def Query(self, request, context):
        if not request or not request.ItemName:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT) #if query invalid, return empty response with invalid argument in context
            context.set_details("Invalid argument provided")
            return toy_store_pb2.QueryResponse()
        query =  request.ItemName.lower()
        with self.lock:
            if query not in self.db:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT) #if query invalid, return empty response with invalid argument in context
                context.set_details("Invalid argument provided")
                return toy_store_pb2.QueryResponse()
            return toy_store_pb2.QueryResponse(Cost=self.db[query].price, Stock=self.db[query].stock)


    """
    Buys an item from the toy store and updates the stock.

    Args:
        request (toy_store_pb2.BuyRequest): gRPC request containing the item name.
        context (grpc.ServicerContext): context of the gRPC call.

    Returns:
        toy_store_pb2.BuyResponse: gRPC response indicating the purchase result.
            - Response:  1 if the purchase is successful,
                            0 if the item is out of stock,
                        -1 if an invalid argument is provided or the item is not found.
    """
    def Buy(self, request, context):
        if not request or not request.ItemName:
            return toy_store_pb2.BuyResponse(Response=-1)
        query =  request.ItemName.lower()
        with self.lock:
            if query not in self.db:
                return toy_store_pb2.BuyResponse(Response=-1)
            if self.db[query].stock == 0:
                return toy_store_pb2.BuyResponse(Response=0)
            self.db[query].stock -= 1 #decrement stock count
            return toy_store_pb2.BuyResponse(Response=1)
    

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count())) #workers set to cpu count to make maximum utilization of cpu
    toy_store_pb2_grpc.add_ToyStoreServicer_to_server(
        ToyStoreServicer(), server
    )
    server.add_insecure_port("[::]:" + str(PORT))
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig()
    serve()
