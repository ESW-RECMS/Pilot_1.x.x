#! /usr/bin/env python

from datetime import datetime

f = open('/home/pi/ESW/Pilot_1.x.x/ADC/datavalues.txt', 'r+')
f.write(str(datetime.now()))
f.close()
