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
from hub import port, motion_sensor
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
        correction = int((reference_yaw - current_yaw) * correction_speed)
        motor_speed = speed * direction - correction
        motor.run(port.A, motor_speed*-1)
        motor.run(port.B, motor_speed)
        print(motion_sensor.tilt_angles()[0])
        await runloop.sleep_ms(10)
    motor.stop(port.A)
    motor.stop(port.B)

# PTS(Precise Turning Code)
def cur_yaw_topview():
    return motion_sensor.tilt_angles()[0] * -1
def cur_yaw_in_3600():
    return (cur_yaw_topview() + 3600) % 3600
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

async def turning_for_degree_v2(degree:int, speed:int=200, ref_yaw:int|None=None, turning_direction:int=1, speed_reduce_angle_diff:int=100, speed_reduce_ratio:float=0.1, tolerance=2):

    """

    Turning for given degree and direction.

    Parameters

    ----------

    degree : int

        decidegree for turning.

        Positive range mean clockwise turning. (yaw from tilt_angles() will goes negative)

        Negative range mean counter clockwise turning. (yaw from tilt_angles() will goes positive)

        Range: -3600 to 3600

    speed : int, optional

        moving speed.

        Default: 200

    ref_yaw : int|None, optional

        If not given, current yaw will use.

        If 0 given, robot align to first position angle when it power on.

        Range: 0 to 3600

        Default: None, current yaw

    turning_direction : int, optional

        Default turning direction. It will changed by degree value.

        1 mean counter clockwise turning

        -1 mean clockwise turning

        Default: 1

    speed_reduce_angle_diff : int, optional

        Tuning parameter of speed reducing beginning angle diff to target yaw.

        Default: 100

    speed_reduce_ratio : float, optional

        Tunning parameter of speed reducing ration near target yaw.

        Default: 0.2

    tolerance : int, optional

        Stop condition tolerance of angle diff.

        Default : 2

    Raises

    ------

    ValueError

        If degree is not in range -3600 to 3600

    """

    if abs(degree) > 3600:

        raise ValueError

    # Depends on motor position

    if degree >= 0:

        turning_direction *= -1

    else:

        turning_direction *= 1

    if ref_yaw == None:

        ref_yaw = cur_yaw_in_3600()

    target_yaw = (ref_yaw + degree) % 3600

    while True:

        angle_diff = abs(target_yaw - cur_yaw_in_3600())

        if angle_diff <= tolerance:

            motor.stop(port.C)

            motor.stop(port.E)

            break

        if angle_diff > speed_reduce_angle_diff:

            motor.run(port.C, speed * turning_direction)

            motor.run(port.E, speed * turning_direction)

        else:

            motor.run(port.C, int(speed * turning_direction * speed_reduce_ratio))

            motor.run(port.E, int(speed * turning_direction * speed_reduce_ratio))

        await runloop.sleep_ms(1)

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
    print("start")
runloop.run(main())
