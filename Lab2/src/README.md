## Team Members' Contributions

1) Aishwarya Sahoo - Implemented Catalog and HTTP Service. Parts of Docker Containerization and Docker-Compose
2) Mitalee Minde - Implemented Client and Order Service. Parts of Docker Containerization and Docker-Compose
#### Part 3 was done by both.

## Folder structure

-src
  |- client
  |- frontend
    |- http_service.py
    |- DockerFile (frontend)
  |- server
    |- catalog
        |- catalog_service.py
        |- unit_test.py
        |- DockerFile (catalog)
    |-order
        |- order_service.py
        |- unit_test.py
        |- DockerFile (order)
  |- test
    |- test.sh //will run the above unit test cases in server/catalog and order/catalog
-docker-compose.yml
## Part 1 
### 1. To run all the three services locally without docker containers, simply run the runAll.sh file using command:
```bash
sh runAll.sh
```
Before running, set the following environment files in the `runAll.sh` file.

The HTTP_SERVER environment variable determines the host of the HTTP service. This needs to be in src/frontend, src/client path.
The CATALOG_SERVER environment variable determines the host of the catalog microservice. This needs to be in src/frontend, src/server/catalog, src/server/order paths.
The ORDER_SERVER environment variable determines the host of the order microservice. This needs to be in src/frontend, src/server/order paths.

If environment variables can not be set, change the respective server hostnames in the config files available within server/catalog, server/order, frontend and client directory.

### 2. Although the gRPC files have been provided they can also be generated using the following commands: 

```bash
pip install -r requirements.txt
```

#### Within src/server/catalog run:
```bash
python -m grpc_tools.protoc -I protos --python_out=. --pyi_out=. --grpc_python_out=. protos/catalog.proto
```

#### Within src/server/order run - 
```bash
python -m grpc_tools.protoc -I protos --python_out=. --pyi_out=. --grpc_python_out=. protos/catalog.proto
python -m grpc_tools.protoc -I protos --python_out=. --pyi_out=. --grpc_python_out=. protos/order.proto
```

#### Within src/front-end run:
```bash
python -m grpc_tools.protoc -I protos --python_out=. --pyi_out=. --grpc_python_out=. protos/catalog.proto
python -m grpc_tools.protoc -I protos --python_out=. --pyi_out=. --grpc_python_out=. protos/order.proto
```

### 3. Navigate to the src/server/catalog directory and run the following command to start the catalog service
```bash
python3 catalog_service.py
```

### 4. Navigate to the src/server/order directory and run the following command to start the order service
```bash
python3 order_service.py
```

### 5. Navigate to the src/frontend directory and run the following command to start the frontend service
```bash
python3 frontend.py
```

## Running the client

### Once the appropirate environment variables or the server hostnames have be set and the services have been started, modify the NUM_OF_REQUEST and PROBABILITY parameters as desrired in config file present in src/client directory


### Run the following command to start the client from the src/client directory
```bash
python3 client.py <Client Id>
```

### In order to launch more than one concurrent client, a bash script has been provided in the src/client directory which can be run as follows 
```bash
sh scheduler.sh <Number of clients>
```

### The output of these clients will be available inside the src/client/output_files directory

## Part 2
### 1. Ensure that the hostnames for catalog, order and frontend services are set to catalog, order and frontend respectively within each config file. 

### 1. To build images for the 3 services using docker-compose, a bash file has been provided in the root folder which can be run as follows
```bash
sh build.sh
```

### 2. To stop and remove the running containers, run the following command
```bash
docker-compose down
```

## Running Testcases

### 1. Navigate to src/test directory and run the following command
```bash
sh test.sh
```