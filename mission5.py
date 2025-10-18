from hub import port, motion_sensor
import runloop, motor, motor_pair
motor_pair.pair(motor_pair.PAIR_1, port.E, port.C)
motor.reset_relative_position
motion_sensor.reset_yaw

async def main():
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -900, 0, velocity=700)
    print("1")
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 60, -150, 250)
    print("2")
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -130, 0, velocity=700)
    print("3")
    await motor.run_for_degrees(port.A, 197, 360) # moving code for arm
    print("4")
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -120, -300, 300)

    print("Soemfopisdhjfd")
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 180, -0, 700)#turn
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -350, 0, velocity=700)
    print("home")
    #await motor.run_for_degrees(port.A, 0, 360)

runloop.run(main())

#the robot has some issues:
#not including or limited to austim 
