

import sys
import paho.mqtt.client as mqtt #import the client1
import time
from random import randint
from subprocess import Popen, CREATE_NEW_CONSOLE
broker_address = "127.0.0.1"

def on_message(client, userdata,message):
    #time.sleep(int(message.payload.decode("utf-8"))/10.0)
    topic = message.topic.split("/")
    client.publish(topic[1]+"/go", "go")


'''if __name__ == '__main__':
    if sys.argv[1] is None:
        print("manca il parametro")
        exit(0)
    print(sys.argv[1])
    topic = "prova/car_"
    client = mqtt.Client("Sensor"+sys.argv[1]) #create new instance
    client.connect(broker_address) #connect to broker
    client.on_message = on_message
    client.loop_start() #start the loop
    for i in range(int(sys.argv[1])-10,int(sys.argv[1])):
        client.subscribe(topic + str(i))
    #while 1:
    #client.publish("ExampleSim-0/Model_0/Sensor-0/verso", "ew")
    #time.sleep(1)
    
    #time.sleep(15)
    #client.publish("control/TestSim", None, retain=True)
    #client.publish("Agent_1/Semaforo-0/Model_1/verso", "ns")
    #time.sleep(2)
    #client.publish("Agent_1/Semaforo-0/Model_1/verso", "ew")
    #client.publish("Agent_1/Semaforo-0/Model_0/verso", "ns")
    #time.sleep(2)
    #client.publish("car_1/ciao","600")


    time.sleep(600)
    client.loop_stop() #stop the loop'''


client = mqtt.Client("Sensor") #create new instance
client.connect(broker_address) #connect to broker
client.loop_start() #start the loop
'''client.publish("control/TestSim", None, retain=True)
client.publish("control/ToastSim", None, retain=True)
client.publish("control/TextSim", None, retain=True)
client.publish("control/NestSim", None, retain=True)
client.publish("control/VestSim", None, retain=True)
client.publish("control/GuestSim", None, retain=True)
client.publish("control/TestJim", None, retain=True)
client.publish("control/TestRim", None, retain=True)
client.publish("control/TestDream", None, retain=True)'''
#client.publish("control/ExampleSim", None, retain=True)
#client.publish("control/ExampleCtrl", None, retain=True)
#client.publish("control/Collector", None, retain=True)

'''client.publish("control/TestSim", "127.0.0.1:7770,"
                                      "queue.pace.verso,"
                                      "test_,"
                                      "ExampleModel,"
                                        "Collector-0.Monitor%"
                                            "verso%"
                                            "queue;"
                                        "ExampleCtrl-0.Agent_0%"
                                            "queue>q_in"
                                      "/"
                                        "Collector-0.Monitor%"
                                            "pace%"
                                            "verso;"
                                        #"ExampleCtrl-0.Agent_1%"
                                        #    "queue>q_in"
                                      "/"
                                        "Collector-0.Monitor%"
                                            "pace%"
                                            "verso%"
                                            "queue",
                   retain=True)
client.publish("control/ToastSim", "127.0.0.1:7771,"
                                      "queue.pace.verso,"
                                      "test_,"
                                      "ExampleModel,"
                                        "Collector-0.Monitor%"
                                            "verso%"
                                            "queue;"
                                        "ExampleCtrl-0.Agent_0%"
                                            "queue>q_in"
                                      "/"
                                        "Collector-0.Monitor%"
                                            "pace%"
                                            "verso;"
                                        #"ExampleCtrl-0.Agent_1%"
                                        #    "queue>q_in"
                                      "/"
                                        "Collector-0.Monitor%"
                                            "pace%"
                                            "verso%"
                                            "queue",
                   retain=True)
client.publish("control/TextSim", "127.0.0.1:7772,"
                                      "queue.pace.verso,"
                                      "test_,"
                                      "ExampleModel,"
                                        "Collector-0.Monitor%"
                                            "verso%"
                                            "queue;"
                                        "ExampleCtrl-0.Agent_0%"
                                            "queue>q_in"
                                      "/"
                                        "Collector-0.Monitor%"
                                            "pace%"
                                            "verso;"
                                        #"ExampleCtrl-0.Agent_1%"
                                        #    "queue>q_in"
                                      "/"
                                        "Collector-0.Monitor%"
                                            "pace%"
                                            "verso%"
                                            "queue",
                   retain=True)
client.publish("control/NestSim", "127.0.0.1:7773,"
                                      "queue.pace.verso,"
                                      "test_,"
                                      "ExampleModel,"
                                        "Collector-0.Monitor%"
                                            "verso%"
                                            "queue;"
                                        "ExampleCtrl-0.Agent_0%"
                                            "queue>q_in"
                                      "/"
                                        "Collector-0.Monitor%"
                                            "pace%"
                                            "verso;"
                                        #"ExampleCtrl-0.Agent_1%"
                                        #    "queue>q_in"
                                      "/"
                                        "Collector-0.Monitor%"
                                            "pace%"
                                            "verso%"
                                            "queue",
                   retain=True)
client.publish("control/VestSim", "127.0.0.1:7774,"
                                      "queue.pace.verso,"
                                      "test_,"
                                      "ExampleModel,"
                                        "Collector-0.Monitor%"
                                            "verso%"
                                            "queue;"
                                        "ExampleCtrl-0.Agent_0%"
                                            "queue>q_in"
                                      "/"
                                        "Collector-0.Monitor%"
                                            "pace%"
                                            "verso;"
                                        #"ExampleCtrl-0.Agent_1%"
                                        #    "queue>q_in"
                                      "/"
                                        "Collector-0.Monitor%"
                                            "pace%"
                                            "verso%"
                                            "queue",
                   retain=True)
client.publish("control/GuestSim", "127.0.0.1:7775,"
                                      "queue.pace.verso,"
                                      "test_,"
                                      "ExampleModel,"
                                        "Collector-0.Monitor%"
                                            "verso%"
                                            "queue;"
                                        "ExampleCtrl-0.Agent_0%"
                                            "queue>q_in"
                                      "/"
                                        "Collector-0.Monitor%"
                                            "pace%"
                                            "verso;"
                                        #"ExampleCtrl-0.Agent_1%"
                                        #    "queue>q_in"
                                      "/"
                                        "Collector-0.Monitor%"
                                            "pace%"
                                            "verso%"
                                            "queue",
                   retain=True)
client.publish("control/TestJim", "127.0.0.1:7776,"
                                      "queue.pace.verso,"
                                      "test_,"
                                      "ExampleModel,"
                                        "Collector-0.Monitor%"
                                            "verso%"
                                            "queue;"
                                        "ExampleCtrl-0.Agent_0%"
                                            "queue>q_in"
                                      "/"
                                        "Collector-0.Monitor%"
                                            "pace%"
                                            "verso;"
                                        #"ExampleCtrl-0.Agent_1%"
                                        #    "queue>q_in"
                                      "/"
                                        "Collector-0.Monitor%"
                                            "pace%"
                                            "verso%"
                                            "queue",
                   retain=True)
client.publish("control/TestRim", "127.0.0.1:7777,"
                                      "queue.pace.verso,"
                                      "test_,"
                                      "ExampleModel,"
                                        "Collector-0.Monitor%"
                                            "verso%"
                                            "queue;"
                                        "ExampleCtrl-0.Agent_0%"
                                            "queue>q_in"
                                      "/"
                                        "Collector-0.Monitor%"
                                            "pace%"
                                            "verso;"
                                        #"ExampleCtrl-0.Agent_1%"
                                        #    "queue>q_in"
                                      "/"
                                        "Collector-0.Monitor%"
                                            "pace%"
                                            "verso%"
                                            "queue",
                   retain=True)
client.publish("control/TestDream", "127.0.0.1:7778,"
                                      "queue.pace.verso,"
                                      "test_,"
                                      "ExampleModel,"
                                        "Collector-0.Monitor%"
                                            "verso%"
                                            "queue;"
                                        "ExampleCtrl-0.Agent_0%"
                                            "queue>q_in"
                                      "/"
                                        "Collector-0.Monitor%"
                                            "pace%"
                                            "verso;"
                                        #"ExampleCtrl-0.Agent_1%"
                                        #    "queue>q_in"
                                      "/"
                                        "Collector-0.Monitor%"
                                            "pace%"
                                            "verso%"
                                            "queue",
                   retain=True)'''

'''for i in range(0, 9):
    subprocess.Popen("python simulator_mosaik.py -r 127.0.0.1:777" + str(i))'''

Popen("python simulator_mosaik.py -r 127.0.0.1:6666")
Popen("python controller.py -r 127.0.0.1:6667")
#Popen("python collector.py -r 127.0.0.1:6668")
time.sleep(60)