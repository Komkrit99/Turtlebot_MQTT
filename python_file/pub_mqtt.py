import paho.mqtt.client as mqtt
import time
import sys
host = "enkey.bu.ac.th"
port = 1883

client = mqtt.Client()
client.connect(host)
print(sys.argv[1])
client.publish("Turtlebot3/MQTT",sys.argv[1])
#time.sleep(5)
#client.publish("TEST/MQTT","s")
print('successful')