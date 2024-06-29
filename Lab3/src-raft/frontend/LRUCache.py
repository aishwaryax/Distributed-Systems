import catalog_pb2

class Node:
    def __init__(self, key="", val=None, nex=None, pre=None):
        self.key = key  # Initialize node's key
        self.val = val  # Initialize node's value
        self.next = nex  # Initialize reference to the next node
        self.prev = pre  # Initialize reference to the previous node

    def delete(self):
        # Delete the node by updating the next and prev references of neighboring nodes
        self.prev.next = self.next
        self.next.prev = self.prev

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity  # Set the maximum capacity of the cache
        self.cache = {}  # Initialize the cache as an empty dictionary
        self.old, self.new = Node(), Node()  # Create two sentinel nodes
        self.old.next = self.new  # Link old to new sentinel node
        self.new.prev = self.old  # Link new to old sentinel node
    
    def append(self, node):
        newest = self.new.prev  # Get the newest node before the sentinel node
        newest.next = node  # Update next reference of the newest node
        node.prev = newest  # Update prev reference of the node
        node.next = self.new  # Update next reference of the node to new sentinel
        self.new.prev = node  # Update prev reference of new sentinel to the node
        self.cache[node.key] = node  # Add node to the cache

    def get(self, key: str) -> catalog_pb2.QueryResponse:
        if key in self.cache:
            node = self.cache[key]  # Get the node from cache
            node.delete()  # Move the node to the end (MRU) by deleting and appending
            self.append(node)
            return node.val  # Return the value associated with the key
        else:
            return None  # Return None if key is not found in cache

    def put(self, key: str, value: catalog_pb2.QueryResponse) -> None:
        if key in self.cache:
            self.cache[key].delete()  # Delete the existing node if key is found
            del self.cache[key]  # Remove the key from cache
        if len(self.cache) >= self.capacity:
            oldest = self.old.next  # Get the oldest node from cache (LRU)
            oldest.delete()  # Delete the oldest node
            del self.cache[oldest.key]  # Remove the key from cache
        node = Node(key, value)  # Create a new node
        self.append(node)  # Append the new node to the end (MRU) of cache

    def clear(self, key: str) -> None:
        if key in self.cache:
            self.cache[key].delete()  # Delete the node associated with the key
            del self.cache[key]  # Remove the key from cache

    def print_all_values(self):
        for node_key, node in self.cache.items():
            print(f"Key: {node_key}, Value: {node.val}")  # Print all key-value pairs in cache
