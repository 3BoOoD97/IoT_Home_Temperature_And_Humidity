from mqtt import MQTTClient
import time
import ujson
import machine
import config
import pycom
import time
from machine import Pin
from dth import DTH

def sub_cb(topic, msg):
   print(msg)

# MQTT Setup
client = MQTTClient(config.SERIAL_NUMBER,
                    config.MQTT_BROKER,
                    user=config.TOKEN,
                    password=config.TOKEN,
                    port=config.PORT)
client.set_callback(sub_cb)
client.connect()
print('connected to MQTT broker')

# The MQTT topic that we publish data to
myTemp = config.TOPIC
myHumid= config.TOPIC1

pycom.heartbeat(False)
pycom.rgbled(0x000008) # blue
th = DTH(Pin('P3', mode=Pin.OPEN_DRAIN),0)
time.sleep(2)

while True:
 result = th.read()
 if result.is_valid():

     #Save temperature &  humidity in variables
    temperature = result.temperature
    humidity = result.humidity

    pycom.rgbled(0x007f00) # green
    client.publish(topic=myTemp, msg=str(temperature) ) # Publishes a message to a connected MQTT broker.
    client.check_msg() # check if there are MQTT messages

    client.publish(topic=myHumid, msg=str(humidity) ) # Publishes a message to a connected MQTT broker.
    client.check_msg() # check if there are MQTT messages
    # Print the data
    print("Temperature: %d C" % temperature)
    print("Humidity: %d %%" % humidity)
    time.sleep(10) # Wait 10 Sec
