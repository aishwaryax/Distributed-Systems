FROM python:3.8

ENV CATALOG_SERVER=spring24-lab2-mitalee18-aishwaryax-catalog-1

RUN pip install grpcio grpcio-tools pandas readerwriterlock

WORKDIR /catalog

COPY ./config.py .

COPY ./protos/ .

COPY ./toy.py .

COPY ./catalog_service.py .

COPY ./protos/catalog.proto ./protos/

COPY ./catalog.csv .


RUN python -m grpc_tools.protoc -I protos --python_out=. --grpc_python_out=. protos/catalog.proto

ENTRYPOINT ["python3", "-u", "catalog_service.py"]