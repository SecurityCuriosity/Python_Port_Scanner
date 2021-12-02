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

# It was a success! ...but there is a problem. It's incredibly slow. If you've ever used Nmap you'll recognize just how slow our port scanner is so far. Feel free to interrupt the program execution with Ctrl+C 
