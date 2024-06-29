# Part 1 : Setup for socket based stoy store:

One can chnage the following configurations - BUFFER_SIZE, POOL_SIZE, PORT, HOSTNAME, NUM_OF_REQUEST in config file to make the server run on Edlab or change port, thread pool size etc

To run socket server, run the following command on the server machine by navigating to /src/part1
```bash
python3 server.py
```

To run socket client, run the following command on the client machine by navigating to /src/part1
```bash
python3 client.py
```

To run multiple socket clients, run the following command on client machine  by navigating to /src/part1, here <num_of_cliensts> refers to the client we want to run at a time
```bash
./scheduler.sh <num_of_clients>
```


# Part 2 : Setup for gRPC Toy Store Application:

One can change the following configurations - PORT, HOSTNAME, ITERS in `config.py` file to change the port, server hostname or number of requests.

Navigate to the grpc folder `/src/part2`

To install all the packages required for successful run, execute the following command:

```bash
pip install -r requirements.txt
```

To run the server, you need to first compile the protos on the server machine using:

```bash
python3 -m grpc_tools.protoc -I./protos --python_out=. --pyi_out=. --grpc_python_out=. ./protos/route_guide.proto
```

To now run gRPC server, run on the server machine:

```bash
python3 server.py
```

To run gRPC client, run the following command on the client machine. Also, change the hostname in `config.py`, if running server on different machines by navigating to `/src/part2`:

```bash
python3 client.py
```

To run multiple gRPC clients, run the following command on client machine. Also, change the hostname in `config.py`, if running server on different machines by navigating to /src/part2. For example, if running 5 client machines, you can run the following command:

```bash
python3 test.py --clients=5
```
