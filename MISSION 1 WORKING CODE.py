import motor
import runloop
import motor_pair
from hub import port
from hub import sound
motor_pair.pair(motor_pair.PAIR_1, port.A, port.B)

motor.run_to_relative_position(port.C, 74, 167)
runloop.sleep_ms(200)


async def main():
    #🡇 𝗧𝗬𝗣𝗘 𝗜𝗡 𝗛𝗘𝗥𝗘 🡇
    print("started")
    
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 650, 0, velocity=670) #Move towards mission 1
    await runloop.sleep_ms(500)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -150, -2, velocity=475) #Move backwards to push the shovel
    await runloop.sleep_ms(100)
    await motor.run_for_degrees(port.C, -40, 200) #Raise attachment
    await runloop.sleep_ms(2000)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 70, 0, velocity=500) #Move forwards to pick up the shovel
    await motor.run_for_degrees(port.C, 67, 670) #Put attachment down
    await runloop.sleep_ms(200)
    await motor.run_for_degrees(port.C, -100, 200) #Raise attachment
    await sound.beep()
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -675, 0, velocity=670) #Move backwards to home


    
    
    
    
    """
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 25, 1000, -1000) # Turn to travel to next mission
    await runloop.sleep_ms(500)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 328, 0, velocity = 400) # Move to next mission
    await runloop.sleep_ms(1000)
    """
    #await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 125, 200, -200) #Turn so robot is backwards facing the mission
    #await runloop.sleep_ms(1000)
    #await motor_pair.move_for_degrees(motor_pair.PAIR_1, -20, 0, velocity = 400) #Reverse
    #await motor.run_for_degrees(port.D, 220, 400) #Put stick down
    #await runloop.sleep_ms(1000)
    ##await runloop.sleep_ms(1000)
    #await motor_pair.move_for_degrees(motor_pair.PAIR_1, -100, 0, velocity = 10000) #Reverse
    #await runloop.sleep_ms(1000)
    #await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 100, 1000, -1000 )
    #await motor.run_for_degrees(port.D, -220, 400) #Put stick up
    
    #await motor_pair.move_for_degrees(motor_pair.PAIR_1, 250, 0, velocity = 6700)
    #await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 50,200, -200)
    #await motor_pair.move_for_degrees(motor_pair.PAIR_1, 700, 0, velocity = 6700)
    
    print("ended")
runloop.run(main())
