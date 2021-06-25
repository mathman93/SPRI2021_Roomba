# when oscillator sends pulse, other oscillators jump to position + set value or to one depending on which
# is less distance.
# I think the value added is set from beginning as it shows it as 0.3 in model.
# in this case our jump value will be 120 as the model uses 1/3 of the total "rotation" as their jump value

import math

''' RPi_Testing.py
Purpose: Basic code for running Xbee, and illustrating code behavior.
	Sets up Xbee;
IMPORTANT: Must be run using Python 3 (python3)
Last Modified: 6/21/2021
By: Timothy Anglea
'''
## Import libraries ##
import serial  # For serial port functions (e.g., USB)
import time  # For accessing system time
import RPi.GPIO as GPIO  # For IO pin access on Raspberry Pi
import math

## Variables and Constants ##
global Xbee  # Specifies connection to Xbee
Xbee = serial.Serial('/dev/ttyUSB0', 115200)  # Baud rate should be 115200

## Functions and Definitions ##
''' Displays current date and time to the screen
	'''


def DisplayDateTime():
    # Month day, Year, Hour:Minute:Seconds
    date_time = time.strftime("%B %d, %Y, %H:%M:%S", time.gmtime())
    print("Program run: ", date_time)


## -- Code Starts Here -- ##
# Setup Code #
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering for GPIO
DisplayDateTime()  # Display current date and time

while True:
    try:
        initial_phase = float(input("Initial oscillator phase? "))  # What are the units of 'phase'?
        print("Initial phase value: {0} degrees".format(initial_phase))
        break
    except ValueError:
        print("Not a number. Try again.")
        continue
# End while

# Clear out Xbee message buffer.
if Xbee.inWaiting() > 0:  # If anything is in the Xbee receive buffer
    x = Xbee.read(Xbee.inWaiting()).decode()  # Clear out Xbee input buffer
# print(x) # Include for debugging
# End if

time_to_take = 2.0  # Length of cycle in seconds
# frequency = 180 # degrees per second
threshold = 360  # "degrees" (could be radians)
frequency = threshold / time_to_take  # degrees per second
# time_to_take = threshold/frequency
# frequency * time_to_take = threshold
phase_time = time.time() - (initial_phase / frequency)  # Time offset for the oscillator
# (time.time() - phase_time) = phase
# time.time() = phase_time + phase
# time.time() - phase = phase_time
pulse = 'z'  # Oscillator pulse character
updated_phase = None

data_time = time.time()
data_step = 1.0  # seconds

while True:
    try:
        # 1. Get current phase value
        # How fast is oscillator "spinning"?
        # #time_phase = time.time() - phase_time
        current_phase = (time.time() - phase_time) * frequency  # The current phase of the oscillator (in degrees)

        # 2. Fire a pulse when phase reaches threshold
        # 2a. reset phase value to zero.
        if current_phase >= threshold:
            print("Phase Reset.")
            # phase_time = time.time() # This works, but is slightly variable
            phase_time += time_to_take  # This is more consistent.
            current_phase -= threshold  # Technically unnecessary
            # current_phase -= (time_to_take*frequency)
            # 2b. send pulse to other oscillators (Xbee)
            Xbee.write(pulse.encode())  # Send the number over the Xbee
            print("You sent stuff.")
        # End if

        # 3. Check for any received pulses from other oscillators
        if Xbee.inWaiting() > 0:  # If there is something in the receive buffer
            received_pulse = Xbee.read(Xbee.inWaiting()).decode()  # Read all data in
            # received_pulse = "z" (pulse)
            print(received_pulse)  # To see what the message is

            # Update phase value based on sync algorithm.
            scaled_phase = 1 / threshold  # scale 360 down for function that is in terms of max of 1

            f = (1 / 2) * math.log(
                1 + (math.exp(2) - 1) * scaled_phase) + .1  # map state value and increment by small amount
            g = (math.exp(2 * f) - 1) / (math.exp(2) - 1)  # map f back into phase

            if g > 1:  # if phase value with increment hits threshold, fire pulse. Must reset phase to 0
                phase_time += current_phase / frequency  # do we need to calculate how much time has passed?

            else:
                updated_phase = g * threshold  # scales it up to threshold
                phase_time = phase_time - ((updated_phase - current_phase) / frequency)  # how much time do we take

                # End if

        if (time.time() - data_time) > data_step:
            print("Current phase value: {0} degrees".format(current_phase))  # Display phase data to screen
            data_time += data_step  # Increment data_time
            # End if
    except KeyboardInterrupt:
        break
