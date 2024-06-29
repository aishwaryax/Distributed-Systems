## Team Members' Contributions

1) Aishwarya Sahoo - New GET orders API, Caching, Synchronization, RAFT implementatoon
2) Mitalee Minde - Replication, Fault Tolerance, Hosting on AWS, Testing and Evaluation

Documentation was done by both.

## Folder structure
```
-src
  |- client
  |- frontend
    |- http_service.py
    |- unit_test.py
  |- server
    |- catalog
        |- catalog_service.py
        |- unit_test.py
    |-order
        |- order_service.py
        |- unit_test.py
  |- test
    |- test.sh //will run the above unit test cases in server/catalog and order/catalog
```
#### A) RUNNING LOCALLY

#### 1. Before running the services, ensure server hostnames in the config files available within each service directory and client directory are correctly set to '127.0.0.1'

#### 2. Although the gRPC files have been provided they can also be generated using the following commands - 

##### Within `src/server/catalog` run - 
1) `python -m grpc_tools.protoc -I protos --python_out=. --grpc_python_out=. protos/catalog.proto`

##### Within `src/server/order` run - 
1) `python -m grpc_tools.protoc -I protos --python_out=. --grpc_python_out=. protos/catalog.proto`
2) `python -m grpc_tools.protoc -I protos --python_out=. --grpc_python_out=. protos/order.proto`

##### Within `src/front-end` run - 
1) `python -m grpc_tools.protoc -I protos --python_out=. --grpc_python_out=. protos/catalog.proto`
2) `python -m grpc_tools.protoc -I protos --python_out=. --grpc_python_out=. protos/order.proto`

#### 3. A run.sh script has been provided in src folder to run the catalog service, 3 instances of order service and the front-end service

##### Run the following command to start all the services WITH CACHING
`./run.sh`

#### 4. Order services will be running on ports 56365, 56366, 56367, catalog service on port 56361 and front-end service on 56363. All these services can be suspended as desired.

#### 5. To run multiple clients client simply go to client folder and run below command
`./scheduler.sh <number of clients>`

#### 6. If you want to run only 1 client the run
`python3 client.py 1`

#### 7. If you want no caching then comment out few lines of code present in http_service.py, productBL.py -> find below lines
In http_service.py comment `self.bl.clear_cache(names)` and in productBL.py comment [these lines](frontend/productBL.py)


#### B) AWS Deployment and testing on EC2

##### Creating m5a.large instance

`aws ec2 run-instances --image-id ami-0d73480446600f555 --instance-type m5a.large --key-name vockey > instance.json`


##### Getting public DNS

`aws ec2 describe-instances --instance-id i-02a804874316a7f72`

##### Giving access to pem file

`chmod 400 labsuser.pem`

##### Authorize port 22 (used by ssh) in the default security group

`aws ec2 authorize-security-group-ingress --group-name default --protocol tcp --port 22 --cidr 0.0.0.0/0`

##### Authorize port 56363 (used by ssh) in the default security group

`aws ec2 authorize-security-group-ingress --group-name default --protocol tcp --port 56363 --cidr 0.0.0.0/0`

##### Ssh into server
`ssh -i labsuser.pem ubuntu@ec2-3-238-172-217.compute-1.amazonaws.com`



##### Commands to install python 3.0
1. `sudo apt update`
2. `sudo apt install python3-pip`
3. `pip3 install --upgrade pip`
4. `sudo apt-get install bash`
5. `sudo add-apt-repository ppa:deadsnakes/ppa`
6. `sudo apt-get update`
7. `sudo apt install build-essential zlib1g-dev \libncurses5-dev libgdbm-dev libnss3-dev \ libssl-dev libreadline-dev libffi-dev curl software-properties-common`
8. `wget https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tar.xz`
9. `tar -xf Python-3.9.0.tar.xz`
10. `cd Python-3.9.0`
11. `./configure`
12. `sudo make altinstall`
13. `sudo update-alternatives --config python3.9`
14. Test the python version `python3.9 -V`
15. `cd  /usr/lib/python3/dist-packages`
16. `ls -la /usr/lib/python3/dist-packages`
17. `sudo cp apt_pkg.cpython-36m-x86_64-linux-gnu.so apt_pkg.so`
18. `cd ~`
19. `sudo apt install python3.9 -distutils`
20. `pip3 install --upgrade setuptools`
21. `pip3 install --upgrade pip`
22. `pip3 install --upgrade distlib`