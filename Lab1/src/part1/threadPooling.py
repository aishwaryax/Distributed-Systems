import threading
from toyStore import ToyStore
class ThreadPooling:
    def __init__(self, poolSize):
        #Thread Pooling Constructor
        self.poolSize = poolSize
        self.queue = []
        self.thread = []
        self.condition = threading.Condition() #created a lock
        self.workerThreadCreation() #creating workers
        self.toyStoreObject = ToyStore()

    
    def workerThreadCreation(self):
        '''
        This method creaters worker threads
        '''
        for _ in range(self.poolSize):
            thread = threading.Thread(target=self.worker)
            thread.daemon = True
            thread.start()
            self.thread.append(thread)
        print(f'Threads  of poolsize {self.poolSize} created and started')

    def worker(self):
        '''
        This method assigns tasks to worker thread
        '''
        while True:
            #Obtaining lock before accessing the queue
            self.condition.acquire()
            try:
                client, request = self.dequeue()
            finally:
                #Releasing lock even if an exception occurs
                self.condition.release()  

            if request is None:
                continue

            print('Request is being executed on thread -> ' + str(threading.current_thread().ident)+' incoming request from'+str(client))
            
            #decoding client's request
            requestdata = request.decode()
            
            #executing query
            valueReturned = self.toyStoreObject.query(requestdata)

            #returning back to client
            client.send(str(valueReturned).encode())

            #closing connection with client
            client.close()

            print('Request has been completed on thread -> ' + str(threading.current_thread().ident))
    

    def close(self):
        '''
        This method signals thread to exit
        '''
        # Add None tasks to the queue to signal threads to exit
        for thread in self.thread:
            thread.join()

    
    def enqueue(self, client, request):
        '''
        This method added the request along with connection to the queue
        '''
        #acquiring lock before adding to queue
        try:
            self.condition.acquire()
            self.queue.append((client, request))
            self.condition.notify() #will unblock only one thread
        finally:
            self.condition.release()

        
    def dequeue(self):
        '''
        This method removes the request along with connection from the queue
        '''
        client, request = None, None
        
        try:
            self.condition.acquire()
            #if queue is non empty then pop from queue, release lock and return
            if len(self.queue) > 0:
                client, request = self.queue.pop(0)
            else:
                #will wait to be notified if we have added anything in queue
                self.condition.wait()
        finally:
            self.condition.release()
        return (client, request)