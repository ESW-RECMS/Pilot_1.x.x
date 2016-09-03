#! /usr/bin/env python

"""
 * File: rms_adc_complete_test.py
 * Authors: ESW Stanford: RECMS 2016
 * Date: 2016/05/20
"""

import time
import os
import RPi.GPIO as GPIO
import math
import sys
import argparse
import gammu
import numpy as np
from datetime import datetime
from esw_lib import compute_rms
from esw_lib import compute_acrms 
from esw_lib import read_adc

""" --- DEFINE CONSTANTS --- """

ADC_MAX = 1023
ADC_REF = 3.3
VOLTS_PER_ADC = ADC_REF/ADC_MAX;
DEBUG = 0
ADC_CHANNELS = (7 , 6)
ADC_CHANNEL = 7
NUM_SAMPLES = 10000

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25
  
""" --- SETUP GPIO PINS FOR READING ADC --- """
  
# set up the SPI interface pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

""" --- START DATA SAMPLING --- """
line = ''
for adc_channel in ADC_CHANNELS:
	main_values = np.zeros(NUM_SAMPLES)
						
	trim_pot = 0
	tic = time.time()
	for i in range(NUM_SAMPLES): 
		# read the analog pin
		trim_pot = read_adc(adc_channel,SPICLK,SPIMOSI,SPIMISO,SPICS)

		if DEBUG:
			print "trim_pot:", trim_pot

		# add the value to the array
		main_values[i] = trim_pot
	toc = time.time()
		
	""" --- END DATA SAMPLING --- """

	""" --- COLLATE AND OUTPUT RESULTS --- """

	#print main_values

	avg = np.mean(main_values)
	acrms = compute_acrms(main_values,avg)
	vpp = (np.max(main_values)-np.min(main_values))
	rms = compute_rms(main_values)

	quan = 'V' if adc_channel % 2 == 0 else 'I'
	unit = 'V' if quan == 'V' else 'A'

	line += 'ADC'+str(adc_channel)+': '+quan+'rms = '+str(acrms*VOLTS_PER_ADC)+' '+unit
	line += ', '+quan+'pp = '+str(vpp*VOLTS_PER_ADC)+' '+unit+'\n'

line = line.strip()
f = open("/home/pi/ESW/Pilot_1.x.x/ADC/datatest.txt","w")
f.write(line)
f.close()


text = ''
f = open('/home/pi/ESW/Pilot_1.x.x/ADC/datatest.txt', 'r+')
f.seek(0)
for line in f:
	text += line
f.close()
print text


message = {
	'Text' : text,
	'SMSC' : {'Location':1},
	'Number' :'+15594929868'
}

sm = gammu.StateMachine()
sm.ReadConfig(0,0,'/etc/gammurc')
sm.Init()
sm.SendSMS(message)
sm.Terminate()

