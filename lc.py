from HX711 import *
from datetime import timedelta
import time
import sys
#import RPi.GPIO as GPIO

# create a SimpleHX711 object using GPIO pin 2 as the data pin,
# GPIO pin 3 as the clock pin, -370 as the reference unit, and
# -367471 as the offset
#with AdvancedHX711(20, 21, 374, 89057, Rate.HZ_80) as hx:
#with SimpleHX711(20, 21, 367, 90684) as hx:
with SimpleHX711(20, 21, 382, 91470) as hx:

  # set the scale to output weights in OZ ounces/ G grams
  hx.setUnit(Mass.Unit.G)

  # constantly output weights using the median of x samples
  try:
    while True:
      print("TimeDelta")
      print(hx.weight(timedelta(seconds=30)))
      time.sleep(30)
      print("Average")
      print(hx.weight(100))
      time.sleep(30)

  except KeyboardInterrupt:
    print("Bye!")
    sys.exit()

