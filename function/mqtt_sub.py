
import sys, select, os
import threading 
if os.name == 'nt':
  import msvcrt, time
else:
  import tty, termios
import time
import threading
import paho.mqtt.client as mqtt
key = ''
host = "test.mosquitto.org"
port = 8000
def on_connect(self, client, userdata, rc):
    print("MQTT Connected.")
    self.subscribe("MQTT/SMF")

def on_message(client, userdata,msg):
    global key
    key = msg.payload.decode("utf-8", "w")
    print(key)
def connect_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host)
    client.loop_forever()
def printkey():
  global key
  while True:
    print(key)
    time.sleep(1)
threading.Thread(target=printkey).start()
client = connect_mqtt()
client.loop_forever()