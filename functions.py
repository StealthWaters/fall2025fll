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
# STRAIGHT LINE CODE END
