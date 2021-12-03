import socket
import threading
from queue import Queue
import sys

#Prompt user for the ip address
remotehost = input("Enter the IP to scan: ")
q = Queue()
printing_lock = threading.Lock()

print("-" * 60 + f"\nPlease wait. Scanning the remote host: {remotehost}\n" + "-" * 60)

# A function to scan a single port
def scanport(remotehost, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.0)
        res = sock.connect_ex((remotehost, port)) #Returns 0 if connection is successful
        sock.close
        return res
    except socket.error:
        print("Error connecting to remote host")
        sys.exit()

def scanner():
    while not q.empty(): #Scan until out of ports
        port = q.get() #Gets the next item in the queue
        if(scanport(remotehost, port) == 0): #Check if connection was successful
            with printing_lock:
                print(f"Port {port}:        Open")

def run_portscanner(threads, queue):
    for port in range(1,1025):
        queue.put(port)
    
    thread_list = []

    for num in range(threads):
        thread = threading.Thread(target=scanner) #Identify the function that each thread will run
        thread_list.append(thread) #List for thread management

    for thread in thread_list:
        thread.start() #Starts the threaded operation
    
    for thread in thread_list:
        thread.join() #This prevents the parent thread from terminating until the child threads are complete

run_portscanner(800, q)
