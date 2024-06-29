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
from pathlib import Path
from raft_utils import Utils, CommitLog
from queue import Queue

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

        self.log = CommitLog(server_id=self.orderServerId)
        commit_logfile = Path(self.log.file)
        commit_logfile.touch(exist_ok=True)


        self.commit_index = -1

        self.last_index, self.last_term = self.log.get_last_entry()
        self.next_index = [0]*len(ORDER_SERVER_DETAILS)
        self.current_term = self.last_term

        self.syncWithLeader()
    
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
            self.current_term += 1
            self.syncWithLeader()
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

    def syncWithLeader(self):
        if self.leader_id == self.orderServerId or not self.leader_id:
            return
        port = None
        for server in ORDER_SERVER_DETAILS:
            if self.leader_id == server[1]:
                port = server[0]
        server_host = os.getenv("ORDER_SERVER", ORDER_SERVER)
        try: 
            last_index, _ = self.log.get_last_entry()
            with grpc.insecure_channel(server_host+':'+str(port)) as channel:
                stub = order_pb2_grpc.OrderStub(channel)
                resp = stub.RequestLogs(order_pb2.RequestLogsRequest(Index = last_index, Server=self.orderServerId))
        except Exception as e:
            print("syncWithLeader Cannot connect to leader: ", port)

    def RequestLogs(self, request, context):
        port = None
        for server in ORDER_SERVER_DETAILS:
            if request.Server == server[1]:
                port = server[0]
        res = Queue()
        Utils.run_thread(fn=self.send_precommit_request, args=(request.Server, port, res, ))
        while True:
            res.get(block=True, timeout=5)
            break
        last_commit_index = self.log.get_last_commit(self.getOrderNumber())
        try: 
            server_host = os.getenv("ORDER_SERVER", ORDER_SERVER)
            with grpc.insecure_channel(server_host+':'+str(port)) as channel:
                stub = order_pb2_grpc.OrderStub(channel)
                stub.CommitIndex(order_pb2.CommitIndexRequest(Index = last_commit_index))
            return order_pb2.BoolResponse(IsSuccess=True)
        except Exception as e:
            print("RequestLogs Cannot connect to replica: ", port)
            return order_pb2.BoolResponse(IsSuccess=False)


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
                        return id
                    else:
                        continue
            except Exception as e:
                print(f'Could not connect to {port} on {id}')
        return None
    

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
        orderNumberToReturn, last_index = None, None
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
                        try:
                            self.lock.acquire()
                            orderNumberToReturn = self.getOrderNumber()
                            cmd = f"{orderNumberToReturn}|{request.ToyName}|{request.ToyQuantity}"
                            self.log.write_log(self.current_term, cmd)
                            shouldCommit = self.send_append_entries_logic()
                            last_index, _ = self.log.get_last_entry()
                            if not shouldCommit:
                                self.log.truncate(last_index)
                                return order_pb2.BuyResponse(OrderNumber=-2, Message="Could not post order")
                            self.commit_index = last_index               
                            self.update_state_machine(cmd)
                            return order_pb2.BuyResponse(OrderNumber=orderNumberToReturn, Message="Order processed successfully")
                        finally:
                            self.lock.release()
                            for service in ORDER_SERVER_DETAILS:
                                port, process = service[0], service[1]
                                if process == self.getOrderServerId():
                                    continue
                                try: 
                                    server_host = os.getenv("ORDER_SERVER", ORDER_SERVER)
                                    with grpc.insecure_channel(server_host+':'+str(port)) as channel:
                                        stub = order_pb2_grpc.OrderStub(channel)
                                        response = stub.CommitIndex(order_pb2.CommitIndexRequest(Index = self.log.get_last_commit(orderNumberToReturn)))
                                except Exception as e:
                                    print("buyOrder : Cannot connect to replica: ", port)
            except Exception as e:
                print("Could not connect to Catalog Service")
                return order_pb2.BuyResponse(OrderNumber=-1, Message="Could not connect to Catalog Service")
            

    def send_append_entries_logic(self):
        try:
            res = Queue()
            for server in ORDER_SERVER_DETAILS:
                port = server[0]
                id = server[1]
                if id != self.orderServerId:
                    Utils.run_thread(fn=self.send_precommit_request, args=(id, port, res, ))
            if len(ORDER_SERVER_DETAILS) > 1:        
                votes = 1 #self vote
                while True:
                    res.get(block=True, timeout=5)
                    votes += 1
                    if votes > (len(ORDER_SERVER_DETAILS)/2.0):
                        return True
                    else:
                        return False
            else:
                return True
        except Exception as ex:
            return False
        
    def send_precommit_request(self, id, port, res=None):
        prev_idx = self.next_index[id - 1]-1
        log_slice = self.log.read_logs(prev_idx)
        if prev_idx == -1:
            prev_term = 0
        else:
            if len(log_slice) > 0:
                prev_term = log_slice[0].Term
                log_slice = log_slice[1:] if len(log_slice) > 1 else []
            else:
                prev_term = 0
                log_slice = []
        request = order_pb2.AppendEntriesRequest(Term=self.current_term, LeaderId=self.orderServerId, PrevLogIndex=prev_idx, PrevLogTerm=prev_term, Entries=log_slice, LeaderCommit=self.commit_index)
        response = None
        retry_attempts = 0
        while True:
            if self.is_leader:
                server_host = os.getenv("ORDER_SERVER", ORDER_SERVER)
                try:
                    with grpc.insecure_channel(server_host+':'+str(port)) as channel:
                        stub = order_pb2_grpc.OrderStub(channel)
                        response = stub.AppendEntries(request)
                except Exception as ex:
                    break
                if response:
                    server, curr_term, success, index = response.Server, response.Term, response.IsSuccess, response.Index
                    if curr_term > self.current_term:
                        self.current_term = curr_term
                    if self.is_leader and curr_term == self.current_term:
                        if success:
                            self.next_index[server-1] = index+1
                        else:
                            self.next_index[server-1] = max(0, self.next_index[server-1]-1)
                            self.send_precommit_request(id, port, res)                    
                    break
            else:
                break
        if res and response and response.IsSuccess:
            res.put('ok')
            
    def AppendEntries(self, request, context):
        try:
            success, index = False, 0
            if request.Term > self.current_term:
                self.current_term = request.Term
            if request.Term == self.current_term:
                self.leader_id = request.LeaderId
                logs = self.log.read_logs(request.PrevLogIndex, request.PrevLogTerm) if request.PrevLogIndex != -1 else []            
                success = request.PrevLogIndex == -1 or (len(logs) > 0 and logs[0].Term == request.PrevLogTerm)
                if success:
                    last_index, last_term = self.log.get_last_entry()
                    if len(request.Entries) > 0 and last_term == request.Entries[-1].Term and last_index == self.commit_index:
                        index = self.commit_index
                    else: 
                        commands = [f"{request.Entries[i].Command}" for i in range(len(request.Entries))]
                        last_index, _ = self.log.rewrite_log(request.PrevLogIndex+1, commands, self.current_term)
                        self.commit_index = last_index
                        index = last_index
            return order_pb2.AppendEntriesResponse(Server=self.orderServerId, Term=self.current_term, IsSuccess=success, Index=index)
        except Exception as ex:
            return order_pb2.AppendEntriesResponse()
        
    
    def CommitIndex(self, request, context):
        self.lock.acquire()
        try:
            last_commit = self.log.get_last_commit(self.getOrderNumber() - 1)
            logs = self.log.read_logs(last_commit + 1, request.Index)
            for log in logs:
                self.update_state_machine(log.Command)
            return order_pb2.BoolResponse(IsSuccess=True)
        finally:
            self.lock.release()

        

    def update_state_machine(self, command):
        order_id, toyname, qty = command.split("|")
        row = [order_id, toyname, qty]
        with open(self.db, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)
        self.data = pd.read_csv("./"+self.fileName)

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