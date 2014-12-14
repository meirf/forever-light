#!/usr/bin/python

import time
from phue import Bridge

b = Bridge('192.168.1.134')

b.set_light(1, 'bri', 10)

time.sleep(5)

b.set_light(2, 'bri', 10)

time.sleep(3)

b.set_light(3, 'bri', 10)
