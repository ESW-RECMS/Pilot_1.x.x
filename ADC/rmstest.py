#! /usr/bin/env python
"""
 * File: template.py
 * Author: FILL NAME HERE
"""
import time
import os
import RPi.GPIO as GPIO
import math
import sys
import argparse
import numpy as np

main_values = np.array([])
GPIO.setmode(GPIO.BCM)
DEBUG = 1
#import scipy.stats as st
#import matplotlib.pyplot as plt

def rms(x):
    return np.sqrt(x.dot(x)/float(x.size))

def acrms(x,dcoffset):
	x -= dcoffset
	return np.sqrt(x.dot(x)/float(x.size))
	#return np.sqrt(rms**2-dcoffset**2)
	
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
	print "here in there"
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

#def main(argc,argv):
"""
N = 1001
t = np.linspace(-2*np.pi,2*np.pi,N)
f = np.sin(t)
d = np.array([1, 2, 3, 4, 5, 6])
dcoffset = 2.3
print rms(d)
print acrms(d,0)
print d+dcoffset
print acrms(d+dcoffset,dcoffset)
print rms(f)
print acrms(f+dcoffset,dcoffset)
"""

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

# set up the SPI interface pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)


# 10k trim pot connected to adc #0
potentiometer_adc = 5;

last_read = 0       # this keeps track of the last potentiometer value
tolerance = 5       # to keep from being jittery we'll only change
					# volume when the pot has moved more than 5 'counts'
					


i = 0
trim_pot = 0
while i <= 100:
	print i 
	i = i+1
	# we'll assume that the pot didn't move
	trim_pot_changed = False

	# read the analog pin
	trim_pot = readadc(potentiometer_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
	main_values = np.append(main_values,last_read)
	# how much has it changed since the last read?
	pot_adjust = abs(trim_pot - last_read)
	
	print trim_pot
	
	

	if DEBUG:
			print "trim_pot:", trim_pot
			print "pot_adjust:", pot_adjust
			print "last_read", last_read

	if ( pot_adjust > tolerance ):
		   trim_pot_changed = True

	if DEBUG:
			print "trim_pot_changed", trim_pot_changed

	if ( trim_pot_changed ):
			set_volume = trim_pot / 10.24           # convert 10bit adc0 (0-1024) trim pot read into 0-100 volume level
			set_volume = round(set_volume)          # round out decimal value
			set_volume = int(set_volume)            # cast volume as integer

			print 'Volume = {volume}%' .format(volume = set_volume)
			set_vol_cmd = 'sudo amixer cset numid=1 -- {volume}% > /dev/null' .format(volume = set_volume)
			os.system(set_vol_cmd)  # set volume

			if DEBUG:
					print "set_volume", set_volume
					print "tri_pot_changed", set_volume

			# save the potentiometer reading for the next loop
			last_read = trim_pot
			main_values = np.append(main_values,last_read)
			print main_values[i]
			#if i > 100:
			#	break

	# hang out and do nothing for a half second
	
	time.sleep(0.1)
	
print main_values

#if __name__ == "__main__":
#	main(len(sys.argv),sys.argv)
