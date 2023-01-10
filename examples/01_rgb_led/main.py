'''
Demonstrate connecting to Thingy:52 and setting the LED to random colors.
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
    # run forever
    while True:
        # create random rgb color
        r = random.randrange(256)
        g = random.randrange(256)
        b = random.randrange(256)
        # update led
        await thingy.led.rgb(r, g, b)
        # sleep for 1 second
        await asyncio.sleep(0.5)

asyncio.run(main())