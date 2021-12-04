import socket
import threading
from queue import Queue
import sys
import argparse

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

def run_portscanner(threads, queue, ports):
    for port in ports:
        queue.put(port)
    
    thread_list = []

    for num in range(threads):
        thread = threading.Thread(target=scanner) #Identify the function that each thread will run
        thread_list.append(thread) #List for thread management

    for thread in thread_list:
        thread.start() #Starts the threaded operation
    
    for thread in thread_list:
        thread.join() #This prevents the parent thread from terminating until the child threads are complete

def scanner():
    while not q.empty(): #Scan until out of ports
        port = q.get() #Gets the next item in the queue
        if(scanport(remotehost, port) == 0): #Check if connection was successful
            with printing_lock:
                print(f"Port {port}:        Open")

def parse_arguments(args):
    parser = argparse.ArgumentParser()

    parser.add_argument("-w","--web", help="only scan common web service ports",action="store_true")
    parser.add_argument("-m","--minimum", help="only scan ports 1-1024",action="store_true")
    parser.add_argument("-a", "--all", help="scan all 65535 ports",action="store_true")
    parser.add_argument("-r", "--registered", help="scan all registered ports (1025-49151)",action="store_true")
    args = parser.parse_args()

    return args

def get_range_from_args(args):
    ports = []
    if not args.all and not args.web and not args.minimum and not args.registered:
        ports+=[*range(1,1025)]

    if args.all:
        ports+=[*range(1,65536)]
        return set(ports).sort()

    if args.web:  
        ports+=[80, 8000, 8080, 443, 4443, 4433]
    if args.minimum:
        ports+=[*range(1,1025)]
    if args.registered:
        ports+=[*range(1025,49151)]
        
    ports.sort()
    return ports

def main(argv = []):
    run_portscanner(100, q, get_range_from_args(parse_arguments(argv)))

main()