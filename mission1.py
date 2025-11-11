from hub import port, motion_sensor
import runloop, motor, motor_pair
motor_pair.pair(motor_pair.PAIR_1, port.E, port.C)
motion_sensor.reset_yaw
motion_sensor.get_yaw_face
print("part 1")

# ---------------- Orientation Helpers ----------------
# Defines normal angles that the robot should move
def _norm_angle(angle):
    """Normalize angle to range [-180, 180]."""
    while angle > 180:
        angle -= 360
    while angle < -180:
        angle += 360
    return angle
# Gets the current yaw angle
def get_yaw():
    """Return current yaw angle if available (SPIKE Prime Hub)."""
    if hasattr(motion_sensor, "get_yaw_face"):
        return motion_sensor.get_yaw_face()
    return None
#  The robot turns the desired angle based on the current yaw and changes to the desired yaw within your set tolerance.
async def turn_relative(degrees, speed=300, tolerance=2):
    """Turn the robot by a relative yaw using the hub motion sensor.

    degrees: desired change in heading (+ clockwise or counter‑clockwise depending on hub convention).
    speed: motor speed magnitude for tank turn.
    tolerance: acceptable yaw error to stop.

    Strategy: reset yaw, then perform small tank turn bursts until target reached.
    Adjust sign if your robot turns the opposite way.
    """
    # Reset yaw to start from 0 for a relative turn.
    if hasattr(motion_sensor, "reset_yaw"):
        motion_sensor.reset_yaw(0)
    target = _norm_angle(degrees)
    # Decide turning direction; if your hub reports opposite sign, flip dir_sign.
    while True:
        current = get_yaw()
        if current is None:
            break  # Sensor not available; abort.
        error = _norm_angle(target - current)
        if abs(error) <= tolerance:
            break
        # Choose direction: positive error -> turn one way.
        # Empirically you may need to invert. Start with this mapping:
        dir = 1 if error > 0 else -1
        # Short controlled burst: larger error -> more degrees.
        burst_degrees = 40 if abs(error) > 30 else 20
        # Tank turn: opposite motor velocities.
        await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, burst_degrees * dir, speed * dir, -speed * dir)
        # brief pause lets sensor update
        await runloop.sleep_ms(30)  
    # Small brake / settle pause
    await runloop.sleep_ms(100)
#Main code
async def main():
    print(
    """The position of the robot should be the right wheel should be just covering the second line from the right 
    of the mission start and the fork all the way back | Mission 1""")
    motion_sensor.reset_yaw(0)
    motor.reset_relative_position(port.A, 0)
    # Move the fork down to the position
    await motor.run_for_degrees(port.A, 188, 360) 

    # Move the robot to the first mission
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -610, 0, velocity=610) 
    # if motion_sensor.get_yaw_face() > 0:
    print("thousand years of")
    # Turn to face the first mission and sweep to the left
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 184, -250, 250) 
    # Turn to sweep to the right
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -100, -250, 250) 
    # Back up to let the brush settle
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 100, 0, velocity=200) 
    # Turn to face the mission after sweeping
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 30, -250, 250) 
    # Wait for the brush to stop moving
    await runloop.sleep_ms(300)
    # Thrust
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -100, 0, velocity=125) 
    # Raise the fork up to pick up the brush
    await motor.run_for_degrees(port.A, -103, 360) 
    
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 200, 0, velocity=600)
    # Lower the fork down to pick up the brush
    await motor.run_for_degrees(port.A, 85, 160)
    # Turn to sweep to the right
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -550, 00, 500)
    #do this cool turn to move out and face path to go to center
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -300, 0, velocity=600)
    # turn to face colluseum next to fossil
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -120, -500, 500)
    await runloop.sleep_ms(500) 
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -30, 0, velocity=610)
    # release
    await motor.run_for_degrees(port.A, 80, 360) 
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 50, 0, velocity=610)
    # release
    await motor.run_for_degrees(port.A, -80, 360) 
    
    # Example orientation adjustment: turn ~90 degrees at end
    await turn_relative(90, speed=300, tolerance=3)
runloop.run(main())
