# Client-Server

Project by courses: write a client-server application
The client and the server communicate with each other using a simple text protocol over TCP sockets. The text protocol has the main advantage - visibility, you can view the dialogue between the client and server side without using additional tools.

An example of server-client interaction.

For clarity, we consider the interaction protocol between the client and server using a specific example. In the example, we will collect metrics with data on the operation of the operating system: cpu (processor load), usage (memory consumption), disk_usage (hard disk space consumption), network_usage (network interface statistics). Such data may be needed to control server load and forecast the expansion of the company's hardware fleet - in other words, for monitoring.

What data will we store?

For each metric (<key>), we will store data about its values ​​(<value>) and the time when the measurement was made (<timestamp>). Since, in real life, there can be several servers, it is necessary to distinguish the data received from different servers (in our example, there are two servers palm and eardrum).
