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
import runloop, motor, motor_pair, time
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
        await runloop.sleep_ms(10)
    motor.stop(port.A)
    motor.stop(port.B)
    
# PTS(Precise Turning Code here
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
            motor.stop(port.A)
            motor.stop(port.B)
            break
        if angle_diff > speed_reduce_angle_diff:
            motor.run(port.A, speed * turning_direction)
            motor.run(port.B, speed * turning_direction)
        else:
            motor.run(port.A, int(speed * turning_direction * speed_reduce_ratio))
            motor.run(port.B, int(speed * turning_direction * speed_reduce_ratio))
        await runloop.sleep_ms(1)

#  🡇 𝗖𝗢𝗗𝗘 𝗦𝗧𝗔𝗥𝗧𝗦 𝗛𝗘𝗥𝗘 🡇
async def main():
    #   🡇 𝗧𝗬𝗣𝗘 𝗜𝗡 𝗛𝗘𝗥𝗘 🡇
    print("started")
    
    print("ended")
runloop.run(main())
