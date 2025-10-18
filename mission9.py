from hub import port, motion_sensor
import runloop, motor, motor_pair
motor_pair.pair(motor_pair.PAIR_1, port.E, port.C)
motor.reset_relative_position
motion_sensor.reset_yaw
async def main():
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 120, -300, 300)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -105, 0, velocity=700)
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 130, -300, 300)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -300, 0, velocity=700)
runloop.run(main())
