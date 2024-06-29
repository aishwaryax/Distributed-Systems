from concurrent import futures
import grpc
import catalog_pb2
import catalog_pb2_grpc
import logging
import threading
import random
import os
import pandas as pd
from toy import Toy
from config import CATALOG_PORT, CATALOG_SERVER, MAX_WORKER, HTTP_SERVER, HTTP_PORT, INVALIDATE_ENDPOINT
import time
import requests
import json

class CatalogServicer(catalog_pb2_grpc.CatalogServicer):
    def __init__(self):
        self.db = None
        self.condition = threading.Condition()
        # lock_gen = rwlock.RWLockFairD()
        # self.read_lock = lock_gen.gen_rlock()
        # self.write_lock = lock_gen.gen_wlock()
        if os.path.isfile("./catalog.csv"):
            self.condition.acquire()
            try:
                self.db = pd.read_csv("./catalog.csv")
            except:
                print("Catalog File does not exits")
            finally:
                self.condition.release()
        else:
            toys_data = [
                ["Elephant", 100, random.randint(1000, 10000)],
                ["Whale", 100, random.randint(1000, 10000)],
                ["Dolphin", 100, random.randint(1000, 10000)],
                ["Tux", 100, random.randint(1000, 10000)],
                ["Fox", 100, random.randint(1000, 10000)],
                ["Python", 100, random.randint(1000, 10000)],
                ["Eagle", 100, random.randint(1000, 10000)],
                ["Bear", 100, random.randint(1000, 10000)],
                ["Tiger", 100, random.randint(1000, 10000)],
                ["Leopard", 100, random.randint(1000, 10000)],
                ["Lion", 100, random.randint(1000, 10000)],
                ["Giraffe", 100, random.randint(1000, 10000)],
                ["Zebra", 100, random.randint(1000, 10000)],
                ["Dog", 100, random.randint(1000, 10000)],
                ["Horse", 100, random.randint(1000, 10000)]
            ]
            self.condition.acquire()
            try:
                self.db = pd.DataFrame(toys_data, columns=["Name", "Stock", "Cost"])
                self.write()  # Write DataFrame to CSV
            except Exception as e:
                print("Cannot write to the DB")
            finally:
                self.condition.release()

        #add update catalog db inside a thread
        thread = threading.Thread(target=self.updateDB, daemon=True)
        thread.start()

    '''
    updates the stock every 10 seconds
    '''
    def updateDB(self, n=10): 
        while True:
            self.condition.acquire()
            try:
                df_filtered = self.db[self.db['Stock'] == 0]
                if len(df_filtered) > 0:
                    self.db.loc[df_filtered.index, 'Stock'] = 100
                    self.write()
                    self.clear_cache(df_filtered['Name'].tolist())
            except Exception as e:
                print("Received error in updating: ", e)
            finally:
                self.condition.release()
            time.sleep(n)

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
        print(f"Received Query with Item Name {request.ItemName}")
        if not request or not request.ItemName:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT) #if query invalid, return empty response with invalid argument in context
            context.set_details("Null argument provided")
            return catalog_pb2.QueryResponse()
        self.condition.acquire()
        # with self.read_lock:
        try:
            print(f"Processing Query with Item Name {request.ItemName}")
            filtered_indices = self.db.index[self.db['Name'] == request.ItemName]

            if len(filtered_indices) <= 0:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT) #if query invalid, return empty response with invalid argument in context
                context.set_details("Invalid argument provided")
                return catalog_pb2.QueryResponse()
            query_result = self.db.loc[filtered_indices[0]]
            return catalog_pb2.QueryResponse(Name=query_result['Name'], Cost=query_result['Cost'], Stock=query_result['Stock'])
        except Exception as e:
            print("Error occured during processing query in catalog service: ", e)
        finally:
            self.condition.release()


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
        print(f"Received Order with Item Name {request.ItemName} and quantity {request.Quantity}")
        if not request or not request.ItemName:
            return catalog_pb2.BuyResponse(Response=-1)
        # with self.write_lock:
        self.condition.acquire()
        try:
            print(f"Processing Order with Item Name {request.ItemName} and quantity {request.Quantity}")
            filtered_indices = self.db.index[self.db['Name'] == request.ItemName]
            if len(filtered_indices) == 0:
                return catalog_pb2.BuyResponse(Response=-1)
            if self.db.loc[filtered_indices[0]]['Stock'] < request.Quantity:
                return catalog_pb2.BuyResponse(Response=0)
            self.db.loc[filtered_indices[0], 'Stock'] -= request.Quantity
            self.write()
            self.clear_cache([request.ItemName])
            return catalog_pb2.BuyResponse(Response=1)
        except Exception as e:
            print("Error occured during updating a buy order in catalog service: ",e)
        finally:
            self.condition.release()

    def clear_cache(self, keys):
        try:
            host = os.getenv("HTTP_SERVER", HTTP_SERVER)  # Get machine name
            port = os.getenv("HTTP_PORT", HTTP_PORT)  # Get machine name
            url = "http://"+host+":"+str(port)+INVALIDATE_ENDPOINT
            data = {
                'names': keys
            }
            json_data = json.dumps(data)
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, data=json_data, headers=headers)
            if response.status_code == 200:
                print("Clear cache status : ", response.json()['data']['isSuccess'])
            else:
                print(f"Error while clearing cache")
        except Exception as ex:
            print("Could not connect to HTTP server, error->",ex)

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
