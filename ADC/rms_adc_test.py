#! /usr/bin/env python

"""
 * File: rms_adc_test.py
 * Authors: ESW Stanford: RECMS 2016
 * Date: 2016/05/20
"""

import time
import os
import RPi.GPIO as GPIO
import math
import sys
import argparse
import numpy as np
from esw_lib import compute_rms
from esw_lib import compute_acrms 
from esw_lib import read_adc

""" --- DEFINE CONSTANTS --- """

ADC_MAX = 1023
ADC_REF = 3.3
DEBUG = 0
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

main_values = np.zeros(NUM_SAMPLES)

file = open("datavalues.txt","w")
					
trim_pot = 0
tic = time.time()
for i in range(NUM_SAMPLES): 
	# read the analog pin
	trim_pot = read_adc(ADC_CHANNEL,SPICLK,SPIMOSI,SPIMISO,SPICS)

	if DEBUG:
		print "trim_pot:", trim_pot

	# add the value to the array
	main_values[i] = trim_pot
toc = time.time()
	
""" --- END DATA SAMPLING --- """

""" --- COLLATE AND OUTPUT RESULTS --- """

print main_values

avg = np.mean(main_values)
acrms = compute_acrms(main_values,avg)
vpp = (np.max(main_values)-np.min(main_values))
rms = compute_rms(main_values)

#file.write("test")
print main_values.shape
print "mean:", avg, "||", avg/ADC_MAX*ADC_REF, "V"
try:
	#file.write('%s'  avg)
	file.write('{} '.format(avg))
except ValueError:
	print "error"
print "acrms:", acrms, "||", acrms/ADC_MAX*ADC_REF, "V"
#file.write(acrms)
file.write('{} '.format(acrms))
print "Vpp:", vpp, "||", vpp/ADC_MAX*ADC_REF, "V"
#file.write(vpp)
file.write('{} '.format(vpp))
print "rms:", rms, "||", rms/ADC_MAX*ADC_REF, "V"
#file.write(rms)
file.write('{} '.format(rms))
file.close

print "time:", toc-tic, "secs || samples/sec:", NUM_SAMPLES/(toc-tic)

