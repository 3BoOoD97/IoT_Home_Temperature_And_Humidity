# IoT_Home_Temperature_And_Humidity

#  Home temperature and humidity





Project Available at: [HackMd](https://hackmd.io/yLvdeyJ_Sea2Z6ib5_B_yg?both)
## :memo: Objective
The objective of this project is to show how to set up a system for measuring the temperature and humidity in real-time using Lopy4 and DHT11 and then connect Lopy4 to WIFI to display our sensor data on Datacake.
The estimated time to finish the project is around 7h-14h
**Purpose of project**
Due to the amount of time that both adults and children spend at home, the home environment is crucial. Reaching the proper room temperature is critical for several reasons. Physical comfort should be a priority. Being too warm affects your ability to focus while being too cold increases your risk of colds, even heart attacks and pneumonia. It also increases the risk of creating respiratory problems. No matter where you live, humidity can put a damper on your health and overall comfort. In the summer, humidity can make the heat feel even worse, causing people to feel lethargic, irritable and generally unwell. While many people think of humidity as hot, heavy and sticky outdoor air, it's important to also consider your home's indoor humidity levels.


**Material used**

| Parts	         | Price               |
| ----------------- |:----------------------- |
Jumper Cable 1-pin male-female 150 mm 10-pack      |29.00 kr[:link:][Cable]   |
| LoPy4 Basic bundle | 849.00 Kr[:link:][LoPy4]     |
| DHT11 Temperature & Humidity Sensor        | 39.00 Kr[:link:][DHT11]     |
| Shipping       | 127.00 Kr
| **Total**       | **1044.00 Kr**

[Cable]: https://www.electrokit.com/produkt/labsladd-1-pin-hane-hona-150mm-10-pack/

[LoPy4]: https://www.electrokit.com/en/product/lnu-1dt305-tillampad-iot-lopy4-basic-bundle/

[DHT11]: https://cdon.se/bygg-verktyg/temperatur-och-fukt-matare-digital-data-passar-arduino-dht11-p49343902



The LoPy4 Basic bundle comes with the following parts:

- LoPy4 with headers: is used to create and connect things over (LoRa, Sigfox, WiFi, Bluetooth).
- Expansion board: is used to connect the sensor and to the LoPy4 to the laptop. 
- Antennae: is used to connect the LoPy4 to (LoRa, Sigfox, WiFi, Bluetooth).
- USB cable: is used to connect the expansion board to the laptop.
- Jumper Cable: is used to connect the expansion board with the DHT11.
- DHT11: is used to sensing the temperature, humidity, and adjustable digital signal transmission (range of -20 to 60℃ with a ±2%. Range of 5 to 95% RH with a ±5%).




**Computer setup**
I started by downloading Lopy4 Firmware Updater that is provided here with the documentation [Pymakr Updater](https://docs.pycom.io/updatefirmware/device/)
After updating the firmware of Lopy4, I have chosen ATOM as my IDE for this project, since I have tried Visual Studio and ATOM and I found that ATOM is easier to use for such a project. After I downloaded ATOM I installed pymakr package by going to Packages -> typing pymakr in the search box -> Click on Install. 

![](https://i.imgur.com/M8eDnFE.png)

I had node.js and Python installed on my device before starting the project. Installing them is quite easy by following the documentation [Node.js](https://nodejs.org/en/download/) ,[Python](https://www.python.org/downloads/). Taking into account, Python should be added as PATH environment variables, the Instructions here will guide you on how to add Python environment to PATH variable in Windows [Add Python to PATH variable](https://www.educative.io/answers/how-to-add-python-to-path-variable-in-windows). If you have installed/updated the firmware correctly and if the port is connected the terminal in ATOM will show a green circle next to the port name, it looks like this:  ![](https:// "title")![](https://i.imgur.com/6OHrjUN.png) 
After we made sure that the port is successfully connected, it is time now to upload the code and run it, we can do this by clicking on the upload icon in the terminal, it looks like this:
![](https://i.imgur.com/PUTaRrS.png)
 





##  Putting everything together
![](https://i.imgur.com/h7CuIR0.jpg)

**Connecte the breadboard with the sensor**
In order to connect the sensor with the breadboard, we need 3 jumper wires.

* The green wire is for data, in this project we choosed PIN3.
* The red wire is for 3V3.
* The orange wire is for GND.

**Platform**

We used MQTT to connect to WiFi and send sensor data. MQTT is a form of lightweight IoT messaging protocol that can deliver real-time and dependable messaging service for IoT devices while utilizing very little code and bandwidth. It is appropriate for hardware-constrained devices and a network environment with constrained bandwidth. We have chosen Datacake to be our end-point after we have tried The Things Network(TTN), Helium and SigFox. However, all of them didn't work because coverage in my area is weak, so only Datacake worked for us. We believe that Datacake is a good option because it is easy to use and we didn't struggle too much to send the data to it and visualise it. 



### The code
For the DHT11 sensor, I am using the course-provided code on Gitlab: [DHT11 & DHT22 - Humidity & Temperature](https://gitlab.lnu.se/1dt305/sensor-libs/-/tree/master/DHT11%20%26%20DHT22%20-%20Humidity%20%26%20Temperature%20Sensor).

Before, sending the data to Datacake, we made sure that our code works and displays the correct values on the terminal.
By running the code below:
```javascript=16

import time
import ujson
import machine
import config
import pycom
import time
from machine import Pin
from dth import DTH

while True:
 result = th.read()
 if result.is_valid():

    temperature = result.temperature
    humidity = result.humidity

    print("Temperature: %d C" % temperature)
    print("Humidity: %d %%" % humidity)
    time.sleep(10) # Wait 10 Sec
```
And this the result we got by running the code
![](https://i.imgur.com/oERQLOM.png)


After we got this result and we made sure that our code works, it means now we are ready to send the data to Datacake.

To display the data that I am getting from the sensor I am using Datacake, the course tutorial helped me with the configuration and connection: [Datacake - WiFi, using MQTT](https://hackmd.io/@lnu-iot/r1aui0B59)  

- main：
```javascript=16
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
```
The main.py that we’ve just written, will publish temperature and humidity values to our MQTT broker every 10 seconds. Here we're expecting a message to appear on our terminal displaying temperature and humidity.
We are sending the temperature in Celsius. Still, we can send it in Fahrenheit if we add some mathematical operations to the result as follow:
```javascript=16
 result = 1.8 * th.read()  + 32;
```



Connectivity
---
We have tried to use TTN, Helium, and SigFox. However, none of them worked with us due to the weak coverage in my area, this is why we have decided to go with Datacake instead. We believe Datacake was a good option because it has a Time-series database for the collection and storage of sensor data and no need to code to create an intuitive dashboard. Moreover, it is user-friendly. 
### WiFi Connectivity
The WLAN (WiFi) is a system feature of all Pycom devices, therefore it is enabled by default. The development boards include an onboard antenna by default, so no external antenna is needed to get started. The WLAN network class always boots in WLAN.AP mode to connect it to an existing network.

The data is sent every 10 seconds through MQTT. To send the data we need to connect to our WiFi first. Taking into account, that the network should be 2.4GHz, otherwise, our device won’t be able to connect.
 
- boot：
```javascript=16
import network
import time
import config

# setup as a station
wlan = network.WLAN(mode=network.WLAN.STA)
wlan.connect(config.WIFI_SSID, auth=(network.WLAN.WPA2, config.WIFI_PASS))
while not wlan.isconnected():
    time.sleep_ms(50)
print(wlan.ifconfig())
```

### Datacake Connectivity

First, we need to create an account, and then we navigate to Devices and then we click on Add Add Device.   
1- We choose New Product and give it a name and we click on next
![](https://i.imgur.com/Z9m9fGH.png)

2- Now we give a name for our device, for the serial number we can leave it empty and it will be generated randomly.
![](https://i.imgur.com/fSU0YIY.png)

3- The last step for adding a device is to choose the plan, for our project we are not sending massive data so the free plan would be good for us.
![](https://i.imgur.com/vXBl0EF.png)

Now, after we created our device it is time to configure our device. We click on Configuration and we scroll down until we see Fields. In our project we want to send humidity and temperature values, so we created two fields Temperature and Humidity. 
![](https://i.imgur.com/8RWUSm5.png)

Now it is time, to update that field, we need to know that what Topic to publish to. We can do that by clicking on configure under the Integrations section. 
![](https://i.imgur.com/YMhKJw6.png)


We copy the string and paste it into our config.py file and then we add the fields name. In our project, we need to send two values so we should have two variables, TOPIC for temperature and TOPIC1 for humidity.
![](https://i.imgur.com/wlP6F2f.png)

For the SERIAL_NUMBER we can find it from the device page it would be at the top.
To get the TOKEN we should navigate to profile -> Edit Profile -> API -> Show. We copy the API Token and paste it into TOKEN variable in config.py file.

Now let us try the code and check if it sends data. We run the code and we check the Debug Log on Datacake.

![](https://i.imgur.com/PSQ8JYp.png)

Here, we can see that we are receiving HUMIDITY and TEMPERATURE values, which means we are receiving the data successfully and we are ready to visualize the data. 


### Presenting data

Last step in our project is visualizing Data on Datacake Dashboard, this can be accomplished by adding a widget on Datacake:

1- We go to our dashboard and we click on add widget

![](https://i.imgur.com/pGSZHOq.png)

2- We choose how we want our data to be displayed, for our project we chose Value Widget.

![](https://i.imgur.com/RB8cOrY.png)

3- Last step we specify which field we want to visualize and we click on Save.

![](https://i.imgur.com/v0QlQCa.png)

And here is the final result after creating the widgets
![](https://i.imgur.com/iUpEoih.png)

If we navigate to the history page we can find the data we are receiving for a specific period of time. Moreover, we can see CURRENT, AVERAGE, MAXIMUM, and MINIMUM values, which is really helpful.
Here is my device history after keeping it running for 1 hour:
![](https://i.imgur.com/JLdPv1r.png)


### Finalizing the design

I put the sensor on my table, it is located in the middle of my bedroom, so the result becomes more accurate (not so close to the window and not so far)
![](https://i.imgur.com/nwBMUmo.jpg)

After we finished our project, we made rules on Datacake to make the project more valuable. Rules would allow the user to act on events caused by a device's measurements, so we have created rules to send notification messages via email to notify us once each hour about the temperature and humidity status (cold, ideal, warm). Creating a rule is easy on Datacake by following this tutorial [Rule Engine](https://docs.datacake.de/device/rule-engine).
Here are the rules we have made:

![](https://i.imgur.com/53Dmfab.png)
* Cold temperature if the temperature is bellow 19°C.
* Ideal temperature if the temperature is between 19-21°C.
* Warm temperature if the temperature is above 21°C.
* Low humidity if the humidity is bellow 30%.
* Ideal humidity if the humidity is between 50-30%.
* High humidity if the humidity is above 50%.

I got this notification when my room temperature was 23°C and humidity 51%:
![](https://i.imgur.com/yJlT89P.png)
![](https://i.imgur.com/3lle1JP.png)


The DHT11 transmits data to the device using just one signal wire. Ground and 5V are supplied by independent cables. To ensure that the signal level stays high by default, a 10K Ohm pull-up resistor is required between the signal line and the 5V line.  Moreover, it includes a surface-mounted 10K Ohm pull-up resistor for the signal line.
Even though, the DHT11 sensor is not the most accurate. However, it is Low power consuming and has excellent long-term stability. Moreover, it is cheap and the measurement range it has is perfect for homes.
Despite that our project is a simple project. However, we struggled to find a contactable platform, we spent many hours trying to connect our device to the IoT networks like TTN,  Helium and SigFox, but unfortunately, we were unable to join any of them, we even bought a wide-range antenna and we couldn't join. We thought we wouldn't be able to do the project on time but Datacake saved us with its simplicity and clarity. Since we spent a lot of time on the connection we had no time to go through the  Payload and webhooks. Perhaps in the future, we go through those topics and use Golioth.io with Datacake so the widget looks more organised.
