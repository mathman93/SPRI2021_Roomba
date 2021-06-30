''' RPi_Testing.py
Purpose: Basic code for running Xbee, and illustrating code behavior.
	Sets up Xbee;
IMPORTANT: Must be run using Python 3 (python3)
Last Modified: 6/29/2021
By: Jamez White
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
		coupling_strength = float(input("Enter coupling strength ")) # What percentage of
		print("Coupling_strength: {0} %".format(coupling_strength))
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
N = 3
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

coupling_strengthP = coupling_strength/100 # this conversts the coupling strength in a percent so we can use it later.
data_time = time.time()
data_step = 1.0 # seconds
just_fired = False
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
            just_fired = True
		# End if

		#3. Check for any received pulses from other oscillators
		if Xbee.inWaiting() > 0: # If there is something in the receive buffer
			received_pulse = Xbee.read(Xbee.inWaiting()).decode() # Read all data in
			# received_pulse = "z" (pulse)
			print(received_pulse) # To see what the message is
            # Update phase value based on (de)sync algorithm.
            # DESYNC algorithm - move to the midpoint
            if just_fired == False:
                pass
                # Save value of oscillator in front of me.
                # (forward_phase = threshold - current_phase)
            else: #if just_fired == True:
                pass
                # Backward_phase = (-1)*current_phase
                # Calculated midpoint, and move there
            
            just_fired = False
            
            # Inverse-MS algorithm - always move backwards
             #alpha in Degesys 2007 is user inputed, page 6 out of 10
             alpha = .09
             phase_change = -(alpha)*current_phase
                # alpha is pretty small, probably less than 0.1
             current_phase += phase_change # (also update phase_time)
              phase_time += alpha/frequency
            #I am not 100% sure on this one, on the doucment I was looking at, I could not get a clear idea on it (Nagpal)
            
            
            # PRF Desync - Look up value to change in PRF
            
            #This one was similar to the synch one just with a few added things, (I think that was the whole point though), with that being said I assumed the symbol that looks like an l is coupling strength in another formed, so it was treated like so. 
            if current_phase > threshold * (N-1)/N:
            
                QD = -coupling_strengthP(current_phase-(threshold/N)
                Current_phase = current_phase + QD #Calculating how much phase to change
                phase_time += QD/frequency
                pass
                # move backwards in phase
            elif current_phase < threshold * (1/N):
                QA = -coupling_strengthP(current_phase-(threshold-threshold/N)
                Current_phase = current_phase + QA #Calculating how much phase to change
                phase_time += QA/frequency
                
                pass
                # move forwards in phase
            else:
                pass
                # Don't move at all
            # End if
            
            

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
