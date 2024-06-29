FROM python:3.8

ENV CATALOG_SERVER=spring24-lab2-mitalee18-aishwaryax-catalog-1
ENV ORDER_SERVER=spring24-lab2-mitalee18-aishwaryax-order-1
ENV HTTP_SERVER=spring24-lab2-mitalee18-aishwaryax-frontend-1

RUN pip install grpcio grpcio-tools

WORKDIR /frontend

COPY ./http_service.py .

COPY ./protos/ .

COPY ./config.py .

COPY ./grpc_channel_manager.py .

COPY ./productBL.py .

COPY ./protos/catalog.proto ./protos/

COPY ./protos/order.proto ./protos/

COPY ./productBL.py .

RUN python -m grpc_tools.protoc -I protos --python_out=. --grpc_python_out=. protos/catalog.proto

RUN python -m grpc_tools.protoc -I protos --python_out=. --grpc_python_out=. protos/order.proto

ENTRYPOINT ["python3", "-u", "http_service.py"]