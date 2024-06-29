import json
import re
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import threading
from productBL import ProductBL
from config import HTTP_SERVER, HTTP_PORT, ORDER_SERVER_DETAILS, ORDER_SERVER
import http.cookies
from readerwriterlock import rwlock
import order_pb2_grpc
import order_pb2
import grpc


class LeaderElection():
    def __init__(self):
        self.leader_port = None
        self.leader_id = None
        a = rwlock.RWLockFairD()
        self.reader_lock = a.gen_rlock()
        self.writer_lock = a.gen_wlock() 

    '''
    elects a leader by pinging all the order servers
    '''
    def electLeader(self):
        is_leader_elected = False
        try:
            self.writer_lock.acquire()
            for server in ORDER_SERVER_DETAILS:
                port = server[0]
                id = server[1]
                
                server_host = os.getenv("ORDER_SERVER", ORDER_SERVER)
                
                try:
                    with grpc.insecure_channel(server_host+':'+str(port)) as channel:
                        stub = order_pb2_grpc.OrderStub(channel)
                        #if leader is not yet elected then check if the sever is alive, and elect as leader
                        if not is_leader_elected:
                            
                            #checking if server is live
                            responseIsAlive = stub.IsAlive(order_pb2.EmptyRequest())

                            #if live we have found the leader
                            if responseIsAlive.status == 1:
                                self.leader_id = id
                                self.leader_port = port
                                is_leader_elected = True
                                print("Elected leader's port:", self.leader_port)
                                response = stub.NotifyReplica(order_pb2.NotifyReplicaRequest(orderServersId=self.leader_id))     
                                if not response.IsSuccess:
                                    print("Leader could not be notified")

                        else: #notify remaining servers that leader has been elected

                            try:
                                with grpc.insecure_channel(server_host+':'+str(port)) as channel:
                                    stub = order_pb2_grpc.OrderStub(channel)
                                    response = stub.NotifyReplica(order_pb2.NotifyReplicaRequest(orderServersId=self.leader_id))
                                    if not response.IsSuccess:
                                        print("Replica's could not be notified")

                            except Exception as e:
                                print(f"Replica with id: {id} and port: {port} could not be notified, exiting with error: ", e)   
                                                
                except Exception as e:
                    print(f"Could not connect to order service with id: {id}, exiting with error code: ", e)
        finally:
            self.writer_lock.release()
            



    '''
    returns selected leaders port
    '''
    def getLeaderPort(self):
        try:
            self.reader_lock.acquire()
            return self.leader_port
        finally:
            self.reader_lock.release()
        
        
class HttpReqHandler(BaseHTTPRequestHandler):
    bl = None
    
    def __init__(self, leaderElection, *args, **kwargs):
        # Initialize ProductBL instance if not already initialized
        self.leaderobj = leaderElection
        #setting leader port in BL object
        while True:
            try:
                self.leaderPort = self.leaderobj.getLeaderPort()
                if self.bl is None:
                    self.bl = ProductBL(self.leaderPort)
            except:
                self.leaderobj.electLeader()
                continue
            break
        super().__init__(*args, **kwargs)


    def do_POST(self):
        cookie = http.cookies.SimpleCookie(self.headers.get('Cookie'))
        if 'client_id' in cookie:
            client_id = cookie['client_id'].value
            print(f"Thread assigned : {threading.current_thread().ident}, Client ID: {client_id}")
        if re.search('/orders', self.path):
            length = int(self.headers.get('content-length'))
            data = self.rfile.read(length).decode('utf8')
            json_data = json.loads(data)
            name = json_data.get('name', '')
            quantity = json_data.get('quantity', '')
            # Call the order method from ProductBL and handle response
                    
            while True:
                resp_data = self.bl.order(name, int(quantity))
                print(resp_data)
                #orderNumber = -2 for connection error with server
                if resp_data.OrderNumber == -2:
                    self.leaderobj.electLeader()
                    self.bl = ProductBL(self.leaderobj.getLeaderPort())
                    continue
                break

            if resp_data.OrderNumber != -1:  
                resp_data = {
                    "data": {
                        "order_number": resp_data.OrderNumber
                    }
                }
            else:
                resp_data = {
                    "error": {
                        "code": 304,
                        "message": "could not post order"
                    }
                }
            # Send response to client
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(resp_data).encode('utf-8'))
        
        elif re.search('/invalidate', self.path):
            length = int(self.headers.get('content-length'))
            data = self.rfile.read(length).decode('utf8')
            json_data = json.loads(data)
            names = json_data.get('names', [])
            # Call the order method from ProductBL and handle response
            self.bl.clear_cache(names)
            resp_data = {
                    "data": {
                        "isSuccess": True
                    }
                }
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(resp_data).encode('utf-8'))
        else:
            # Send forbidden response for non-matching path
            self.send_response(403)
            self.end_headers()

    def do_GET(self):
        cookie = http.cookies.SimpleCookie(self.headers.get('Cookie'))
        if 'client_id' in cookie:
            client_id = cookie['client_id'].value
            print(f"Thread assigned : {threading.current_thread().ident}, Client ID: {client_id}")
        if re.search(r'^/products/[\w-]+$', self.path):
            name = self.path.split('/')[-1]
            # Call the get_catalog method from ProductBL and handle response
            resp_data = self.bl.get_catalog(name)
            if resp_data.Name != "":
                # Send success response with product details
                resp_data = {
                    "data": {
                        "name": resp_data.Name,
                        "price": resp_data.Cost,
                        "quantity": resp_data.Stock
                    }
                }
            else:
                # Send not found response if product name is empty
                resp_data = {
                    "error": {
                        "code": 404,
                        "message": "product not found"
                    }
                }
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(resp_data).encode('utf-8'))
        elif re.search(r'^/orders/[\w-]+$', self.path):
            order_no = int(self.path.split('/')[-1])
            # Call the get_order method from ProductBL and handle response
            while True:
                resp_data = self.bl.get_order(order_no)

                #orderNumber = -2 for connection error with server
                if resp_data.OrderNumber == -2:
                    self.leaderobj.electLeader()
                    self.bl = ProductBL(self.leaderobj.getLeaderPort())
                    continue
                break
            if resp_data.OrderNumber != -1:
                # Send success response with product details
                resp_data = {
                    "data": {
                        "number": resp_data.OrderNumber,
                        "name": resp_data.ToyName,
                        "quantity": resp_data.ToyQuantity
                    }
                }
            else:
                # Send not found response if product name is empty
                resp_data = {
                    "error": {
                        "code": 404,
                        "message": "order not found"
                    }
                }
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(resp_data).encode('utf-8'))
        else:
            # Send forbidden response for non-matching path
            self.send_response(403)
            self.end_headers()




if __name__ == '__main__':
    http_service = os.getenv("HTTP_SERVER", HTTP_SERVER)
    
    # Leader Election object
    leaderElection = LeaderElection()
    leaderElection.electLeader()
    
    def handle(*args, **kwargs):
        HttpReqHandler(leaderElection, *args,  **kwargs)

    server = ThreadingHTTPServer((http_service, HTTP_PORT), handle)
    print(f"Starting server on {http_service}:{HTTP_PORT}")


    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        print("Frontend Server stopped.")
