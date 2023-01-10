'''
Demonstrate subscribing to multiple sensor readings with one handler.
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
    async def event_handler(event):
        if event['type'] == 'temperature':
            print('Temperature: {:.2f}°C'.format(event['data']))
        elif event['type'] == 'pressure':
            print('Pressure: {:.2f} hPa'.format(event['data']))
    # subcribe to different events
    await thingy.temperature.subscribe(event_handler)
    await thingy.pressure.subscribe(event_handler)
    # run forever
    while True:
        await asyncio.sleep(1)

asyncio.run(main())