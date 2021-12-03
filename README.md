# Python_Port_Scanner

**Alright. Day 1** - a TCP port scanner. Well, python is fun, so let's give it a shot. 

We're dealing with network connections, so we will need to import the socket module

```Python
import socket
```

Sockets are found everywhere and are the method that most networked devices communicate. For futher details check out [this link](https://docs.python.org/3/library/socket.html)

That info aside, let's get to some code:

For now let's only focus on a single remote host:

```Python
#Prompt user for the ip address
remotehost = input("Enter the IP to scan: ")
```

For now we'll also only scan ports 1-1024:

```Python
for port in range(1,1025):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        res = sock.connect_ex((remotehost, port)) #Returns 0 if connection is successful
        if res == 0:
            print(f"Port {port}:        Open")
        sock.close
```

Let's take a look at
```Python
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```
This is the basic syntax for creating a socket (connection)
- AF_INET - Indicates an IPv4 type of connection
- SOCK_STREAM - Indicates a TCP type of connection

Let's give it a try!

```
Enter the IP to scan: 192.168.18.132
Port 22:        Open
```

## It was a success! ...but there is a problem. It's incredibly slow. If you've ever used Nmap you'll recognize just how slow our port scanner is so far. Feel free to interrupt the program execution with Ctrl+C 

## Let's add a timeout on the connection to speed things up

```Python
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1) #<------ Add this line
        res = sock.connect_ex((remotehost, port)) #Returns 0 if connection is successful
```

When we run this we'll see that there is a difference in speed, but that it's still significantly slower than any commonly used scanner

## Perhaps we could use hyperthreading? 

We'll need to import a few modules, so add the following to your imports.
```Python
import threading
from queue import Queue
```

Let's go ahead and clean up our code before we start implementing any functional changes. Let's take an OOP approach:

After a bit of tidying up and a function definition, your code should now look like this:

```Python
import socket
import threading
from queue import Queue
import sys
from datetime import datetime as dt

#Prompt user for the ip address
remotehost = input("Enter the IP to scan: ")

print("-" * 60 + f"\nPlease wait. Scanning the remote host: {remotehost}\n" + "-" * 60)

# A function to scan a single port
def scanport(remotehost, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1)
        res = sock.connect_ex((remotehost, port)) #Returns 0 if connection is successful
        sock.close
        return res
    except socket.error:
        print("Error connecting to remote host")
        sys.exit()

for port in range(1,1025):
    if(scanport(remotehost, port) == 0):
        print(f"Port {port}:        Open")
```

### First, we will assign the port range to the queue to ensure they are accessed in order by the threads:

Add the following line to initialize the queue:
```Python
q = Queue()
```

Add the following to add the ports to the queue:
```Python
for port in range(1,1025):
    q.put(port)
```
    
### From this point we have to create a 'scanner' function for our threads. This function will check the queue for the next port number, scan the port, and print the result
```Python
def scanner():
    while not q.empty(): #Scan until out of ports
        port = q.get() #Gets the next item in the queue
        if(scanport(remotehost, port) == 0): #Check if connection was successful
            print(f"Port {port}:        Open")
```

### Now we will define the main driver for our scanner and our multithreading

```Python
def run_portscanner(threads, queue):
    for port in range(1,1025):
        queue.put(port)
    
    thread_list = []

    for num in range(threads):
        thread = threading.Thread(target=scanner) #Identify the function that each thread will run
        thread_list.append(num) #List for thread management

    for thread in thread_list:
        thread.start() #Starts the threaded operation
    
    for thread in thread_list:
        thread.join() #This prevents the parent thread from terminating until the child threads are complete
```

### Alright. Let's see if this works. Let's call our driver function and see the magic happen. 

```Python
run_portscanner(150, q)
```

In this case I assigned 150 threads to the running process. Your system will limit the ammount of threads you can utilize. After running the scanner with a higher number of threads (800 in my case) I found that the output was getting mixed up. This is apparently from multiple threads attempting to access a variable at the same time. 

You can fix this by placing locks on variables. This forces the multithreading to wait until the resource is unlocked to access it. This can be implemented like so:

```Python
printing_lock = threading.Lock()
```
and
```Python
        if(scanport(remotehost, port) == 0): #Check if connection was successful
            with printing_lock:
                print(f"Port {port}:        Open")
```

##Well, that wraps up day one. See the full code in the repo. Feel free to critique and improve!

