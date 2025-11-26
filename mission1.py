# CODE RELIES ON PORTS "C" AND "E"
from hub import port, motion_sensor
import runloop, motor, time
motor.reset_relative_position(port.A, 0)
motion_sensor.reset_yaw
#SIX
#SEVEN
# STRAIGHT LINE CODE START (SLC) move_straight_for_time(4000) <-- Pres Ctrl+Left_Arrow twice to copy sample.
async def move_straight_for_time(duration:int, speed:int=400, direction:int=1, reference_yaw:int|None=None, correction_speed:float=0.7):
    """
    Moves FRONT or BACK for specific TIME

    PARAMETERS
    -

    duration ( Integer ) --> REQUIRED 
        Milisecond time for moving
    speed ( Integer )
        Default = 400
    direction ( Integer )
        Default = 1 [FORWARD]
    reference_yaw ( Integer )
        Default = None [Uses CURRENT]
    correction_speed ( Float )
        Default = 0.7

        LOWER makes SLOW TURN, more prone to FALLING OFF PATH.

        HIGHER makes FASTER but LESS ACCURATE correction.

    await move_straight_for_time(1500)
    -
    ^ A 4 second sample movement code set to defaults
    """

    tick_until = time.ticks_ms() + duration

    if reference_yaw == None:
        reference_yaw = motion_sensor.tilt_angles()[0]

    while time.ticks_ms() < tick_until:
        current_yaw = motion_sensor.tilt_angles()[0]
        correction = int((reference_yaw - current_yaw) * correction_speed)

        left_speed, right_speed = (speed * direction - correction)*-1, speed * direction - correction

        motor.run(port.C, left_speed)
        motor.run(port.E, right_speed)

        await runloop.sleep_ms(10)
    
    motor.stop(port.C)
    motor.stop(port.E)
# Precise Turning Code (PTS)
async def turning_for_degree(degree:int, speed:int=200, ref_yaw:int|None=None, correction_factor:float=0.1, tolerance=2):
    """
    Turning for given degree and direction.

    Parameters
    ----------
    degree : int
        decidegree for turning.
        Positive range mean clockwise turning. (yaw will goes negative)
        Negative range mean counter clockwise turning. (yaw will goes positive)
        Turning angle should less than 180 degree, for both direction.
        Range: -1800 to 1800
    speed : int, optional
        moving speed.
        Default: 200
    ref_yaw : int|None, optional
        Target yaw. If not given, current yaw will use.
        If 0 given, robot align to first position angle.
        Default: None, current yaw
    correction_factor : float, optional
        Tunning parameter for amount of control.
        Default:0.2

    Raises
    ------
    ValueError
        If degree is not in range -1800to1800
    """
    if abs(degree) > 1800:
        raise ValueError

    if degree > 0:
        turning_direction = -1
    else:
        turning_direction = 1

    if ref_yaw == None:
        ref_yaw = motion_sensor.tilt_angles()[0]

    # Change from -180to180 to 0to360
    ref_yaw = (ref_yaw - 3600) % 3600
    target_yaw = (ref_yaw - degree) % 3600

    while True:
        angle_diff = abs(abs((motion_sensor.tilt_angles()[0] - 3600)%3600) - abs(target_yaw))

        #motor.run(port.C, speed * turning_direction)
        #motor.run(port.E, speed * turning_direction)
        if angle_diff > 100:
            motor.run(port.C, speed * turning_direction)
            motor.run(port.E, speed * turning_direction)
        else:
            motor.run(port.C, int(speed * turning_direction * correction_factor))
            motor.run(port.E, int(speed * turning_direction * correction_factor))

        if angle_diff <= tolerance:
            break

        await runloop.sleep_ms(1)

    motor.stop(port.C)
    motor.stop(port.E)
async def main():
    #-860 is exactly 90 degrees to the left with current code in turning_for_degree

    await motor.run_for_degrees(port.A, 185, 360) #move arm DOWN
    await move_straight_for_time(2100) #move forward
    await turning_for_degree(-1290) # turn to shovel off half
    await turning_for_degree(600) # turn to shovel off other half (sweep)
    await runloop.sleep_ms(100) # wait
    await move_straight_for_time(250, 400, -1) # back up
    await runloop.sleep_ms(100) # wait
    await turning_for_degree(-185) #align to face
    await runloop.sleep_ms(500) # wait
    await move_straight_for_time(375) # thrust
    await runloop.sleep_ms(500)
    await motor.run_for_degrees(port.A, -40, 360) #move arm UP
    await move_straight_for_time(400, 400, -1) # back up carrying shovel
    await turning_for_degree(-860) # face home
    await move_straight_for_time(1300, 400, 1) # return

runloop.run(main())
