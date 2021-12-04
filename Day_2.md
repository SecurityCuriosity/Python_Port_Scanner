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
