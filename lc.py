from HX711 import * # https://github.com/endail/hx711-rpi-py
from datetime import timedelta
import time
import sys
import paho.mqtt.client as mqtt # Allow publishing to MQTT Server

Debug = True              # True to print messages to screen
MQTT_Enable = False       # True to send via MQTT
Broker_IP = "10.74.1.224" # MQTT Broker IP *** IP address of your MQTT Broker ***
Broker_Port = "1883"      # MQTT Broker Port *** Port of your MQTT Broker 1883 is default ***
MQTT_Wait = .01           # Pause between MQTT Topic Pulishing
Count = 1                 # Reading Count
Weight_Holder = 107.0     # Weight of the Spool Holder
Weight_Spool_Empty = 200  # Weight of an Empty Spool

def MQTT():
  # Send to the MQTT Broker
  try:
    mqttc = mqtt.Client("python_pub")
    mqttc.connect(Broker_IP, Broker_Port)
    time.sleep(MQTT_Wait)
    QoS = 0
    Retain = True
    # mqttc.publish(Topic, Payload, QoS, Retain)
    # QoS 0=Send only, 1=Confirm, 2=send until confirmed
    #mqttc.publish("filament_3d/Weight_TD", Weight, QoS, Retain)
    #if Debug is True: print('MQTT published Weight_TD')
    #time.sleep(MQTT_Wait)
    mqttc.publish("filament_3d/Weight_AVG", Weight, QoS, Retain)
    if Debug is True: print('MQTT published Weight_AVG')
    time.sleep(MQTT_Wait)

  except:
    # Prevent crashing if Broker is disconnected
    if Debug is True:
      print ("MQTT Failed")

# create a SimpleHX711 object using GPIO pin 20 as the data pin
# GPIO pin 21 as the clock pin
# -382 as the reference unit
# -91470 as the offset
#with AdvancedHX711(20, 21, 374, 89057, Rate.HZ_80) as hx:
#with SimpleHX711(20, 21, 367, 90684) as hx:
with SimpleHX711(20, 21, 382, 91470) as hx:

  # set the scale to output weights in OZ ounces/ G grams
  hx.setUnit(Mass.Unit.G)

  # constantly output weights using the median of x samples
  try:
    while True:
      #LC_1 = str(hx.weight(timedelta(seconds=1)))
      #Weight_TD = float(LC_1.split(" ", 1)[0]) #Extract number from string without units
      #Weight_TD = Weight_TD - Weight_Holder - Weight_Spool_Empty
      #if Debug is True:
      #  print("TimeDelta " + str(Weight_TD))
      #time.sleep(30)
      LC_2 = str(hx.weight(10))
      Weight_Avg = float(LC_2.split(" ", 1)[0]) #Extract number from string without units
      Weight_Avg = Weight_Avg - Weight_Holder - Weight_Spool_Empty
      if Debug is True:
        print("Average " + str(Weight_Avg))
        print("Reading " + str(Count))
        Count = Count + 1
      time.sleep(30)
      if MQTT_Enable is True:
        MQTT()

  except KeyboardInterrupt:
    if Debug is True: print("Exiting")
    sys.exit()
