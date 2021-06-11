''' RPi_Testing.py
Purpose: Basic code for running Xbee, and illustrating code behavior.
	Sets up Xbee;
IMPORTANT: Must be run using Python 3 (python3)
Last Modified: 6/11/2021
By: Timothy Anglea
'''
## Import libraries ##
import serial # For serial port functions (e.g., USB)
import time # For accessing system time
import RPi.GPIO as GPIO # For IO pin access on Raspberry Pi

## Variables and Constants ##
global Xbee # Specifies connection to Xbee
Xbee = serial.Serial('/dev/ttyUSB0', 115200) # Baud rate should be 115200

## Functions and Definitions ##
''' Displays current date and time to the screen
	'''
def DisplayDateTime():
	# Month day, Year, Hour:Minute:Seconds
	date_time = time.strftime("%B %d, %Y, %H:%M:%S", time.gmtime())
	print("Program run: ", date_time)

## -- Code Starts Here -- ##
# Setup Code #
GPIO.setmode(GPIO.BCM) # Use BCM pin numbering for GPIO
DisplayDateTime() # Display current date and time

# Clear out Xbee message buffer.
if Xbee.inWaiting() > 0: # If anything is in the Xbee receive buffer
	x = Xbee.read(Xbee.inWaiting()).decode() # Clear out Xbee input buffer
	#print(x) # Include for debugging

phase = float(input("Initial oscillator phase? ")) # What are the units of 'phase'?
print("Initial phase value: {0} [units]".format(phase))

# Main Code #


## -- Ending Code Starts Here -- ##
# Make sure this code runs to end the program cleanly

Xbee.close()
GPIO.cleanup() # Reset GPIO pins for next program
