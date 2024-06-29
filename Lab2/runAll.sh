#!/bin/bash

export CATALOG_SERVER=localhost
export ORDER_SERVER=localhost
export HTTP_SERVER=localhost
pip install -r requirements.txt
cd ./src/server/catalog/
python3 -m grpc_tools.protoc -I./protos --python_out=. --pyi_out=. --grpc_python_out=. ./protos/catalog.proto
python3 catalog_service.py &

cd ../order/
python3 -m grpc_tools.protoc -I protos --python_out=. --pyi_out=. --grpc_python_out=. ./protos/order.proto
python3 order_service.py &

cd ../../frontend/
python3 http_service.py &
