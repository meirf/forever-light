import unittest
import hebcal
import urllib2
from dateutil.parser import parse

class TestHebCal(unittest.TestCase):
    def test_date_parse(self):
        a = hebcal.parse_date("2015-09-04T19:05:00-04:00")
        self.assertTrue(a.hour==19)
        self.assertTrue(a.minute==5)

    def test_parse_heb_cal_full_response(self):
        url = "http://www.hebcal.com/hebcal/?v=1&cfg=json&maj=on&year=2015&month=9&c=on&geo=zip&zip=10012"
        response = hebcal.get_candles_havdalah(urllib2.urlopen(url).read())
        candles = set()
        candles.update(["2015-09-04T19:05:00-04:00", "2015-09-11T18:53:00-04:00","2015-09-13T18:50:00-04:00","2015-09-18T18:41:00-04:00","2015-09-22T18:34:00-04:00","2015-09-25T18:29:00-04:00","2015-09-27T18:26:00-04:00"])
        havdala = set()
        havdala.update(["2015-09-05T20:33:00-04:00", "2015-09-12T20:21:00-04:00","2015-09-15T20:16:00-04:00","2015-09-19T20:09:00-04:00","2015-09-23T20:03:00-04:00","2015-09-26T19:58:00-04:00","2015-09-29T19:53:00-04:00"])
        self.assertEqual((candles,havdala),response,"candle/hav don't match")

    def test_is_today_on_off(self):
        d = "2015-09-04T00:00:00-04:00"
        dobj = parse(d)
        on,time = hebcal.is_today_on_off(dobj)
        expec_on = True
        expec_time = parse("2015-09-04T19:05:00-04:00")
        self.assertEqual((on,time),(expec_on,expec_time),"is_today_on_off don't match")
        d = "2015-09-05T00:00:00-04:00"
        dobj = parse(d)
        on,time = hebcal.is_today_on_off(dobj)
        expec_on = False
        expec_time = parse("2015-09-05T20:33:00-04:00")
        self.assertEqual((on,time),(expec_on,expec_time),"is_today_on_off don't match")
        d = "2014-12-14T00:00:00-04:00"
        dobj = parse(d)
        on,time = hebcal.is_today_on_off(dobj)
        expec_on = None
        expec_time = None
        self.assertEqual((on,time),(expec_on,expec_time),str(on))

    def test_get_time_diff(self):
        now = parse("2015-09-04T19:05:00-04:00")
        critical_point = parse("2015-09-04T19:07:00-04:00")
        expected = 120
        self.assertEqual(expected,hebcal.get_time_diff(now, critical_point),"get_time_diff dont match")
        now = parse("2015-09-04T19:07:00-04:00")
        critical_point = parse("2015-09-04T19:05:00-04:00")
        expected = None
        self.assertEqual(expected,hebcal.get_time_diff(now, critical_point),"get_time_diff dont match")

if __name__ == '__main__':
    unittest.main()