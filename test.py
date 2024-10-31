import asyncio

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.board import Board

async def connect():
    opts = RobotClient.Options.with_api_key( 
        api_key='76xw3zzupfnrmauorjh5s6se944jobf1',
        api_key_id='1fc268d1-3c06-46a0-8db0-c5b499c0bdfe'
    )
    return await RobotClient.at_address('mypi-main.huogibm7zf.viam.cloud', opts)

async def main():
    machine = await connect()

    print('Resources:')
    print(machine.resource_names)
    
    # Note that the pin supplied is a placeholder. Please change this to a valid pin you are using.
    # local
    local = Board.from_robot(machine, "local")
    local_return_value = await local.gpio_pin_by_name("16")
    print(f"local gpio_pin_by_name return value: {local_return_value}")

    # Don't forget to close the machine when you're done!
    await machine.close()

if __name__ == '__main__':
    asyncio.run(main())
