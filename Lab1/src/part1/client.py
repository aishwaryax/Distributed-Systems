#!/usr/bin/env python3
import socket
import random
from config import BUFFER_SIZE, PORT, HOSTNAME, NUM_OF_REQUEST
import time


host = HOSTNAME  # Get machine name
port = PORT  # Specify the port to connect to
latency = [] # to store average latency per client

 # Close the socket when done
def query(toyName, clientSocket):
    '''
    This method sends a query to client
    
    '''
    #creating a query message to send to server
    message = "Query "+toyName
    print(message)

    startTime = time.time()

    #encoding the message
    clientSocket.send(message.encode())

    #receiving response from server and printing the appropriate response
    response = clientSocket.recv(BUFFER_SIZE)
    response = response.decode()

    endTime = time.time()

    latency.append(endTime-startTime)


    if int(response) == -1:
        print(f"{toyName} not found")
    elif int(response) == 0:
        print(f"{toyName} not in stock")
    else:
        print(f"{toyName}'s price is {response}")


def sendRequest():
    '''
    This method opens a connection ans sends the connection along with random toy name to query method
    '''
    #selecting a random toyname from below data
    requestData = ["Tux", "Whale", "INVALID_TOY"]

    for _ in range(NUM_OF_REQUEST):
        clientSocket = socket.socket()
        
        

        #connection with server
        clientSocket.setblocking(True)
        clientSocket.connect((host, port))
        query(random.choice(requestData), clientSocket)
        clientSocket.close()

        

if __name__ == "__main__":
    sendRequest()

    latencyAvg = sum(latency) / len(latency)
    print("Average latency is -> ", latencyAvg)
