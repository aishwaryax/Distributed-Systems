from concurrent import futures
import grpc
import order_pb2
import order_pb2_grpc
import catalog_pb2
import catalog_pb2_grpc
import os
import csv
from threading import Lock
from config import CATALOG_PORT, ORDER_PORT, CATALOG_SERVER, ORDER_SERVER, WORKERS, ORDER_SERVER_DETAILS
import pandas as pd
import sys

class OrderServicer(order_pb2_grpc.OrderServicer):
    def __init__(self):
        '''
        Initialized lock and gets orderNumber
        '''
        self.lock = Lock()

        #getting current path
        scriptDir = os.path.dirname(__file__)

        #getting current server id
        self.orderServerId = self.getOrderServerId()


        #setting file name and DB
        self.fileName = 'order'+'_'+str(self.orderServerId)+'.csv'
        
        #file
        self.db = os.path.join(scriptDir, self.fileName)

        #Dataframe
        self.data = pd.read_csv("./"+self.fileName)

        #getting current orderId
        self.orderNumber = self.getOrderNumber()
        
        #on initilaizition is_leader would be false
        self.is_leader = False

        #get current leader id
        self.leader_id = self.GetLeaderId()

        #when server comes back online then sync with the current leader
        self.syncWithReplica()
    
    def getOrderServerId(self):
        '''
        Returns server id which we get in cmd
        '''
        return int(sys.argv[2])

    
    def NotifyReplica(self, request, context):
        '''
        If incoming server id is of self then setting leader to be True
        '''
        if request.orderServersId ==  self.orderServerId:
            self.is_leader = True
            self.syncWithReplica()
        return order_pb2.BoolResponse(IsSuccess=True)

    def IsAlive(self, request, context):
        '''
        returns if the server is alive
        '''
        return order_pb2.IsAliveResponse(status=1, orderServersId=self.orderServerId,message="Order Server is alive")
    
    def IsLeader(self, request, context):
        '''
        return if self is leader or nots
        '''
        return order_pb2.BoolResponse(IsSuccess=self.is_leader)

    def syncWithReplica(self):
        '''
        When a replica comes back online it is synced with the leader
        '''
        
        
        port = None
        server_host = os.getenv("ORDER_SERVER", ORDER_SERVER)
        for service in ORDER_SERVER_DETAILS:
            port, process = service[0], service[1]
            if process == self.getOrderServerId():
                continue
            try: 
                lastOrderNumber = self.getOrderNumber()
                print("Last id in DB is:",lastOrderNumber)
                #getting data to sync from the leader
                with grpc.insecure_channel(server_host+':'+str(port)) as channel:
                    stub = order_pb2_grpc.OrderStub(channel)
                    response = stub.DataToSync(order_pb2.DataToSyncRequest(pendingOrderStartId = lastOrderNumber))
                #syncing data
                try:
                    self.lock.acquire()
                    print("Writing to original replica's local DB")
                    try:
                        with open(self.db, 'a', newline='') as file:
                            writer = csv.writer(file)
                            rows = [(order.OrderNumber, order.ToyName, order.ToyQuantity) for order in response.OrderRequests]
                            writer.writerows(rows)
                        self.data = pd.read_csv("./"+self.fileName)
                    except:
                        print("Could not write back to replica")
                        print(f"Error while writing data from replica {port} to replica: {e}")
                    finally:
                        self.lock.release()
                except Exception as e:
                    print("Could not sync with replica: ", port)
                    print("Error while syncing to replica->", e)
            except Exception as e:
                print("Cannot connect to replica: ", port)
                print("Error while connecting to replica: ", e)


    
    def DataToSync(self, request, context):
        '''
        Returns data to sync to the replica
        '''
        #replica's id to sync with
        # print("In Data to Sync")
        idToSync = request.pendingOrderStartId
        sync_data = order_pb2.SyncData()
        with open(self.fileName, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                order_number = int(row['orderNumber'])
                product_name = row['productName']
                quantity = int(row['quantity'])
                if order_number >= idToSync:
                    # print(f"Appending order_id: {order_number} to sync data response")
                    sync_data.OrderRequests.append(order_pb2.GetResponse(OrderNumber=order_number, ToyName=product_name, ToyQuantity=quantity))
        # print("Data to sync sending response: ", sync_data)
        return sync_data

    def GetLeaderId(self):
        '''
        Sets leaderId on startup
        '''
        for server in ORDER_SERVER_DETAILS:
            port = server[0]
            id = server[1]
            if id == self.orderServerId:
                continue
            try:
                server_host = os.getenv("ORDER_SERVER", ORDER_SERVER)
                with grpc.insecure_channel(server_host+':'+str(port)) as channel:
                    stub = order_pb2_grpc.OrderStub(channel)
                    response = stub.IsLeader(order_pb2.EmptyRequest())
                    if response.IsSuccess:
                        # print("Leader id is->",id)
                        return id
                    else:
                        continue
            except Exception as e:
                print(f'Could not connect to {port} on {id}')
        return None
    
    def SynchronizeOrder(self, request, context):
        '''
        Syncing with replicas Simultaneously
        '''
        self.lock.acquire()
        try:
            with open(self.db, 'a', newline='') as file:
                writer = csv.writer(file)
                rows = [(order.OrderNumber, order.ToyName, order.ToyQuantity) for order in request.OrderRequests]
                writer.writerows(rows)
            self.data = pd.read_csv("./"+self.fileName)
            return order_pb2.BoolResponse(IsSuccess=True)
        finally:
            print("Synced database with replica")
            self.lock.release()


    def getOrderNumber(self):
        '''
        returns orderNumber by counting number of rows present in csv file
        '''
        file = open(self.db)
        csvreader = csv.reader(file)
        orderNumberHeader, productNameHeader, quantityHeader = next(csvreader)
        val = sum(1 for row in csvreader)
        file.close()
        return val
    

    def buyOrder(self, request, context):
        '''
        if order can be placed through catalog service then we return order number as response else we return -1
        '''
        print(f'Order received for toy: {request.ToyName} and for quantity: {request.ToyQuantity}')
        quantity = request.ToyQuantity
        orderNumberToReturn = None
        if quantity <= 0:
            return order_pb2.BuyResponse(OrderNumber=-1, Message="Invalid quantity")
        else:
            
            catalogService = os.getenv("CATALOG_SERVER", CATALOG_SERVER)
            try:    
                with grpc.insecure_channel(catalogService+':'+str(CATALOG_PORT)) as channel:
                    stub = catalog_pb2_grpc.CatalogStub(channel)
                    response = stub.Buy(catalog_pb2.BuyRequest(ItemName=request.ToyName, Quantity=quantity))
                    if response.Response == -1:
                        return order_pb2.BuyResponse(OrderNumber=-1, Message="Invalid Toy Name")
                    elif response.Response == 0:
                        return order_pb2.BuyResponse(OrderNumber=-1, Message="Insufficient Quantity")
                    else:
                        self.lock.acquire()
                        orderNumberToReturn = self.getOrderNumber()
                        field = [orderNumberToReturn, request.ToyName, request.ToyQuantity]
                        try:
                            with open(self.db, 'a', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(field)
                                print(f"Order has been processed with OrderNumber {orderNumberToReturn}")
                            self.data = pd.read_csv("./"+self.fileName)                           
                            return order_pb2.BuyResponse(OrderNumber=orderNumberToReturn, Message="Order processed successfully")
                        finally:
                            self.lock.release()
                            for server in ORDER_SERVER_DETAILS:
                                port = server[0]
                                id = server[1]
                                if id == self.orderServerId:
                                    continue
                                try:
                                    server_host = os.getenv("ORDER_SERVER", ORDER_SERVER)
                                    with grpc.insecure_channel(server_host+':'+str(port)) as channel:
                                        stub = order_pb2_grpc.OrderStub(channel)
                                        sync_data = order_pb2.SyncData()
                                        sync_data.OrderRequests.append(order_pb2.GetResponse(OrderNumber=orderNumberToReturn, ToyName=request.ToyName, ToyQuantity=request.ToyQuantity))                                        
                                        stub.SynchronizeOrder(sync_data)
                              
                                except:
                                  print(f'Replica: {port}, {id} could not be notified.')      
                            print(f'Order processed for toy: {request.ToyName} and for quantity: {request.ToyQuantity}')
            except Exception as e:
                print("Could not connect to Catalog Service")
                print("Error is =>", e)
                print(e.with_traceback)
                return order_pb2.BuyResponse(OrderNumber=-1, Message="Could not connect to Catalog Service")

    def GetOrder(self, request, context):
        '''
        Get order returns order details if order id exits else returns error code
        '''
        if not request:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT) #if query invalid, return empty response with invalid argument in context
            context.set_details("Null argument provided")
            return order_pb2.GetResponse()
        with self.lock:
            filtered_indices = self.data.index[self.data['orderNumber'] == request.OrderNumber]
            if len(filtered_indices) <= 0:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT) #if query invalid, return empty response with invalid argument in context
                context.set_details("Invalid argument provided")
                return order_pb2.GetResponse()
            query_result = self.data.loc[filtered_indices[0]]
            return order_pb2.GetResponse(OrderNumber=query_result['orderNumber'], ToyName=query_result['productName'], ToyQuantity=query_result['quantity'])
        

def serve():
    '''
    This method starts the server
    '''
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=WORKERS))
    order_pb2_grpc.add_OrderServicer_to_server(OrderServicer(), server)
    
    # Read server from environment variable if set, otherwise from config file
    serverHost = os.getenv("ORDER_SERVER", ORDER_SERVER)
    #getting port from cmd
    ORDER_PORT = sys.argv[1]
    server.add_insecure_port(serverHost + ':'+str(ORDER_PORT))

    
    server.start()
    print("The Order server is running on port:", ORDER_PORT)
    try:
        server.wait_for_termination()   
    except KeyboardInterrupt:
        print("Server shutting down")

if __name__ == '__main__':
    serve()