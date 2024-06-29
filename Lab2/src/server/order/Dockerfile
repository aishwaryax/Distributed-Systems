FROM python:3.8

ENV CATALOG_SERVER=spring24-lab2-mitalee18-aishwaryax-catalog-1
ENV ORDER_SERVER=spring24-lab2-mitalee18-aishwaryax-order-1

RUN pip install grpcio grpcio-tools

WORKDIR /order

COPY ./order_service.py .

COPY ./config.py .

COPY ./protos/ .

COPY ./protos/catalog.proto ./protos/

COPY ./protos/order.proto ./protos/

COPY ./order.csv .

RUN python -m grpc_tools.protoc -I protos --python_out=. --grpc_python_out=. protos/catalog.proto

RUN python -m grpc_tools.protoc -I protos --python_out=. --grpc_python_out=. protos/order.proto

ENTRYPOINT ["python3", "-u", "order_service.py"]
