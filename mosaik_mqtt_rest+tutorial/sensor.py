import sys
import paho.mqtt.client as mqtt #import the client1
import time
from random import randint
from subprocess import Popen, CREATE_NEW_CONSOLE

broker_address = "127.0.0.1"

client = mqtt.Client("Sensor") #create new instance
client.connect(broker_address) #connect to broker
client.loop_start() #start the loop

client.publish("test/sensor1/x", "Model_0:20")
time.sleep(5)
client.publish("test/sensor1/x", "Model_0:0")
time.sleep(5)
client.publish("test/sensor1/x", "Model_0:20")
time.sleep(15)
client.publish("test/sensor1/x", "Model_0:100")