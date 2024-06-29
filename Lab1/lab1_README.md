[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/Nj4Di-xo)
Compsci 677: Distributed and Operating Systems

Spring 2024

# Lab 1: Asterix and the Online Toy Store

## Goals and Learning Outcomes

This lab has the following learning outcomes with regard to concepts covered in class.

1) Learn to design distributed client-server applications
2) Learn to design a concurrent networked server application
3) Learn to design your own thread pool for servers and use thread pool abstractions provided by
   major languages
4) Learn to design distributed applications using a low-level abstraction of socket communication as
   well as a high-level abstraction of remote procedure calls.

The lab also has the following learning outcomes with regard to practice and modern technologies.

5) Learn to use gRPC, a modern RPC framework
6) Learn to measure the performance of a distributed application
7) Learn to use version control and build tools

## Instructions

1) You may work in groups of two for this lab. If you decide to work in groups, you should briefly
   describe how the work is divided between the two team members in your README file.
2) You can use either Python or Java for this assignment.
3) Use the following team naming format when you create your team on GitHub: spring24-lab1-GitHubid1-Githubid2. For example, spring24-lab1-alice-bob for a group of two. For a single group team, use spring24-lab1-alice as an example team name for a student with github id alice. If you already chose a different format for your team, edit your team name to the above format. 
4) Do's and don'ts:
   - discuss lab with other students: allowed
   - use of AI tools: allowed with attribution (be sure to read the policy in the course syllabus)
   - use code from others/Internet/friends/coders for hire: disallowed
   - ask TAs for clarifications/help: always allowed

## Lab Description

The year is 50 B.C.  The Gauls, led by Asterix, have decided to upgrade their village store. Asterix and Obelix
plan to deploy an online store, the first of its kind in their village, where fellow Gauls can shop from the comfort of their homes and have 
orders delivered by carrier pigeons (drone delivery is yet to be invented). Every Gaul has a smart stone tablet (not to be confused with a smartphone or tablets, which are also yet to be invented) that allows them to look up their favorite products and place an order. 

This lab has three parts (two programming parts and one performance measurement/evaluation part). In
the first part, you will design your own thread pool and use it to write a simple client-server
application that uses network sockets. This part will give you an appreciation of how thread pools
work internally. In the second part, you will use gRPC and built-in thread pool mechanisms to write
the client-server application. This part will give you an appreciation of using modern frameworks to
write distributed applications since most programmers simply use higher-level abstractions such as
built-in thread pools and RPCs rather than implementing their own thread pool or using lower-level
abstractions such as sockets.

## Part 1: Implementation with Socket Connection and Handwritten Thread Pool

In this part, you need to implement Asterix's online Toy store as a socket-based client-server application.

The server component should implement a single method Query, which takes a single string argument
that specifies the name of the toy. The Query method returns the dollar price of the item (as a
floating point value, such as 25.99) if the item is in stock. It returns -1 if the item is not found
and 0 if the item is found but not in stock.

The client component should connect to the server using a socket connection. It should construct a
message in the form of a buffer specifying the method name (e.g., string "Query") and arguments
("toyName"). The message is sent to the server over the socket connection. The return value is
another buffer containing the cost of the item or an error code such as -1 and 0, as noted above.

The village server hosts the world's smallest toy store that sells only two items: (i) Tux and (ii) Whale,
both stuffed animals for Linux and Docker fans. It maintains a product catalog that includes these
items, the current price of each item, and the number of items in stock in an in-memory data structure
(this part does not require a database backend for your store application's product catalog).

The server should listen on a network port of your choice (e.g., a high port number such as 8888),
accept incoming client requests over sockets, and assign this request to an idle thread in the
thread pool. The main part of the assignment is to implement your own ThreadPool. The thread
pool should create a static number of threads that is configurable at start time, and these threads
wait for requests. The main server thread should accept requests over a socket, insert them into
a request queue, and notify the thread pool, which causes one of the idle threads to be assigned this
request for processing. Your design should include the request queue, threading code for the thread
pool, and any synchronization needed to insert or remove requests from the queue and notify threads.

The client should be a for-loop that sequentially issues query requests to the server. You design
should be able to use multiple client processes to make concurrent requests to the server, thereby
exercising the thread pool.

Design notes: 
- You are not allowed to use a ThreadPool framework that is available by the language/libraries
and should implement your own threading pool.

- You should also implement your own synchronization code (using locks, semaphore, or other suitable primitive)
  to ensure thread safety when adding or removing requests from the request queue. For example, you are not allowed
  to use a thread-safe queue library, which does this synchronization automatically for you.

- You are allowed to look at sample implementations of thread pools that are available on the
Internet, but in the end, your code should be your own work and not include snippets of code
written by others. We have a comprehensive list of sample implementations that can be found on the
Internet and will be strictly checked for violations of this policy. If you read some docs or
looked at code found on the Internet, please credit all such sources by listing them in a Reference
section.

## Part 2: Implementation with gRPC and Built-in Thread Pool

In this part, you need to implement the online Toy store using gRPC and a built-in thread pool
support.

The server component should implement two gRPC calls: 
   1. `Query(itemName)`  which takes the string
ItemName and returns the cost of the item and real-time stock indicating how many are in stock. 
   2. `Buy(ItemName)` which buys the item and reduces the stock of that item by 1. The method returns 1 if
the call succeeds, 0 if the item is not in stock and -1 if an invalid item name is specified.

You should use protobuf to create appropriate message structures for arguments and return values of
both calls and design rpc methods as noted above. The product catalog should be expanded to four
stuffed animals. In addition to Tux and Whale, the catalog should also include elephant (for PHP
enthusiasts) and dolphin (for MySQL fans).

Implement your gRPC server using a built-in thread pool. You do not need to write your own thread
pool and should instead use a built-in dynamic thread pool support. Since the thread pool is
dynamic, set an appropriate max limit on the maximum number of concurrent RPCs when you start your
server. Use appropriate synchronization methods on the product catalog since querying and buying
will read from and write to the catalog, which makes it a shared data structure. The product catalog
can be maintained in memory, and no database backend is needed for this lab. Implement appropriate
error/exception handling as needed for your design (for example, an item may be in stock when
queried, but stock may run out by the time the client sends a buy request)

The client component should use gRPC to make queries and buy calls to the server. The client can be a
for loop that sequentially issues either buy or query requests. Your design should be able to allow multiple
client processes to make concurrent requests to the server, thereby exercising the thread pool.

## Part 3: Evaluation and Performance Measurement

For each part, perform a simple load test and performance measurements. The goal here is to understand
how to perform load tests on distributed applications and understand performance. Deploy more than
one client process and have each one make concurrent requests to the server. The clients should
be running on a different machine than the server (use the EdLab, if needed). Measure the latency
seen by the client for different types of requests, such as query and buy.

Vary the number of clients from 1 to 5 and measure the latency as the load increases. Make simple
plots showing the number of clients on the X-axis and response time/latency on the Y-axis. Be sure to
show the response times of query and buy requests separately for part 2.

Using these measurements, answer the following questions:

1) How does the latency of Query compare across Part 1 and Part 2? Is one more efficient than the
   other?
2) How does the latency change as the number of clients (load) varies? Does a load increase
   impact response time?
3) How does the latency of the query compare to the buy? You can measure the latency of each by having clients
   only issue query requests and only issue buy requests and measure the latency of each separately.
   Does synchronization play a role in your design and impact the performance of each? While you are not
   expected to do so, the use of read-write locks should ideally cause query requests (with read locks)
   to be faster than buy requests (which need write locks). Your design may differ, and you
   should observe if your measurements show any differences for query and buy based on your design.
4) In part 1, what happens when the number of clients is larger than the size of the static thread pool?
   Does the response time increase due to request waiting?

## What to submit.

1) Your solution should contain source code for both parts separately. Inside the `src` directory,
   you should have two folders named "part1" and "part2" for the two parts. Submit your code with
   good inline comments.

2) Submit the following additional documents inside the `docs` directory. 1) A Brief design document
   (1 to 2 pages) that explains your design choices (include citations if you used or referred to
   Internet sources), 2) An Output file (1 to 2 pages), showing sample output or screenshots to
   indicate your program works, and 3) An Evaluation doc (2 to 3 pages), for part 3 showing plots
   and making observations.

3) Submit all of the above via GitHub Classroom. Include a README at the top level explaining how to
   build and run your code on Edlab (if we can not run it, we can not grade it). It's recommended to
   use a build tool and include your build file in the repo if you are using Java (e.g., gradle or
   Maven). For Python, it's optional to use a build tool, but `requirements.txt` should be included if your code has external dependencies.

4) Your GitHub repo is expected to contain many commits with proper commit messages (which is good
   programming practice). Use GitHub to develop your lab and not just to submit the final version.
   We expect a reasonable number of commits and meaningful commit messages from both members of the
   group (there is no "target" number of commits that is expected, just enough to show you are using
   GitHub as one should).

Notes:
 -  Since this is a graduate class, we assume you know how to write a good design doc. Writing proper technical descriptions to discuss the details
   of your system is an important aspect of designing systems. To see some examples, please refer to https://www.designdocs.dev/library
   for how well-known open-source projects provide good design docs. We strongly suggest using a format such as the one in
   https://github.com/aws/eks-anywhere/blob/main/designs/single-node-cluster.md to write your design doc, and it should include
   sections such as Introduction, Objective, Solutions overview/architecture, APIs, Testing, List of known issues/Alternatives, etc.

## Grading Rubric

1) Part 1 and Part 2 are each 42.5% of the lab grade.

   For full credit:

   * Source code should build and work correctly (20%)
   * A design doc should be submitted (7.5%)
   * Code should have in-line comments (5%)
   * An output file should be included (5%)
   * GitHub repo should have adequate commits and meaningful commit messages (5%).

3) Part 3 is 15% of the grade.

   For full credit:

   * Eval document should be turned in with measurements for Part 1 and 2 (shown as plots where
     possible and tables otherwise) (7.5%)
   * Explaining the plots by addressing answers to the 4 questions listed in Part 3 (7.5%).

Late policy will include 10% of points per day. Medical or COVID exceptions require advance notice
and should be submitted through Piazza (use exceptionrequests folder in Piazza). Three free late days
per group are available for the entire semester - use them wisely and do not use them up for one lab
by managing your time well.

## References

- Who are the Gauls? https://en.wikipedia.org/wiki/Asterix
- Tutorial to gRPC in Python https://grpc.io/docs/languages/python/basics/
- Tutorial to gRPC in Java https://grpc.io/docs/languages/java/basics/
- Learn about Git and GitHub https://docs.github.com/en/get-started/using-git/about-git
- Learn about Python's built-in threadpool https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor
- Learn about Java's built-in threadpool https://docs.oracle.com/javase/tutorial/essential/concurrency/pools.html


