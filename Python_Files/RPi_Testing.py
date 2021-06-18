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

initial_phase = float(input("Initial oscillator phase? ")) # What are the units of 'phase'?
print("Initial phase value: {0} [units]".format(initial_phase))

threshold = 360 # "degrees" (could be radians)
data_time = time.time()
data_step = 1.0 # seconds
phase_time = time.time() - initial_phase
# (time.time() - phase_time) = phase
# time.time() = phase_time + phase
# time.time() - phase = phase_time
# Main Code #
while True:
	try:
		current_phase = time.time() - phase_time
		#1. Get current phase value
			# How fast is oscillator "spinning"?
			
		#2. Fire a pulse when phase reaches threshold
			# 2a. reset phase value to zero.
		if current_phase >= threshold:
			print("Phase Reset.")
			#phase_time = time.time() # This works, but is slightly variable
			phase_time += threshold # This is more consistent.
			current_phase -= threshold
			# 2b. send pulse to other oscillators (Xbee)
		# End if

		#3. Check for any received pulses from other oscillators
			# Update phase value based on sync algorithm.
		
		if (time.time()-data_time) > data_step:
			print("Current phase value: {0} [units]".format(current_phase)) # Display phase data to screen
			data_time += data_step # Increment data_time
		# End if
	except KeyboardInterrupt:
		break
# End while

## -- Ending Code Starts Here -- ##
# Make sure this code runs to end the program cleanly

Xbee.close()
GPIO.cleanup() # Reset GPIO pins for next program
