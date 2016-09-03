#! /usr/bin/env python

"""
 * File: recms_lib.py
 * Authors: ESW Stanford: RECMS 2016
 * Date: 2016/05/20
"""

import RPi.GPIO as GPIO
import math
import numpy as np

def compute_rms(x):
    return np.sqrt(x.dot(x)/float(x.size))

def compute_acrms(x,dcoffset):
	y = x - dcoffset
	return np.sqrt(y.dot(y)/float(y.size))
	
def read_adc(adcnum, clockpin, mosipin, misopin, cspin):
	if ((adcnum > 7) or (adcnum < 0)):
			return -1
	GPIO.output(cspin, True)

	GPIO.output(clockpin, False)  # start clock low
	GPIO.output(cspin, False)     # bring CS low

	commandout = adcnum
	commandout |= 0x18  # start bit + single-ended bit
	commandout <<= 3    # we only need to send 5 bits here
	for i in range(5):
			if (commandout & 0x80):
					GPIO.output(mosipin, True)
			else:
					GPIO.output(mosipin, False)
			commandout <<= 1
			GPIO.output(clockpin, True)
			GPIO.output(clockpin, False)

	adcout = 0
	# read in one empty bit, one null bit and 10 ADC bits
	for i in range(12):
			GPIO.output(clockpin, True)
			GPIO.output(clockpin, False)
			adcout <<= 1
			if (GPIO.input(misopin)):
					adcout |= 0x1

	GPIO.output(cspin, True)

	adcout >>= 1       # first bit is 'null' so drop it
	return adcout
