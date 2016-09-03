#! /usr/bin/env python

"""
 * File: sample.py
 * Authors: ESW Stanford: RECMS 2016
 * Date: 2016/09/02
"""

import time
import os
import RPi.GPIO as GPIO
import math
import sys
import argparse
import gammu
import numpy as np
import recms_lib

print message

text = ''
f = open(recms_lib.filename, 'r+')
f.seek(0)
for line in f:
	text += line
f.close()
print text


message = {
	'Text' : text,
	'SMSC' : {'Location':1},
	'Number' : recms_lib.number
}

sm = gammu.StateMachine()
sm.ReadConfig(0,0,'/etc/gammurc')
sm.Init()
sm.SendSMS(message)
sm.Terminate()
