#! /usr/bin/env python
import time
import gammu
from datetime import datetime

SLEEP_TIME = 150

for i in range(10):
	sm = gammu.StateMachine()
	sm.ReadConfig(0,0,'/etc/gammurc')
	sm.Init()

	f = open('/home/pi/ESW/ADC/datavalues.txt', 'r+')
	text = str(datetime.now())
	f.write(text)
	f.close()
	message = {
	'Text' : text,
	'SMSC' : {'Location':1},
	'Number' :'+15594929868'
	}
	sm.SendSMS(message)
	sm.Terminate()
	time.sleep(SLEEP_TIME)
	
