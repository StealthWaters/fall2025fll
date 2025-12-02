from hub import port, motion_sensor
import runloop, motor, motor_pair, time
motor_pair.pair(motor_pair.PAIR_1, port.E, port.C)
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

        left_speed, right_speed = (speed * direction - correction)*-1, speed * direction + correction

        motor.run(port.C, left_speed)
        motor.run(port.E, right_speed)

        await runloop.sleep_ms(10)

    motor.stop(port.C)
    motor.stop(port.E)
# Precise Turning Code (PTS)
def cur_yaw_topview():
    return motion_sensor.tilt_angles()[0] * -1

def cur_yaw_in_3600():
    return (cur_yaw_topview() + 3600) % 3600

async def main():
    # The position of the robot should be the right wheel should be just covering the 3rd line from the right of the mission start and the fork all the way back
    await move_straight_for_time(1000)
    await motor.run_for_degrees(port.A, 240, 360)
    await move_straight_for_time(200, 400, -1)
    await motor.run_for_degrees(port.A, -193, 360)
    # continue

    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 110, -250, 250)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -220, 0, velocity=500)
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -95, -250, 250)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -400, 0, velocity=250)
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 5, -250, 250)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 300, 0, velocity=500)
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 100, -250, 250)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 600, 0, velocity=500)

runloop.run(main())
