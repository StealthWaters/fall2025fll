
from hub import port
import motor
import motor_pair
import runloop


motor_pair.pair(motor_pair.PAIR_1, port.A, port.B)


async def main():
    # write your code here
    
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 1005, 0, velocity=500) # Move straight to mission
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 94, 200, -200) # Turn to mission
    # Put flag down here
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 282, 0, velocity=400) #
    await motor.run_for_degrees(port.C, -200, 300) #
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 255, 0, velocity=6700) # Move straight to mission
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -40, 100, -100)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 356, 0, velocity=6700) # Move straight to mission
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 41, 100, -100)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 255, 0, velocity=6700) # Move straight to mission
    await motor.run_for_degrees(port.D, -73, 300) #
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 48, 100, -100)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 670, 0, velocity=500) # Move straight to mission
    await runloop.sleep_ms(350)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -200, 0, velocity=4000) # Move straight to mission
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -45, 100, -100)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 300, 0, velocity=2000) # Move straight to mission
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 55, 100, -100)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 1000, 0, velocity=2000) # Move straight to mission


    """
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 80, 200, -200)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 815, 0, velocity=6700) # Move straight to home
    """
runloop.run(main()) 
