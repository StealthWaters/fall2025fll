from hub import port
import runloop, motor, motor_pair
motor_pair.pair(motor_pair.PAIR_1, port.E, port.C)

async def main():
    # The position of the robot should be the right wheel should be just covering the 3rd line from the right of the mission start and the fork all the way back
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -380, 0, velocity=500)
    await motor.run_for_degrees(port.A, 240, 360)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 100, 0, velocity=500)    
    await motor.run_for_degrees(port.A, -193, 360)
    # continue

    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 94, -250, 250)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -220, 0, velocity=500)
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -95, -250, 250)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -400, 0, velocity=250)
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 5, -250, 250)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 300, 0, velocity=500)
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 100, -250, 250)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 500, 0, velocity=500)

runloop.run(main())
