## Welcome back! Hopefully the previous day's code wasn't too terrible. 

First things first, I'd like to add a couple of improvements to yesterday's code before we move on. 

### Let's add the functionality to scan wider ranges of ports and to specify some command line parameters

#### First we'll add a function to collect command line argument. This will be our new main driver:

```Python
def main(argv = []): #Accepts commandline parameters and defaults to empty list if none
```
#### Next we need to add the functionality to handle these arguments. We'll use the argeparse module

```Python
import argparse
```
#### Now let's define a function to parse the arguments passed over the cli
```Python
def parse_arguments(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("-w","--web", help="only scan common web service ports",action="store_true")
    parser.add_argument("-m","--minimum", help="only scan ports 1-1024",action="store_true")
    parser.add_argument("-a", "--all", help="scan all 65535 ports",action="store_true")
    parser.add_argument("-r", "--registered", help="scan all registered ports (1025-49151)",action="store_true")
    args = parser.parse_args()
    return args
```

There's a bit to unpack here, but let's give it a shot:
- The 'parser' is a structure provided by argeparse of the 'ArgumentParser' type. It does what it sounds like...manages the possible arguments that can be 
passed to the program.....really seems like this should have been called 'manager', but whatever. This is the cool feature that let's you add a '-h' to see
all of the possible command line arguments
- We have to define each possible argument that can be passed, otherwise everything will return an 'unknown argument' error. We do this with 'add_argument'
- We then define the short form '-w', the long form '--web', and what shows up in the help section (help="scan all 65535 ports")
- The 'action' determines if the parser will store 'True' or 'False' if the argument is present. This is important later for checking if an argument is present

#### Next up we will create a function to build out our port list from the passed arguments: 
```Python
def get_range_from_args(args):
    print(args)
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
```
#### We are passing out arguments as a parameter and adding ports to a list depending on what arguments are present. Pretty straightforward. Now we'll make a slight adjustment to our run_portscanner() function:

```Python
def run_portscanner(threads, queue, ports):
    print(type(ports))
    for port in ports:
        queue.put(port)
    
    thread_list = []
```

#### Lastly we'll go back to our main() function

```Python
def main(argv = []):
    run_portscanner(100, q, get_range_from_args(parse_arguments(argv)))

main()
```

## Alright! Hopefully that all works for you. Check the Day_1.5-Port_Scanner.py if you have issues. 


## Now let's get to our new functionality - Banner Grabbing! 

#### The socket module has a recv method that captures a certain number of bytes to receive from the socket. We should probablly use that.

The socket method that we used before, **socket.connect_ex** is faster, but it does not play as nicely on some connections (not 100% sure why...need to investigate). So, we're going to build a new funtion that will connect using the the **socket.connect** function. 
```Python
def bannergrab(remotehost, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2.0)
    try:
        sock.connect((remotehost, port))
        sock.send('Test\r\n'.encode())
        banner = (sock.recv(1024)).decode('utf-8')
        sock.close()    
    except socket.error as error:
        print(error)
        sys.exit()
    return banner
```

Most of what we have here is similar to our previous **scanport()** function. With the exception of:
```Python
        sock.connect((remotehost, port))
        sock.send('Test\r\n'.encode())
        banner = (sock.recv(1024)).decode(errors="ignore")
```
For this we are using **socket.connect()** instead of **socket.connect_ex()**. Both will owrk, but i was noticing some oddities when connecting to services like SSH when using **connect_ex()**. 

**sock.send()** is our first new addition. This send whatever is passed as an argument to the port on the receiving end of the connection. This output needs to be converted to bytes before sending. This is accomplished through the **encode()** function (this defaults to UTF-8 encoding. Other encoding schemes can be specified.)

The socket then awaits for a response. The response can be accessed with **sock.receive()** the **1024** specifies the maximum number of bytes to receive. Since this is received as bytes it must be decoded through the **decode()** command. This defaults to UFT-8 as well. We may receive other types of input and the UTF-8 codecs would not be able to decode it. So, instead of filling our screen woth errors, we can add **errors="ignore** asa parameter to decoed(). 

### Need to make sure the bannergrabbing only runs when a port is active. We can use our **scanner()** method to accomplish this. 
```Python
def scanner():
    while not q.empty(): #Scan until out of ports
        port = q.get() #Gets the next item in the queue
        r = scanport(remotehost, port)
        if( r == 0): #Check if connection was successful
            with printing_lock:
                print(f"Port {port}:        Open", end="")
                b = bannergrab(remotehost, port)
                print("\t\t", b)
```

You can see in the code snippet above that we've added the following two lines:
```Python
                b = bannergrab(remotehost, port)
                print("\t\t", b)
```

We only want the banner grabbing function to run when there is a successful connection, so we wait for a successful connection. This is indicated by the fucntion existing under the **if( r == 0): ** statement. 

### That wraps up the banner grabbing portion. Run your code, and see if you get the expected output. Something like this:
```
Port 22:        Open             SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.3
```

### See Day_2-Port_Scanner.py for any clarification 


