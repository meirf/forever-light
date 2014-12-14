from phue import Bridge
import time

b = Bridge('10.214.59.124')
b.connect()

def turn_on():
    b.set_light(1, 'on', False)
    #time.sleep(2)
    #b.set_light(1, 'on', True)
    #b.set_light(1, 'bri', 254)
    time.sleep(1)
    b.set_light(1, 'on', True)
    b.set_light(1, 'bri', 1)
    time.sleep(1)
    b.set_light(1, 'bri', 100)
    time.sleep(1)
    b.set_light(1, 'bri', 255)

def turn_off():
    b.set_light(1, 'on', False)

if __name__=="__main__":
    b.connect()
    turn_on()