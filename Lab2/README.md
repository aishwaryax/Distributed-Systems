[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/xFRBl5c9)
Compsci 677: Distributed and Operating Systems

Spring 2024


# Lab 2: Asterix and Tiered Microservices-Based Toy Store

 

## Information about your submission
1. Name and email: Mitalee Minde - mminde@umass.edu
2. Team member name and email: Aishwarya Sahoo - absahoo@umass.edu
3. Number of late days used for this lab: 2
4. Number of late days used so far including this lab: 2

Please note : Readme is present in src folder

## Goals and Learning Outcomes

This lab has the following learning outcomes with regard to concepts covered in class.
1. Design distributed server applications using a multi-tier architecture and microservices.
2. Design virtualized applications.
3. Design interfaces for web applications.

The lab also has the following learning outcomes with regard to practice and modern technologies.
1. Learn how to implement a REST API server.
2. Learn to measure the performance of a distributed application.
3. Learn how to use Docker to containerize your micro-service and learn to manage an application consisting
   of multiple containers using Docker Compose.
4. Learn how to test a distributed application.

## Instructions

1. You may work in groups of two for this lab. If you decide to work in groups, you should briefly
    describe how the work is divided between the two team members in your README file.  Be sure to list
    the names of all team members at the top of this README file.
2) You can use either Python or Java for this assignment. For this lab, you may use different languages for different
    microservices if you want.
3) Use the following team naming format when you create your team on GitHub: spring24-lab2-GitHubid1-Githubid2. For example, spring24-lab2-alice-bob for a group of two. For a single group team, use spring24-lab2-alice as an example team name for a student with github id alice. If you already chose a different format for your team, edit your team name to the above format. 
4) Do's and don'ts:
   - discuss lab with other students: allowed
   - use of AI tools: allowed with attribution (be sure to read the policy in the course syllabus)
   - use code from others/Internet/friends/coders for hire: disallowed
   - ask TAs for clarifications/help: always allowed




## Lab Description

The year is 50 B.C.  The Gauls, led by Asterix and Obelix, are have had a lot of success with their online store, the first of of its kind 
in all of Gaul. Even the Romans have begun to envy the conveience of receiving orders by carrier pigeon in the comfort of their homes.
To accomodate growing demand, Asterix has decided to scale up their implementation by adopting a modern and scalable architecture.


To do so, in this lab, we will extend the toy store application that you implemented in the first lab. 
Instead of using a monolithic server, we will now employ a two-tier design for the Toy Store (a front-end tier and a
back-end tier) using microservices at each tier. The front-end is implemented as a single
microservice, while the back-end is implemented as two separate services: a catalog service and
an order service.

Note: You are not required to use any code from Lab 1, but please feel free to use any parts of lab 1 for lab 2 if it is useful to you.

## Part 1: Implement Your Multi-Tiered Toy Store as Microservices

### Front-end Service

The clients can communicate with the front-end service using the following two HTTP-based REST APIs.
In an HTTP-based REST API, a client sends its request as an HTTP request and receives a reply as an HTTP response.
We will use HTTP GET and POST requests to send requests to the server. The server supports Query and Buy requests, like in Lab 1, but these are sent as HTTP REST requests as follows.  

1. `GET /products/<product_name>`

    This API is used to query the details of a product. If the query is successful, the server
    should return a JSON reply with a top-level `data` object. Similar to lab 1, the `data` object
    has three fields: `name`, `price`, and `quantity`. For instance,

    ```json
    {
        "data": {
            "name": "Tux",
            "price": 15.99,
            "quantity": 100
        }
    }
    ```

    If things go wrong, for example, if the product name provided by the client does not exist, the
    front-end service should return a JSON reply with a top-level `error` object. The `error` object
    should contain two fields: `code` (for identifying the type of the error) and `message` (human-readable explanation of what went wrong). For instance,

    ```json
    {
        "error": {
            "code": 404,
            "message": "product not found"
        }
    }
    ```

2. `POST /orders`

    This API will try to place an order for a certain product. The client should attach a JSON body
    to the POST request to provide the information needed for the order (`name` and `quantity`).

    ```json
    {
        "name": "Tux",
        "quantity": 1
    }
    ```

    If the order is placed successfully, the front-end service returns a JSON object with a
    top-level `data` object, which only has one field named `order_number`.

    ```json
    {
        "data": {
            "order_number": 10
        }
    }
    ```

    In case of error, the front-end service returns a JSON reply with a top-level `error` object,
    which has two fields, `code` and `message`, similar to the product query API.

The server should listen to HTTP requests on a socket port  (normally, this would be port 80 for HTTP, but we suggest using a higher-numbered port since your machine may need admin/root privileges to listen on port 80). 
Like before, the server should listen for incoming requests over HTTP and assign them to a thread pool. You can use any builtin thread pool for servicing client requests. Alternatively, you can also use a simple thread-per-request model (or, more precisely, thread-per-session)  to create a thread for each new client. The thread should first parse the HTTP request to extract the GET/POST command. Depending on whether it is a Query or a Buy, it should make a request to the Catalog or Order service, as discussed below. The response from this back-end service should be used to construct a json response as shown in the above API and sent back to the client as an HTTP reply. 


**Note that when implementing the front-end service, you can NOT use existing web frameworks
such as [`Django`](https://github.com/perwendel/spark),
[`Flask`](https://github.com/pallets/flask), [`Spark`](https://github.com/perwendel/spark),
etc.** Web frameworks already implement a lot of the functionality of lab 2 and provide higher-level abstractions to the developer. The goal here is to understand the details, which is why you need to implement them yourself rather than using a web framework.

You'll have to handle the HTTP requests directly in your application or you can implement your own simple web
framework (this is actually not as hard as you may think). Languages such as Python and Java provide HTTP libraries to make this straightforward for you, and you should use them to implement HTTP clients and the front-end service.

If you don't know how to get started on this part, be sure to check out the [FAQ](https://piazza.com/class/ls3nga1lnag6g8/post/152) 
 on Piazza.

### Catalog Service

When the front-end service receives a query request, it will forward the request to the catalog
service. The catalog service needs to maintain the catalog data, both in memory and in a CSV or text
file on disk ("database"). The disk file will persist in the state of the catalog. When the service starts up, it should initialize itself from the database disk file.  In production applications, a real database engine is used for this part, but here we will use a file to maintain the catalog.

You should use all the toys mentioned in lab 1 for the catalog and also add fox (for Mozilla fans) or python (for Python fans) as items for sale.

While query requests will simply read the catalog, buy requests will be sent to the order service, which will then contact the catalog service to update (decrease) the stock of items in the catalog. These updates should be written out to the catalog on disk (immediately or periodically, depending on your design). 
 
The catalog service is implemented as a server that listens to requests from the front-end service or the order 
service. The catalog service exposes an **internal interface** to these two components. As part of this lab, you 
should first design the interface (i.e., list of exposed functions and their inputs/outputs) for the catalog service and clearly describe it in your design doc. You can use  any mechanism of choice to implement the interface for the catalog (e.g., sockets, RPC (e.g., pyro), RMI (e.g., java RMI), gRPC, or HTTP REST). You should describe how you implemented your interface in your design doc.
 
Like the front-end server, you should employ threads to service incoming requests. Since the catalog can be accessed concurrently by more than one thread, use synchronization to protect reads and updates to the catalog. While simple locks are acceptable, we suggest using read-write locks for higher performance. 
 

### Order Service

When the front-end service receives an order request, it will forward the request to the order
service. Obviously, the order service still needs to interact with the catalog service to complete the
order. Specifically, a buy order should succeed only if the item is in stock, and the stock should be decremented.


If the order is successful, the order service generates an order number and returns it to
the front-end service. The order number should be a unique, incremental number, starting from 0.
The order service also needs to maintain the order log (including order number, product name, and
quantity) in a persistent manner. Similar to the catalog service, we will just use a simple CSV or text file
on disk as the persistent storage for the database.

Like in the catalog service, you need to first design the interface exposed by your order service (i.e., a list of functions and their input/outputs). You can use any method for front-end to invoke this interface (e.g., socket, RPC, RMI, REST HTTP). Further, the order service should be threaded and should use synchronization when writing to the order database file.


### Client

The client in this lab works in the following way. First, it opens an HTTP connection with the front-end
service, then it randomly queries an item. If the returned quantity is greater than zero, with
probability $p$ it will send another order request using the same connection. Make $p$ an
adjustable parameter in the range $[0, 1]$ so that you can test how your application performs when
the percentage of order requests changes. A client can make a sequence of queries and (optional) order for each such query based on probability $p$. This sequence of requests is called a session. Your front-end server should use a single thread to handle all requests from the session until the client closes the HTTP socket connection.  Make sure that the thread pool at the server is large enough to handle all active client and their sessions without starving. 

### Communication

We have specified that the front-end service should provide a REST interface to the client, but have asked you to 
design the interfaces exposed by the two backend micro-services.  As noted above, you can use REST API, RPC, RMI, gRPC, raw sockets, etc.  

**Note:** If you make your own message protocol to interact between the client and the server, or send something like "GET /stocks/stocks_name" as the message (because of the example GET /stocks/<stock_name> given in the instructions), know that this is wrong and will result in deducted points.

### Concurrency

It's important that all your microservices can handle requests concurrently. You can use any of the
concurrency models taught in class: thread-per-request, threadpool, async, etc.

## Part 2: Containerize Your Application

In this part, you will first containerize your application code and then learn to deploy all components 
as a distributed application  using Docker. If you are not familiar with Docker, be sure to look at 
lablet 2, which provides a hands-on tutorial. Also, review the references at the end of this file.

First, create a docker file for each of the three microservices that you implemented in part 1. Verify that
they build and run without issue.

After that, write a Docker compose file that can bring up (or tear down) all three services using one
`docker-compose up` (or `docker-compose down`) command.

Note that files you write in a Docker container are not directly accessible from the host, and they
will be erased when the container is removed. Therefore, you should mount a directory on the host as
a volume to the **catalog** and **order** services so that files and output can persist after the containers
are removed.

Another thing to notice is that when you use Docker compose to bring up containers, it will set up a
new network for all the containers, the containers will have a different IP address in this network
than your host IP address. Therefore, you need to consider how to pass the IP/hostnames to the
services so that they know how to locate other services regardless of whether they are running on
"bare metal" or inside containers. (HINT: you can set environment variables when building a Docker
image or in a Docker compose file).

## Part 3: Testing and Performance Evaluation

In this part, you will be testing the functionality and performance of your code.

First, write some simple test cases to verify that your code works as expected. Be sure to test the code and error handling (e.g., by querying items that do not exist or buying items that are out of stock). Testing distributed applications is different from testing a single program. So you should try to test the full application as well as the micro-services. Write a few different test cases and attach the output to show that it worked as expected.  Submit your test cases and the outputs in a test directory.

Second, write some performance/load tests to evaluate the performance of your application. Deploy more than one client process and have each one make concurrent requests to the server. The clients should be running on a different machine than the server (use the EdLab, if needed). Measure the latency seen by the client for different types of requests, such as query and buy.

Vary the number of clients from 1 to 5 and measure the latency as the load goes up. Make simple plots showing the number of clients on the X-axis and response time/latency on the Y-axis. 

Using these measurements, answer the following questions:

1. Does the latency of the application change with and without Docker containers? Did virtualization add any overheads?
2. How does the latency of the query compare to buy? Since buy requests involve all three microservices, while query requests only involve two microservices, does it impact the observed latency? 
3. How does the latency change as the number of clients changes? Does it change for different types of requests?



## What to Submit

At the top of this README file, add the name(s) and umass email address(es) of all the team members.
Also, if you are working in a group, briefly describe how the work is divided.

1. Your solution should contain source code for both parts separately. Inside the `src` directory, you
should have a separate folder for each component/microservice, e.g., a `client` folder for client
code, a `front-end` folder for the front-end service, etc.

2. The docker files and Docker compose files should be placed under the root folder. Also, include a
`build.sh` script that can build all your images. This script should be able to build your images on
Edlab machines.

3. A short README file on how to run your code. Include build/make files if you created any, otherwise the README instructions on running the code  should provide details on how to do so.

4. Submit the following additional documents inside the docs directory. 1) A  design document (2-3 pages) that 
explains your design choices (include citations if you used referred to Internet
sources), 2) An Output file (1 to 2 pages), showing sample output or screenshots to indicate your
program works, and 3) An Evaluation doc (2 to 3 pages) for part 3 showing plots and making
observations.

5. Submit your test cases in the test directory. Attach sample output of test cases on the docs directory.

6. Your GitHub repo is expected to contain many commits with proper commit messages (which is good
programming practice). Use GitHub to develop your lab and not just to submit the final version. We
expect a reasonable number of commits and meaningful commit messages from both members of the group
(there is no "target" number of commits that is expected, just enough to show you are using GitHub
as one should).

Notes:
 -  Since this is a graduate class, we assume you know how to write a good design doc. Writing proper technical descriptions to discuss the details
   of your system is an important aspect of designing systems. To see some examples, please refer to https://www.designdocs.dev/library
   for how well-known open-source projects provide good design docs. We strongly suggest using a format such as the one in
   https://github.com/aws/eks-anywhere/blob/main/designs/single-node-cluster.md to write your design doc, and it should include
   sections such as Introduction, Objective, Solutions overview/architecture, APIs, Testing, List of known issues/Alternatives, etc.

## Grading Rubric

1) Part 1 50% of the lab grade.

    For full credit:

    * Source code should build and work correctly (25%),
    * Code should have in-line comments (5%),
    * A descriptive design doc should be submitted (10%),
    * An output file should be included (5%),
    * GitHub repo should have adequate commits and meaningful commit messages (5%).

2) Part 2 is 30% of the lab grade.

    For full credit:

    * The docker files should build each microservice successfully (15%),
    * The docker-compose file should be able to bring up/tear down the whole application using one
        command (10%),
    * The catalog file and order log file should be persisted after container removal (5%).

3) Part 3 is 20% of the grade.

    For full credit:

    * Eval document should be turned in with measurements for Part 1 and 2 (shown as plots where
        possible and tables otherwise) (10%),
    * Explaining the plots by addressing answers to the 4 questions listed in Part 3 (5%)
    * Test cases and test case output (5%)

For late policy, we will deduct 10% per day. Medical or COVID exceptions require advanced notice
and should be submitted through Piazza (use the exception requests folder in Piazza). Three free late days
per group are available for the entire semester. Use them wisely and do not use them up for one lab
by managing your time well.

## References

1. HTTP protocol: https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol
2. Dockerfile reference: https://docs.docker.com/engine/reference/builder/
3. Compose file reference: https://docs.docker.com/compose/compose-file/
4. Docker volumes: https://docs.docker.com/storage/volumes/
