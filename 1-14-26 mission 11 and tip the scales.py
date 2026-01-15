"""
ﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠ𝗙𝗥𝗢𝗡𝗧
    ╔════════════════════════════╗
    ║                            ║
    ║ﾠﾠﾠﾠﾠﾠ𝗔ﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠ𝗕ﾠﾠﾠﾠﾠﾠﾠﾠ║
    ║ﾠﾠleft wheelﾠﾠﾠﾠright wheelﾠﾠ║
    ║ﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠ║
    ║ﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠ║
    ║ﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠ║
    ║ﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠ║
    ║ﾠﾠﾠﾠﾠ𝗖ﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠ𝗗ﾠﾠﾠﾠﾠﾠﾠﾠ║
    ║ﾠﾠfront motorﾠﾠﾠﾠback motorﾠﾠ║
    ║ﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠ║
    ║ﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠ║
    ║ﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠ║
    ║ﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠ║
    ║ﾠﾠﾠﾠﾠﾠﾠ𝗘ﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠ𝗙ﾠﾠﾠﾠﾠﾠﾠﾠ║
    ║ﾠﾠﾠﾠnothingﾠﾠﾠﾠrange sensorﾠﾠ║
    ╚════════════════════════════╝
ﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠ𝗕𝗔𝗖𝗞
"""
from hub import port, motion_sensor, sound
import runloop, motor, motor_pair, time, distance_sensor
motor_pair.pair(motor_pair.PAIR_1, port.A, port.B)

# STRAIGHT LINE CODE START (SLC)
# move_straight_for_time(4000) <-- this moves forward for 4000ms(aka 4 sec) at speed 400(default) and with everything else default
motion_sensor.reset_yaw

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
        correction = int((reference_yaw - abs(current_yaw)) * correction_speed)
        motor_speed = speed * direction - correction
        motor.run(port.A, motor_speed*-1)
        motor.run(port.B, motor_speed)
    motor.stop(port.A)
    motor.stop(port.B)
    await runloop.sleep_ms(10)

# PTS(Precise Turning Code)
def cur_yaw_in_3600():
    return (motion_sensor.tilt_angles()[0] + 3600)% 3600

def angle_error(target, current):
    # signed shortest-path error: -1800 ~ +1800
    return (target - current + 5400) % 3600 - 1800

async def turning_for_degree_v3(degree:int, direction:int=-1, speed:int=150, reference_yaw:int|None=None, angle_diff_to_reduce_speed:int=100, speed_reduce_ratio:float=0.1, tolerance=20):
    """

    ═══════════════════

    Turns for a set amount of degrees

    PARAMETERS:
    -

    degree ( Integer ) --> REQUIRED
        Turns this amount of degrees, use direction to change the turning direction instead of using negatives
        in 10s, so a 90 degree turn would be 900

    direction ( Integer )
        Default = -1
        -1 is turning clockwise, 1 is turning counter-clockwise

    speed ( Integer )
        Default = 150

    reference_yaw ( Integer )
        Default = None
        None uses current yaw to turn, otherwise uses that as baseline yaw

    angle_diff_to_reduce_speed ( Integer )
        Default = 100
        Angle difference to start reducing speed

    speed_reduce_ratio ( Float )
        Default = 0.1
        Ratio at which to reduce the speed

    tolerance ( Integer )
        Default = 30
        Gives a buffer amount to turn to, as the wheels aren't all accurate

    await turning_for_degree_v3(900)
    sample code set to 90 degree clockwise turn, everything else defaulted

    Raises

    ------

    ValueError

        If degree is not in range 1 to 3599(aka 3600)
    """

    if degree >= 3600 or degree == 0:
        raise ValueError

    if reference_yaw == None:
        reference_yaw = cur_yaw_in_3600()

    # calculate target yaw
    if direction == 1:
        target_yaw = (reference_yaw + degree) % 3600
    else:
        target_yaw = (reference_yaw - degree) % 3600

    while True:
        current_yaw = cur_yaw_in_3600()
        error = angle_error(target_yaw, current_yaw)
        print(cur_yaw_in_3600())
        # stop if within tolerance
        if abs(error) <= tolerance:
            break

        # slow down near target
        turn_speed = speed
        if abs(error) < angle_diff_to_reduce_speed:
            turn_speed = int(speed * speed_reduce_ratio)

        # motor direction from error sign
        motor_speed_left = turn_speed if error > 0 else -turn_speed
        motor_speed_right = motor_speed_left

        # run motors
        motor.run(port.A, motor_speed_left)
        motor.run(port.B, motor_speed_right)

    # stop motors
    motor.stop(port.A)
    motor.stop(port.B)

async def move_straight_until_range(rangesensorrange:int, speed:int=400, direction:int=1, reference_yaw:int|None=None, correction_speed:float=0.7):
    """
    Moves FRONT or BACK until distance sensor reaches a certain amount

    PARAMETERS
    -

    distance ( Integer ) --> REQUIRED
        Until the distance sensor reaches this amount

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
    await move_straight_until_range(100)
    -
    ^ A sample movement code set to 100
    """
    if reference_yaw == None:
        reference_yaw = motion_sensor.tilt_angles()[0]
    print(rangesensorrange)
    while rangesensorrange < distance_sensor.distance(port.F):
        print("1")
        print(rangesensorrange)
        current_yaw = motion_sensor.tilt_angles()[0]
        correction = int((reference_yaw - current_yaw) * correction_speed)
        motor_speed = speed * direction - correction
        motor.run(port.A, motor_speed*-1)
        motor.run(port.B, motor_speed)
        await runloop.sleep_ms(100)
    motor.stop(port.A)
    motor.stop(port.B)
async def acode_to_move_percentage_wise(rotation_percentage:int=300, speed:int=300):
    """
    Move percentage wise.
    -
    Pick a percentage. If the number is below 10 (10% rotation; up to 9 rotations),
    then it defaults to number of full rotations.
    """
    motor.run_for_degrees(port.A, int(rotation_percentage*-1), speed)
    motor.run_for_degrees(port.B, int(rotation_percentage), speed)

#🡇 𝗖𝗢𝗗𝗘 𝗦𝗧𝗔𝗥𝗧𝗦 𝗛𝗘𝗥𝗘 🡇
async def main():
    #🡇 𝗧𝗬𝗣𝗘 𝗜𝗡 𝗛𝗘𝗥𝗘 🡇
    print("started")
    motion_sensor.reset_yaw
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 955, 1, velocity=450)
    await sound.beep(400, 500, 100)
    await runloop.sleep_ms(250)
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -105, 100, -100)
    await sound.beep(440, 500, 100)
    await runloop.sleep_ms(250)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 95, 1)
    await sound.beep(480, 500, 100)
    await runloop.sleep_ms(250)
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -20, 100, -100)
    await sound.beep(520, 500, 100)
    await motor.run_for_degrees(port.C, 2100, 1200)
    await sound.beep(560, 500, 100)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -100, 1, velocity=450)
    await runloop.sleep_ms(250)
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 27, 100, -100) #Rotate into a position where it is ready to complete tipping the scales
    await runloop.sleep_ms(250)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -185, 1, velocity=450)#move backwards, to set up for one way door
    await runloop.sleep_ms(250)
    await motor.run_for_degrees(port.D, 180, 750) # tip the scales
    await motor.run_for_degrees(port.D, -175, 600) #retract the arm back to og position so it doesn't get in the way
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 180, 1, velocity=450)#move forwards, pulling the cart out in the process. The car will be latched onto the one way gate
    await runloop.sleep_ms(250)
    #return
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -190, 100, -200) #rotate to set up b4 going home
    motor_pair.move(motor_pair.PAIR_1, 1, velocity=600)
    while distance_sensor.distance(port.F) > 125:
        continue
    motor_pair.stop(motor_pair.PAIR_1)
    print("Finish")
runloop.run(main()) #2266
