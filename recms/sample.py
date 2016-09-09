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
from datetime import datetime
from recms_lib import compute_rms
from recms_lib import compute_acrms 
from recms_lib import read_adc
import recms_lib

""" --- DEFINE CONSTANTS --- """

ADC_MAX = 1023
ADC_REF = 3.3
VOLTS_PER_ADC = ADC_REF/ADC_MAX;
DEBUG = 0
ADC_CHANNELS = (0,1,2,3,4,5,6,7) 
NUM_SAMPLES = 10000

IV_PORT = 4
VOLTAGE_RATIO = 456.09 # 119.95 V actual / 0.263 V measured, based on oscilloscope photo
CURRENT_RATIO = 3.56 # 793 mA actual / 222.79 mV measured, based on oscilloscope photo

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
main_values = np.zeros((len(ADC_CHANNELS), NUM_SAMPLES))

tic = time.time()
for i in range(NUM_SAMPLES):
	for adc_channel in ADC_CHANNELS: 
		# read the analog pin
		adc_val = read_adc(adc_channel,SPICLK,SPIMOSI,SPIMISO,SPICS)
		if DEBUG:
			print "adc_val:", adc_val
		# add the corrected value to the array
		gain = CURRENT_RATIO if adc_channel<IV_PORT else VOLTAGE_RATIO
		main_values[adc_channel][i] = adc_val*VOLTS_PER_ADC*gain
toc = time.time()
print("sampling rate: "+str(len(ADC_CHANNELS)*NUM_SAMPLES/(toc-tic))+" Hz")

""" --- END DATA SAMPLING --- """

""" --- COLLATE AND OUTPUT RESULTS --- """
line = ""
for adc_channel in ADC_CHANNELS:
	avg = np.mean(main_values[adc_channel][:])
	acrms = compute_acrms(main_values[adc_channel][:],avg)
	vpp = (np.max(main_values[adc_channel][:])-np.min(main_values[adc_channel][:]))
	rms = compute_rms(main_values[adc_channel][:])
	quan = 'I' if adc_channel < IV_PORT else 'V'
	unit = 'V' if quan == 'V' else 'A'
	#gain = CURRENT_RATIO if adc_channel<IV_PORT else VOLTAGE_RATIO
	line+="%.3f" % (acrms)+','+"%.3f" % (vpp) +','
	#line += 'ADC'+str(adc_channel)+': '+quan+'rms = '+"%.3f" % (acrms*gain*VOLTS_PER_ADC)+' '+unit
	#line += ', '+quan+'pp = '+"%.3f" % (vpp*gain*VOLTS_PER_ADC)+' '+unit+'\n'

line = line.strip()
line = line[:-1]+'\n'
f = open(recms_lib.datafile,"a")
f.write(line)
f.close()
