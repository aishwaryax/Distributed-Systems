#!/usr/bin/env python3
import random
import requests
from config.config import FRONTEND_PORT, FRONTEND_HOSTNAME, NUM_OF_REQUEST, GET_PRODUCT, PLACE_ORDER, PROBABILITY, GET_ORDER_HISTORY
import time
import sys
import os
import pandas as pd

host = os.getenv("HTTP_SERVER", FRONTEND_HOSTNAME)  # Get machine name
port = FRONTEND_PORT  # Specify the port to connect to
queryLatency = [] # to store average query latency per client
buyLatency = [] # to store average buy latency per client
lookupOrderLatency = [] #to store average lookup per client
successfulOrderRequests = pd.DataFrame(columns=["QueryId", "ToyName", "Quantity", "OrderNumber"]) #stores order requests that are successfu
queryUrl = "http://"+host+":"+str(FRONTEND_PORT)+GET_PRODUCT
orderUrl = "http://"+host+":"+str(FRONTEND_PORT)+PLACE_ORDER
orderHistoryUrl = "http://"+host+":"+str(FRONTEND_PORT)+GET_ORDER_HISTORY

def sendRequest():
    #selecting a random toyname from below data
    requestData = ["Elephant", "Tux", "Whale", "Dolphin", "Fox", "Python", "Eagle", "Bear", "Tiger", "Leopard", "Lion", "Giraffe", "Zebra", "Dog", "Horse", "ElephaNT", "INVALID_TOY"]
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
                    successfulOrderRequests.loc[len(successfulOrderRequests.index)] = [i, toyName, 1, jsonData['data']['order_number']] 
                else:
                    print(f'Request {i}: Order for {toyName} of quantity 1 Failed')
            else:
                print('Either quantity is 0 or probability is too low')

        else:
            error = queryResponse.json().get('error', {})
            message = error.get('message', '')
            print(f'Request {i}: Query for {toyName} failed, status = {queryResponse.status_code} with message = {message}')
        
    session.close()

def validateResults():
    df = successfulOrderRequests

    for row in df.itertuples():
        order_id = row.OrderNumber
        orderQueryUrl = orderHistoryUrl + str(order_id)
        try:
            startTime = time.time()
            orderQueryResponse = requests.get(orderQueryUrl, cookies={'client_id': str(sys.argv[1])})
            endTime = time.time()

            lookupOrderLatency.append(endTime - startTime)


            jsonData = orderQueryResponse.json()
            if "data" in jsonData:
                if (row.OrderNumber == jsonData['data']['number'] and
                    row.ToyName == jsonData['data']['name'] and
                    row.Quantity == jsonData['data']['quantity']):
                    print(f"matched for orderId: {row.OrderNumber}")
                    continue

                if row.OrderNumber != jsonData['data']['number']:
                    print(f"Error: Local OrderNumber is: {row.OrderNumber} and API is returning {jsonData['data']['number']}")

                if row.ToyName != jsonData['data']['name']:
                    print(f"Error: Local ToyName is: {row.ToyName} and API is returning {jsonData['data']['name']}")

                if row.Quantity != jsonData['data']['quantity']:
                    print(f"Error: Local quantity is: {row.Quantity} and API is returning {jsonData['data']['quantity']}")
            else:
                print('API is not returning data field for order id:', order_id)
        except Exception as e:
            print("Client request error :",e)
        
        

if __name__ == "__main__":
    sendRequest()
    validateResults()
    avgQueryLatency = sum(queryLatency) / len(queryLatency)
    avgBuyLatency = 0 if len(buyLatency) == 0 else sum(buyLatency) / len(buyLatency)
    avgOrderLookUpLatency = 0 if len(lookupOrderLatency) == 0 else sum(lookupOrderLatency) / len(lookupOrderLatency)
    print("Average  query latency is -> ", avgQueryLatency)
    print("Average  Buy latency is -> ", avgBuyLatency)
    print("Average  Order Lookup latency is -> ", avgOrderLookUpLatency)
