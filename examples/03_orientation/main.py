'''
Demonstrate subscribing to Thingy:52 orientation events to change LED color.
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
    async def orientation_handler(event):
        if event['data'] == 'up':
            await thingy.led.rgb(255, 0, 0)
        elif event['data'] == 'right':
            await thingy.led.rgb(255, 200, 0)
        elif event['data'] == 'down':
            await thingy.led.rgb(0, 255, 0)
        elif event['data'] == 'left':
            await thingy.led.rgb(0, 0, 255)
    # subcribe to orientation events with handler
    await thingy.orientation.subscribe(orientation_handler)
    # run forever
    while True:
        await asyncio.sleep(1)

asyncio.run(main())