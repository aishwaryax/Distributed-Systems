#!/bin/bash

# Step 1: Remove existing output directory
rm -rf output

# Step 2: Create a new output directory
mkdir output

# Step 3: Change directory to server/catalog and start catalog_service.py
cd server/catalog
python3 -u catalog_service.py > ../../output/catalog_service.txt 2>&1 &

# Step 4: Change back to the parent directory (server)
cd ..

# Step 5: Change directory to server/order and start order_service.py with specified arguments
cd order
python3 -u order_service.py 56365 1 > ../../output/order_1.txt 2>&1 &
python3 -u order_service.py 56366 2 > ../../output/order_2.txt 2>&1 &
python3 -u order_service.py 56367 3 > ../../output/order_3.txt 2>&1 &

sleep 5

cd ../..
cd frontend
python3 -u http_service.py > ../output/http_service.txt 2>&1 &