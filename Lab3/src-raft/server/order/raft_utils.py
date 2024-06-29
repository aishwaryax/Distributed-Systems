from threading import Thread, Lock
from threading import Lock
import order_pb2
import os

class Utils:
    def run_thread(fn, args):
        thread = Thread(target=fn, args=args)
        thread.daemon = True
        thread.start()
        return thread
    

class CommitLog:
    def __init__(self, server_id):
        self.file = 'commit_log_' + str(server_id) + '.txt'
        self.lock = Lock()
        self.last_index = -1
        self.last_term = 0
        if os.path.isfile(self.file):
            with self.lock:
                with open(self.file, 'r') as f:
                    data = f.readlines()
                    if len(data):
                        self.last_index = len(data) - 1
                        self.last_term = int(data[self.last_index].split(",")[0])


    def write_log(self, term, cmd):
        with self.lock:
            with open(self.file, 'a') as f:
                f.write(f"{term},{cmd}\n")
                self.last_index += 1
            return self.last_index, self.last_term
        
    def get_last_entry(self):
        with self.lock:
            return self.last_index, self.last_term
        
    def get_last_commit(self, last_commit_order):
        index = -1
        with self.lock:
            with open(self.file, 'r') as f:
                data = f.readlines()
                for i in range(len(data) - 1, -1, -1):
                    line = data[i]
                    cmd = line.strip().split(",")[1]
                    order_no = cmd.split("|")[0]
                    if int(order_no) == last_commit_order:
                        return i
        return index
    
    def truncate(self, start):
        with self.lock:
            with open(self.file, 'r+') as file:
                lines = file.readlines()
                file.seek(0)
                file.truncate()
                file.writelines(lines[:start])
        
    def rewrite_log(self, start, commands, term):
        index = 0
        i = 0
        with self.lock:
            with open(self.file, 'r+') as f:
                if len(commands) > 0:
                    while i < len(commands):
                        if index >= start:
                            f.write(f"{term},{commands[i]}\n")
                            i += 1
                            if index > self.last_index:
                                self.last_index = index
                        index += 1
                    f.truncate()
            return self.last_index, self.last_term
        
    def read_logs(self, start=0, end=None):
        with self.lock:
            output = []
            index = 0
            with open(self.file, 'r') as f:
                for line in f:
                    if index >= start:
                        term, cmd = line.strip().split(",")
                        output.append(order_pb2.LogEntry(Term=int(term), Command=cmd))
                    index += 1
                    if end and index > end:
                        break
            return output
    