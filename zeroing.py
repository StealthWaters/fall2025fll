from hub import port
import motor
import motor_pair
import runloop

async def main():
    await motor.run_to_absolute_position(port.C, 0, 100)
    await motor.run_to_absolute_position(port.D, 0, 100)
runloop.run(main())
