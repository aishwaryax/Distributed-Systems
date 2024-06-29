from concurrent import futures
import grpc
import order_pb2
import order_pb2_grpc
import catalog_pb2
import catalog_pb2_grpc
import os
import csv
from threading import Lock
from config import CATALOG_PORT, ORDER_PORT, CATALOG_SERVER, ORDER_SERVER, WORKERS


class OrderServicer(order_pb2_grpc.OrderServicer):
    def __init__(self):
        '''
        Initialized lock and gets orderNumber
        '''
        self.lock = Lock()
        scriptDir = os.path.dirname(__file__)
        fileName = 'order.csv'
        self.db = os.path.join(scriptDir, fileName)
        self.orderNumber = self.getOrderNumber()

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

        if quantity <= 0:
            return order_pb2.BuyResponse(OrderNumber=-1, Message="Invalid quantity")
        else:

            catalogService = os.getenv("CATALOG_SERVER", CATALOG_SERVER)
            
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
                        return order_pb2.BuyResponse(OrderNumber=orderNumberToReturn, Message="Order processed successfully")
                    finally:
                        self.lock.release()
                        print(f'Order processed for toy: {request.ToyName} and for quantity: {request.ToyQuantity}')

def serve():
    '''
    This method starts the server
    '''
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=WORKERS))
    order_pb2_grpc.add_OrderServicer_to_server(OrderServicer(), server)
    
    # Read server from environment variable if set, otherwise from config file
    serverHost = os.getenv("ORDER_SERVER", ORDER_SERVER)
    server.add_insecure_port(serverHost + ':'+str(ORDER_PORT))
    server.start()
    print("The Order server is running.")
    try:
        server.wait_for_termination()   
    except KeyboardInterrupt:
        print("Server shutting down")

if __name__ == '__main__':
    serve()