#!/usr/bin/env python3
import random
import requests
from config.config import FRONTEND_PORT, FRONTEND_HOSTNAME, NUM_OF_REQUEST, GET_PRODUCT, PLACE_ORDER, PROBABILITY
import time
import sys
import os

host = os.getenv("HTTP_SERVER", FRONTEND_HOSTNAME)  # Get machine name
port = FRONTEND_PORT  # Specify the port to connect to
queryLatency = [] # to store average query latency per client
buyLatency = [] # to store average buy latency per client
queryUrl = "http://"+host+":"+str(FRONTEND_PORT)+GET_PRODUCT
orderUrl = "http://"+host+":"+str(FRONTEND_PORT)+PLACE_ORDER

def sendRequest():
    #selecting a random toyname from below data
    requestData = ["Elephant", "Tux", "Whale", "Dolphin", "Fox", "Python", "ElephaNT", "INVALID_TOY"]
    probability = PROBABILITY
    session = requests.Session()
    
    for i in range(NUM_OF_REQUEST):
        
        toyName = random.choice(requestData)
        print(f"Query {i} toyname: {toyName}")
        url = queryUrl + toyName
        startTimeQuery = time.time()
        queryResponse = requests.get(url, cookies={'client_id': str(sys.argv[1])})
        endQueryTime = time.time()
        queryLatency.append(endQueryTime-startTimeQuery)

        #querying toy
        jsonData = queryResponse.json()

        if 'data' in jsonData:
            data = queryResponse.json().get('data', {})
            quantity = data.get('quantity', 0)

            #placing order if quantity > 0 and rondom value <= expected probability 
            if quantity > 0 and random.random() <= probability:
                print(f'Making a buy request for toy: {toyName}')
                orderData = {"name":toyName, "quantity": 1}

                startTimeBuy = time.time()
                orderResponse = session.post(orderUrl, json=orderData)

                jsonData = orderResponse.json()

                if 'data' in jsonData:
                    endTimeBuy = time.time()
                    buyLatency.append(endTimeBuy-startTimeBuy)
                    print(f'Request {i}: Order for {toyName} of quantity 1 placed successfully.')   
                else:
                    print(f'Request {i}: Order for {toyName} of quantity 1 Failed')
            else:
                print('Either quantity is 0 or probability is too low')

        else:
            error = queryResponse.json().get('error', {})
            message = error.get('message', '')
            print(f'Request {i}: Query for {toyName} failed, status = {queryResponse.status_code} with message = {message}')
        
    session.close()

        
        

if __name__ == "__main__":
    sendRequest()
    avgQueryLatency = sum(queryLatency) / len(queryLatency)
    avgBuyLatency = 0 if len(buyLatency) == 0 else sum(buyLatency) / len(buyLatency)
    print("Average  query latency is -> ", avgQueryLatency)
    print("Average  Buy latency is -> ", avgBuyLatency)
