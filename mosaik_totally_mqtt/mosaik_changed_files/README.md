This are the files needed for the application to run in the desired mode. You can choose to replace the original in your Python folder or 

Mosaik_api : I changed the class Simulator to add a MQTT client inside. The client is therefore present in every subclass and ready to 
receive messages since the __init__ call.
Since the simulator in the beginning doesn't know the name he will be given by mosaik, it communicates to mosaik it's IP:PORT, which becomes
(treated like a string) a temporary topic. In this topic the simulator will receive the init call, know his true name and then subscribe to 
the topic on which he will listen until the end of simulation.

simmanager : I created a new class FakeProxy, it contains all the attributes of a mosaik Proxy, except for the TCP socket. I used this to avoid
changing the whole code. When mosaik recognises a simulatore wants to communicate only trought MQTT he will create a FakeProxy, but will treat
it almost as a normal Proxy.
In start call i check if the simulator wants to connect to mosaik by MQTT (that is if the method in SIM_CONFIG is "connect"). If it does then
a new instance of FakeProxy is created, else the simulation run normally.

scheduler : I changed step and get_data in sim_process. They no more run using yield, but instead have a semaphore inside them that waits for 
MQTT messages to be exchanged.
Also I wrote some if statements to check Proxy types and make FakeProxy have a different treatment.

scenario : Added a MQTT client in class World. Since the beginning it is subscribed to all topics (TODO it should be better to change it's 
topic from "#" to something like "mosaik/#", since in the first case all the messages mosaik publishes are sent back to him, possibly causing
traffic on the network.


WARNING:
this implementation using only mqtt come with 2 major costs:
1)as for now all the simulators can only use MQTT, no hybrid protocol is permitted;
2)the program will probably run slower than the original mosaik framework due to the changes I made in the code, in particular the Semaphore I 
implemeted to wait for sincronization between mosaik and the simulators.
