''' RPi_Testing.py
Purpose: Basic code for running Xbee, and illustrating code behavior.
	Sets up Xbee;
IMPORTANT: Must be run using Python 3 (python3)
Last Modified: 6/21/2021
By: Timothy Anglea
'''
## Import libraries ##
import serial # For serial port functions (e.g., USB)
import time # For accessing system time
import RPi.GPIO as GPIO # For IO pin access on Raspberry Pi
import math

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

while True:
	try:
		initial_phase = float(input("Initial oscillator phase? ")) # What are the units of 'phase'?
		print("Initial phase value: {0} degrees".format(initial_phase))
		break
	except ValueError:
		print("Not a number. Try again.")
		continue
# End while

# Clear out Xbee message buffer.
if Xbee.inWaiting() > 0: # If anything is in the Xbee receive buffer
	x = Xbee.read(Xbee.inWaiting()).decode() # Clear out Xbee input buffer
	#print(x) # Include for debugging
# End if

time_to_take = 2.0 # Length of cycle in seconds
# frequency = 180 # degrees per second
threshold = 360 # "degrees" (could be radians)
frequency = threshold / time_to_take # degrees per second
# time_to_take = threshold/frequency
# frequency * time_to_take = threshold
phase_time = time.time() - (initial_phase/frequency) # Time offset for the oscillator
# (time.time() - phase_time) = phase
# time.time() = phase_time + phase
# time.time() - phase = phase_time
pulse = 'z' # Oscillator pulse character

data_time = time.time()
data_step = 1.0 # seconds
# Main Code #
while True:
	try:
		#1. Get current phase value
			# How fast is oscillator "spinning"?
			# #time_phase = time.time() - phase_time
		current_phase = (time.time() - phase_time)*frequency # The current phase of the oscillator (in degrees)
		
		#2. Fire a pulse when phase reaches threshold
			# 2a. reset phase value to zero.
		if current_phase >= threshold:
			print("Phase Reset.")
			#phase_time = time.time() # This works, but is slightly variable
			phase_time += time_to_take # This is more consistent.
			current_phase -= threshold # Technically unnecessary
			#current_phase -= (time_to_take*frequency)
			# 2b. send pulse to other oscillators (Xbee)
			Xbee.write(pulse.encode()) # Send the number over the Xbee
			print("You sent stuff.")
		# End if

		#3. Check for any received pulses from other oscillators
		if Xbee.inWaiting() > 0: # If there is something in the receive buffer
			received_pulse = Xbee.read(Xbee.inWaiting()).decode() # Read all data in
			# received_pulse = "z" (pulse)
			print(received_pulse) # To see what the message is
			# Update phase value based on sync algorithm.
            #In coolretion to Dr.Wangs document on PCO's and Energy efficient sync
            # To my knowledge the format of this PCO system is that once a oscillator recivies a pulse it will check its current phase to determine whether or not it needs to advance or have a delay.
            # After reading it was not a 100% sure on how the delay worked but for the advancement I did find an equation that I beleive is the correct one.
            
            if  current_phase > (threshold/2)
                    # at this point we would need to have a advandment, at a time determined by an equation, pg 4 section B, formula 2, I think...
            elif current_phase < (threshold/2)
                    # This would then lead to a delay possibly a refractory period??
            elif current_phase = threshold or current_phase = 0
                    # No change in stance




		# End if
		
		if (time.time()-data_time) > data_step:
			print("Current phase value: {0} degrees".format(current_phase)) # Display phase data to screen
			data_time += data_step # Increment data_time
		# End if
	except KeyboardInterrupt:
		break
# End while

## -- Ending Code Starts Here -- ##
# Make sure this code runs to end the program cleanly

Xbee.close()
GPIO.cleanup() # Reset GPIO pins for next program
