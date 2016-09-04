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

ADC_CHANNELS = (0,1,2,3,4,5,6,7) 

text = ''
f = open(recms_lib.datafile, 'r+')
num_lines = len(f.readlines())
file_values = np.zeros(len(ADC_CHANNELS))

f.seek(0)
for line in f:
	line_vector = line.split(',')
	for i in line_vector:
		file_values[i]+=float(line_vector[i])/num_lines
f.close()

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
