"""
ﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠ𝗙𝗥𝗢𝗡𝗧
    ╔════════════════════════════╗
    ║                            ║
    ║ﾠﾠﾠﾠﾠﾠ𝗔ﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠ𝗕ﾠﾠﾠﾠﾠﾠﾠ║
    ║ﾠﾠﾠﾠﾠﾠ𝗔ﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠ𝗕ﾠﾠﾠﾠﾠﾠﾠﾠ║
    ║ﾠﾠleft wheelﾠﾠﾠﾠright wheelﾠﾠ║
    ║ﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠ║
    ║ﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠ║
    ║ﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠ║
    ║ﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠ║
    ║ﾠﾠﾠﾠﾠ𝗖ﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠ𝗗ﾠﾠﾠﾠﾠﾠﾠ║
    ║ﾠﾠﾠﾠﾠ𝗖ﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠ𝗗ﾠﾠﾠﾠﾠﾠﾠﾠ║
    ║ﾠﾠfront motorﾠﾠﾠﾠback motorﾠﾠ║
    ║ﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠ║
    ║ﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠ║
@@ -19,9 +19,8 @@
    ╚════════════════════════════╝
ﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠﾠ𝗕𝗔𝗖𝗞
"""
from hub import port, motion_sensor
from hub import port, motion_sensor, sound
import runloop, motor, motor_pair, time, distance_sensor
from hub import sound
motor_pair.pair(motor_pair.PAIR_1, port.A, port.B)

# STRAIGHT LINE CODE ST
async def main():
    motion_sensor.reset_yaw
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 955, 1, velocity=450)
    await sound.beep(400, 500, 100)
    await runloop.sleep_ms(250)
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -105, 100, -100)
    await sound.beep(440, 500, 100)
    await runloop.sleep_ms(250)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 95, 1)
    await sound.beep(480, 500, 100)
    await runloop.sleep_ms(250)
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -20, 100, -100)
    await sound.beep(520, 500, 100)
    await motor.run_for_degrees(port.C, 2100, 1200)
    await sound.beep(560, 500, 100)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -100, 1, velocity=450)
    await runloop.sleep_ms(250)
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 27, 100, -100) #Rotate into a position where it is ready to complete tipping the scales
    await runloop.sleep_ms(250)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -185, 1, velocity=450)#move backwards, to set up for one way door
    await runloop.sleep_ms(250)
    await motor.run_for_degrees(port.D, 180, 750) # tip the scales
    await motor.run_for_degrees(port.D, -175, 600) #retract the arm back to og position so it doesn't get in the way
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 180, 1, velocity=450)#move forwards, pulling the cart out in the process. The car will be latched onto the one way gate
    await runloop.sleep_ms(250)
    #return
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -190, 100, -200) #rotate to set up b4 going home
    motor_pair.move(motor_pair.PAIR_1, 1, velocity=600)
    while distance_sensor.distance(port.F) > 125:
        continue
    motor_pair.stop(motor_pair.PAIR_1)
    print("Finish")
runloop.run(main()) #2266
