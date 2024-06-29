import threading
import subprocess
import argparse

def run_script(script_name):
    subprocess.run(["python3", script_name])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument('--clients', default = 1, type=int, help="number of client processes to be run")
    args = parser.parse_args()

    clients = int(args.clients)
    script_threads = []
    for _ in range(clients):
        script_threads.append(threading.Thread(target=run_script, args=("client.py",)))
    for script_thread in script_threads:
        script_thread.start()
    for script_thread in script_threads:
        script_thread.join()