'''
Demonstrate subscribing to Thingy:52 temperature readings.
'''

import asyncio
import random

from aiothingy import Thingy52

async def main():
    # connect to thingy
    thingy = Thingy52()
    print('connecting...')
    await thingy.connect()
    print('connected')
    # set LED red to start
    await thingy.led.rgb(255, 0, 0)
    # event handler
    async def temperature_handler(event):
        print('{:.2f}°C'.format(event['data']))
    # subcribe to temperature events with handler
    await thingy.temperature.subscribe(temperature_handler)
    # run forever
    while True:
        await asyncio.sleep(1)

asyncio.run(main())