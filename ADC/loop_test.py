#! /usr/bin/env python

#import time
import gammu
from datetime import datetime

sm = gammu.StateMachine()
sm.ReadConfig(0,0,'/etc/gammurc')
sm.Init()
i = 0
#while(True):
f = open('/home/pi/ESW/ADC/datavalues.txt', 'r+')
#var = f.readline()
f.write(str(datetime.now()))
#var = 'test' 
#print var
message = {
'Text' : 'jhgfjrf'+str(i),
'SMSC' : {'Location':1},
'Number':'+15594929868',
}
sm.SendSMS(message)
#time.sleep(20)
i += 1
