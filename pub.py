import paho.mqtt.client as mqtt
from time import strftime, sleep
import csv
import glob, os

mqtt_username = "pi"
mqtt_password = "raspberry"
mqtt_broker_ip = "192.168.4.1"
port = 1883

# Callback Function on Connection with MQTT Server
# def on_connect( client, userdata, flags, rc):
# 	print ("Connected with Code :" +str(rc))
#	client.publish(topic="LED", payload="00")

client = mqtt.Client()
# client.on_connect = on_connect
client.username_pw_set(mqtt_username,mqtt_password)
client.connect(host=mqtt_broker_ip, port=port, keepalive=60)

client.loop_start()
while True:
    print("Switch to MANUAL mode\n -- turn light ON\n")
    client.publish(topic="LED", payload="11")
    sleep(30)
    print(" -- now turn light OFF\n")
    client.publish(topic="LED", payload="10")
    sleep(30)
    print("switch to AUTO mode\n")
    client.publish(topic="LED", payload="00")
    sleep(30)
client.loop_stop(force=False)
