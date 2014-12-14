#!/usr/bin/python

import time
from phue import Bridge

b = Bridge('192.168.1.134')

print b.get_api()

b.set_light(1, 'bri', 1)

time.sleep(3)

b.set_light(1, 'bri', 254)

time.sleep(3)

b.set_light(1, 'bri', 1)
