from hub import light_matrix, port
import runloop, motor, motor_pair
motor_pair.pair(motor_pair.PAIR_1, port.E, port.C)

async def main():
    # write your code here
    # await motor.run_for_degrees(port.A, 190, 360) # Raise the fork up to set up for pushing the lever
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -750, 0, velocity=670)
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 30, -250, 250) # Turn to sweep to the right
    await motor.run_for_degrees(port.A, 190, 360) # Raise the fork up to set up for pushing the lever
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 30, -250, 250) # Turn to sweep to the right
#    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 76, -250, 250) # Turn to face the mission after sweeping

    # await motor_pair.move_for_degrees(motor_pair.PAIR_1, 100, 0, velocity=200) # Move forward to release the boulders
    #await motor_pair.move_for_degrees(motor_pair.PAIR_1, 100, 0, velocity=200) # Back up
    
runloop.run(main())
