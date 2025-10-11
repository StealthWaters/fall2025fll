from hub import port, motion_sensor
import runloop, motor, motor_pair
motion_sensor.reset_yaw(0)
motor_pair.pair(motor_pair.PAIR_1, port.E, port.C)

async def main():
    # The position of the robot should be the right wheel should be just covering the 3rd line from the right of the mission start and the fork all the way back
    
    await motor.run_for_degrees(port.A, 193, 360)

    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -530, 0, velocity=500)
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 175, -250, 250)
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -80, -250, 250)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 100, 0, velocity=200)
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 30, -250, 250)

    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -100, 0, velocity=125)
    await motor.run_for_degrees(port.A, -90, 360)
    # Turns right

runloop.run(main())
