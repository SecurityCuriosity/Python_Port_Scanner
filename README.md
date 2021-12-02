# Python_Port_Scanner

Alright. Day 1 - a TCP port scanner. Well, python is fun, so let's give it a shot. 

We're dealing with network connections, so we will need to import the socket module
![image](https://user-images.githubusercontent.com/86580417/144463675-011563b7-1c85-409d-90af-f318d3e07f7d.png)

Sockets are found everywhere and are the method that most networked devices communicate. For futher details check out ![link](https://docs.python.org/3/library/socket.html)

That info aside, let's get to some code:

For now let's only focus on a single remote host:

![image](https://user-images.githubusercontent.com/86580417/144465337-37903bbc-68a4-4a89-b643-a2e3e10f1d2e.png)

For now we'll also only scan ports 1-1024:

![image](https://user-images.githubusercontent.com/86580417/144512041-348ebc97-4ea8-47d1-8647-7e96ef205432.png)

