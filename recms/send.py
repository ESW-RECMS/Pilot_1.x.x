#! /usr/bin/env python

"""
 * File: sample.py
 * Authors: ESW Stanford: RECMS 2016
 * Date: 2016/09/06
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
PARTITIONS = 2 #must be a multiple of len(ADC_CHANNELS)

text = ''
f = open(recms_lib.datafile, 'wr+')
num_lines = len(f.readlines())
pp_values = np.zeros(len(ADC_CHANNELS))
rms_values = np.zeros(len(ADC_CHANNELS))
f.seek(0)
for line in f:
	line_vector = line.split(',')
	for i in range(len(line_vector)):
		if i%2==0:
			rms_values[i/2]+=float(line_vector[i])/num_lines
		else:
			pp_values[i/2]+=float(line_vector[i])/num_lines

f.close()

#verbose text
for i in range(len(rms_values)):
	text+=recms_lib.get_adc_type(i)+str(recms_lib.adc_to_channel(i))+":"+str(rms_values[i])+recms_lib.get_adc_unit(i)+'\n'

#csv text
#for i in range(rms_values):
#	text+=rms_values[i]+','
#	text = text[:-1]

	if((i+1)%(len(ADC_CHANNELS)/PARTITIONS)==0):
		message = {
			'Text' : text,
			'SMSC' : {'Location':1},
			'Number' : recms_lib.number
		}

		sm = gammu.StateMachine()
		sm.ReadConfig(0,0,'/etc/gammurc')
		sm.Init()
		sm.SendSMS(message)
		print("sent: "+text)
		sm.Terminate()
		text=''




