''' RPi_Testing.py
Purpose: Basic code for running Xbee, and illustrating code behavior.
	Sets up Xbee;
IMPORTANT: Must be run using Python 3 (python3)
Last Modified: 7/12/2021
By: Timothy Anglea
'''
## Import libraries ##
import serial # For serial port functions (e.g., USB)
import time # For accessing system time
import RPi.GPIO as GPIO # For IO pin access on Raspberry Pi
import math
import os.path # For setting directory path for files

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

collect_data = False # Boolean for choosing to collect and save data from program

while True:
	try:
		initial_heading = float(input("Initial robot heading value? ")) # in degrees
		print("Initial phase value: {0} degrees".format(initial_heading))
		break
	except ValueError:
		print("Not a number. Try again.")
		continue
# End while

if collect_data: # is True
	# Open a text file for data retrieval
	file_name_input = input("Name for data file: ")
	dir_path = "/home/pi/SPRI2021_Roomba/Data_Files/" # Directory path to save file on Raspberry Pi
	file_name = os.path.join(dir_path, file_name_input+".txt") # text file extension
	file = open(file_name, "w") # Open a text file for storing data
		# Will overwrite anything that was in the text file previously
# End if

# Clear out Xbee message buffer.
if Xbee.inWaiting() > 0: # If anything is in the Xbee receive buffer
	x = Xbee.read(Xbee.inWaiting()).decode() # Clear out Xbee input buffer
	#print(x) # Include for debugging
# End if

N = 3 # Number of oscillators
time_to_take = 3.0 # Length of cycle in seconds
# frequency = 180 # degrees per second
threshold = 360 # "degrees" (could be radians)
frequency = threshold / time_to_take # degrees per second
# time_to_take = threshold/frequency
# frequency * time_to_take = threshold
initial_phase = initial_heading
phase_time = time.time() - (initial_phase/frequency) # Time offset for the oscillator
#heading = initial_phase (spinning robot again)
# (time.time() - phase_time) = phase
# time.time() = phase_time + phase
# time.time() - phase = phase_time
pulse = 'z' # Oscillator pulse character

heading = initial_heading # Variable for direction of robot
data_time = time.time()
data_step = 0.5 # seconds
just_fired = False
# Main Code #
while True:
	try:
		current_time = time.time() # Get current time for the loop iteration (rather than calling it multiple different times)
		#1. Get current phase value
			# How fast is oscillator "spinning"?
			# #time_phase = time.time() - phase_time
		current_phase = (current_time - phase_time)*frequency # The current phase of the oscillator (in degrees)
		#heading = current_phase # Robots are constantly spinning (not good)

		#2. Fire a pulse when phase reaches threshold
			# 2a. reset phase value to zero.
		if current_phase >= threshold:
			print("Phase Reset.")
			#phase_time = time.time() # This works, but is slightly variable
			phase_time += time_to_take # This is more consistent.
			current_phase -= threshold # Technically unnecessary
			#current_phase -= (time_to_take*frequency)
			# 2b. send pulse to other oscillators (Xbee)
			Xbee.write(pulse.encode()) # Send the pulse over the Xbee
			print("You sent stuff.") # Include for debugging
			just_fired = True # Boolean for DESYNC algorithm
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
			#phase_change = -(alpha)*current_phase
				# alpha is pretty small, probably less than 0.1
			#current_phase += phase_change #(also update phase_time)
			#heading += phase_change # (Update robot heading value by the same amount)

			# PRF Desync - Look up value to change in PRF
			if current_phase > threshold * (N-1)/N:
				pass
				# move backwards in phase
			elif current_phase < threshold * (1/N):
				pass
				# move forwards in phase
			else:
				pass
				# Don't move at all
			# End if
		# End if
		
		# Print out and save data
		if (current_time-data_time) > data_step:
			print("Current phase value: {0} degrees".format(current_phase)) # Display phase data to screen
			if collect_data: # is True
				# Write data to file
				file.write("{0:.3f}, {1:.3f}, {2:.3f}\n".format(current_time, current_phase, heading))
			# End if
			data_time += data_step # Increment data_time
		# End if
	except KeyboardInterrupt: # (e.g., Ctrl + c)
		break # End while loop and exit code cleanly
# End while

## -- Ending Code Starts Here -- ##
# Make sure this code runs to end the program cleanly

if collect_data: # is True
	file.close() # Close data file when done.
# End if
Xbee.close()
GPIO.cleanup() # Reset GPIO pins for next program

''' Poster Content
Abstract:

1. Introduction:
	a. What is the problem? ("Our research addresses the problem of...")
	b. Why is it a problem?
	c. What have other people done to solve this problem? (Literature review)
	d. How are we going to solve this problem? (what is different or new?)

2. "Methods":
	Details on how we will solve the problem
		What algorithms are we using?
		What background information is needed?
		Which variables mean what in the formulas?

3. Results:
	Data and figures from experiments or simulations
		Provide experimental setup parameters and details
		Explain important aspects of figures and tables
		Discuss impliplications of the experimental results
			What does the data mean?
			How do these results show that our solution addresses the problem?

4. Conclusion:
	Summarize the problem, our solution, and the key results
	Suggest future work based on what we did
		How would we do these same experiments differently?
		What should be the methods or experiments we look at next?
'''