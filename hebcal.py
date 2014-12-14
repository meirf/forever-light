from dateutil.parser import parse
import json
import urllib2
import datetime
from sys import argv
import time
import pytz
import main

#return True,date False,date None,None
def is_today_on_off(date):
    year = date.year
    month = date.month
    url_base = "http://www.hebcal.com/hebcal/?v=1&cfg=json&maj=on&c=on&geo=zip&zip=10012"
    url_base+="&year="+str(year)
    url_base+="&month="+str(month)
    (can,hav) = get_candles_havdalah(urllib2.urlopen(url_base).read())
    for c in can:
        d = parse(c)
        if d.day==date.day:
            return True,d
    for h in hav:
        d=parse(h)
        if d.day==date.day:
            return False,d
    return None, None

def parse_date(date_field):
    return parse(date_field)

#returns ({candle_1,candle_2 ....},{hav_1,hav_2...})
def get_candles_havdalah(full__str_response):
    js = json.loads(full__str_response)
    candles = set()
    for x in js['items']:
        if x['category']=='candles':
            candles.add(x['date'])
    havdala = set()
    for x in js['items']:
        if x['category']=='havdalah':
            havdala.add(x['date'])
    return (candles, havdala)

#return None if critical_point already happened
#assumed now and critical_point are same day
def get_time_diff(now, critical_point):
    if now is None:
        now = datetime.datetime.now()
    if critical_point>now:
        return (critical_point-now).seconds
    return None

def demo_1():
    d = raw_input("Please enter date: ")
    dobj = parse(d)
    on,t = is_today_on_off(dobj)
    if on:
        print "Turn ON lights at..."
    if not on:
        print "Turn OFF lights at..."
    print t

def demo_2(critical_point):
    now = datetime.datetime.now(pytz.utc)
    now = now - datetime.timedelta(0,3600)
    diff = get_time_diff(now,critical_point)
    if diff is not None:
        print "Sleeping for %d seconds" %(diff)
        time.sleep(diff)
    else:
        print "Sleeping for %d seconds:" %(24*60*60)
        time.sleep(24*60*60)
    print "Turning on light..."
    main.turn_on()
    while True:
        print "Sleeping for %d seconds:" %(24*60*60)
        time.sleep(24*60*60)
        now = datetime.datetime.now(pytz.utc)
        now = now - datetime.timedelta(0,3600)
        on,t = is_today_on_off(now)
        if on is not None:
            diff = get_time_diff(now,t)
            time.sleep(diff)
            if on:
                main.turn_on()
            else:
                main.turn_off()

#2086-09-08T00:00:00-04:00
#2086-09-10T00:00:00-04:00
if __name__=="__main__":
    if argv[1] == str(1):
        demo_1()
    if argv[1] == str(2):
        print "Start demo 2..."
        critical_point = argv[2]
        demo_2(parse(critical_point))