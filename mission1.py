from hub import light_matrix, port
import runloop, motor, motor_pair
motor_pair.pair(motor_pair.PAIR_1, port.E, port.C)

async def main():
    # The position of the robot should be the right wheel should be just covering the 3rd line from the right of the mission start and the fork all the way back

    await motor.run_for_degrees(port.A, 193, 360)

    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -535, 0, velocity=500)
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 177, -250, 250)
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -93, -250, 250)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 100, 0, velocity=200)
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 35, -250, 250)
    await runloop.sleep_ms(300)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -100, 0, velocity=125)
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -15, -250, 250)
    await motor.run_for_degrees(port.A, -200, 600000)

    # Turn right


runloop.run(main())
