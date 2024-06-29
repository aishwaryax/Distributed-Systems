#!/usr/bin/env python3
import socket
from threadPooling import ThreadPooling
from config import BUFFER_SIZE, POOL_SIZE, HOSTNAME, PORT

def handleServer():
    '''
    This method handles all calls made to server
    '''
    server = socket.socket()
    # Get local machine name
    host = HOSTNAME  
    # Reserve a port for your service
    port = PORT  
    
    # Bind to the port
    server.bind((host, port))  
    # Now wait for client connection
    print(f"Server listening on port: {port}")
    server.listen()

    threadPool = ThreadPooling(POOL_SIZE)
    try:
        while True:
            # Establish connection with client
            client, addr = server.accept() 

            # lock acquired
            print(f"Connection from {addr} has been established.")

            # Receive request msg from client in the number of predefined bytes ie BUFFER SIZE
            reqMsg = client.recv(BUFFER_SIZE)
            
            # Add request to our threadpool
            threadPool.enqueue(client, reqMsg)
    except KeyboardInterrupt:
        del(threadPool)
        print("Keyboard interrupt received. Shutting down server...")
        server.close()
    except Exception as e:
        del(threadPool)
        print(f"An error occurred in the server: {e}")
        


if __name__ == "__main__":
    handleServer()
   

    

