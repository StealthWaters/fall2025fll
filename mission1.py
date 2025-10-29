from hub import port
import runloop, motor, motor_pair
motor_pair.pair(motor_pair.PAIR_1, port.E, port.C)

print("part 1")
async def main():
    print("maybe")
# Align the bulging edge part of the right side gymbal wheel to the third line right side of the left launch pad.
# Mission 1
    await motor.run_for_degrees(port.A, 190, 360) # Move the fork down to the position

    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -610, 0, velocity=500) # Move the robot to the first mission
    print("*moans*")
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 177, -250, 250) # Turn to face the first mission and sweep to the left
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -93, -250, 250) # Turn to sweep to the right
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 100, 0, velocity=200) # Back up to let the brush settle
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 35, -250, 250) # Turn to face the mission after sweeping
    await runloop.sleep_ms(300) # Wait for the brush to stop moving
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -100, 0, velocity=125) # Thrust
    await motor.run_for_degrees(port.A, -103, 360) # Raise the fork up to pick up the brush
    await motor.run_for_degrees(port.A, 100, 6000)
    await motor.run_for_degrees(port.A, -173, 660) # Raise the fork up to pick up the brush
runloop.run(main())
