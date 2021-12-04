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

# Alright! Hopefully that all works for you. Check the Day_1.5-Port_Scanner.py if you have issues. 



