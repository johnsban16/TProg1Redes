###### Project 1
---
# TCP implementation over UDP connection in Python
### University of Costa Rica
#### Computer Networks
---

Implementation of a reliable transmission TCP protocol over an UDP connection.

First, run receiver: ```python3 Receiver.py```

Then, run the Sender, especifying the file to be sent: First, run receiver: ```python3 Sender.py file```


### Test with mininet

install mininet

sudo apt install mininet

sudo mn --custom topo.py --topo mytopo --link tc
xterm h1 h2
h1 sender
h2 receiver

Python version: 3.3
