'''
Demonstrate subscribing to Thingy:52 button events to turn LED on/off.
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
    # event handler
    async def button_handler(event):
        if event['data']:
            # button down, turn LED on
            await thingy.led.rgb(127, 0, 255)
        else:
            # button up, turn LED off
            await thingy.led.off()
    # subcribe to button events with handler
    await thingy.button.subscribe(button_handler)
    # run forever
    while True:
        await asyncio.sleep(1)

asyncio.run(main())