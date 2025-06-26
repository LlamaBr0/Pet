# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Tony                                                         #
# 	Created:      6/25/2025, 12:55:50 PM                                       #
# 	Description:  EXP project                                                  #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain = Brain()
brainInertial = Inertial()
motorR = Motor(Ports.PORT1)
motorL = Motor(Ports.PORT5)
senseMotor = Motor(Ports.PORT4)
sense = Distance(Ports.PORT2)
drivebase = SmartDrive(motorL, motorR, brainInertial, 260, 320, 320, MM, 1)

def calibrateInertial():
    brain.screen.print("Calibrating Gyro")
    brain.screen.new_line()
    brain.screen.print("Please Wait")
    brainInertial.calibrate
    while brainInertial.is_calibrating():
        wait(25, MSEC)
    brain.screen.clear_screen()
    brain.screen.set_cursor(1,1)

senseMotor.set_position(0, DEGREES)
senseMotor.set_velocity(10, PERCENT)
motorR.set_reversed(True)

def seek():
    global found_object
    found_object = False
    global angle
    global object_distance 
    while found_object == False:
        senseMotor.spin_to_position(30, DEGREES, 5, PERCENT, False)
        if sense.object_distance(INCHES) < 40:
            break
        senseMotor.spin_to_position(-30, DEGREES, 5, PERCENT, False)
        if sense.object_distance(INCHES) < 40:
            break
    senseMotor.stop(BRAKE)
    angle = senseMotor.position(DEGREES)
    found_object = True
    object_distance = sense.object_distance()

calibrateInertial()

while True:

    seek()

    drivebase.turn_to_heading(angle, DEGREES, 20, PERCENT, True)
    drivebase.drive_for(FORWARD, object_distance, MM, 30, PERCENT, True)

