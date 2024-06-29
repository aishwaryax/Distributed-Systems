from collections import defaultdict
from concurrent import futures
import grpc
import catalog_pb2
import catalog_pb2_grpc
import logging
import threading
import multiprocessing
import random
import os
import pandas as pd
from toy import Toy
from config import CATALOG_PORT, CATALOG_SERVER, MAX_WORKER
from readerwriterlock import rwlock

class CatalogServicer(catalog_pb2_grpc.CatalogServicer):
    def __init__(self):
        self.db = None
        lock_gen = rwlock.RWLockFairD()
        self.read_lock = lock_gen.gen_rlock()
        self.write_lock = lock_gen.gen_wlock()
        if os.path.isfile("./catalog.csv"):
            self.db = pd.read_csv("./catalog.csv")
        else:
            toys_data = [
                ["Elephant", random.randint(1000, 10000), random.randint(1000, 10000)],
                ["Whale", random.randint(1000, 10000), random.randint(1000, 10000)],
                ["Dolphin", random.randint(1000, 10000), random.randint(1000, 10000)],
                ["Tux", random.randint(1000, 10000), random.randint(1000, 10000)],
                ["Fox", random.randint(1000, 10000), random.randint(1000, 10000)],
                ["Python", random.randint(1000, 10000), random.randint(1000, 10000)],
            ]
            self.db = pd.DataFrame(toys_data, columns=["Name", "Stock", "Cost"])
            self.write()  # Write DataFrame to CSV
        self.lock = threading.Lock() #change this to rw lock #3rd solution to reader writers if time permits

    def write(self):
        if not os.path.isfile("./catalog.csv"):
            self.db.to_csv("./catalog.csv", index_label="ID")
        else:
            # Write DataFrame to CSV without index
            self.db.to_csv("./catalog.csv", index=False)
    """
        Queries the toy store for information about a specific toy.

        Args:
            request (catalog_pb2.QueryRequest): gRPC request containing the item name.
            context (grpc.ServicerContext): context of the gRPC call.

        Returns:
            catalog_pb2.QueryResponse: gRPC response containing the cost and stock information.

        Raises:
            grpc.RpcError: If an invalid argument is provided or the item is not found.
    """
    def Query(self, request, context):
        if not request or not request.ItemName:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT) #if query invalid, return empty response with invalid argument in context
            context.set_details("Null argument provided")
            return catalog_pb2.QueryResponse()
        with self.read_lock:
            filtered_indices = self.db.index[self.db['Name'] == request.ItemName]
            if len(filtered_indices) <= 0:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT) #if query invalid, return empty response with invalid argument in context
                context.set_details("Invalid argument provided")
                return catalog_pb2.QueryResponse()
            query_result = self.db.loc[filtered_indices[0]]
            return catalog_pb2.QueryResponse(Name=query_result['Name'], Cost=query_result['Cost'], Stock=query_result['Stock'])


    """
    Buys an item from the toy store and updates the stock.

    Args:
        request (catalog_pb2.BuyRequest): gRPC request containing the item name.
        context (grpc.ServicerContext): context of the gRPC call.

    Returns:
        catalog_pb2.BuyResponse: gRPC response indicating the purchase result.
            - Response:  1 if the purchase is successful,
                         0 if the item is out of stock,
                        -1 if an invalid argument is provided or the item is not found.
    """
    def Buy(self, request, context):
        if not request or not request.ItemName:
            return catalog_pb2.BuyResponse(Response=-1)
        with self.write_lock:
            filtered_indices = self.db.index[self.db['Name'] == request.ItemName]
            if len(filtered_indices) == 0:
                return catalog_pb2.BuyResponse(Response=-1)
            if self.db.loc[filtered_indices[0]]['Stock'] < request.Quantity:
                return catalog_pb2.BuyResponse(Response=0)
            self.db.loc[filtered_indices[0], 'Stock'] -= request.Quantity
            self.write()
            return catalog_pb2.BuyResponse(Response=1)
    

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=MAX_WORKER)) #workers set to cpu count to make maximum utilization of cpu
    catalog_pb2_grpc.add_CatalogServicer_to_server(
        CatalogServicer(), server
    )
    server_host = os.getenv("CATALOG_SERVER", CATALOG_SERVER)
    server.add_insecure_port(server_host + ':' + str(CATALOG_PORT))
    server.start()
    print("The Catalog server is running.")
    try:
        server.wait_for_termination()   
    except KeyboardInterrupt:
        print("Server shutting down")

if __name__ == "__main__":
    logging.basicConfig()
    serve()
