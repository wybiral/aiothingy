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
        elif event['type'] == 'humidity':
            print('Humidity: {:.2f}%'.format(event['data']))
        elif event['type'] == 'air_quality':
            print('eCO2: {:.2f} ppm'.format(event['data']['co2']))
            print('TVOC: {:.2f} ppb'.format(event['data']['voc']))
    # subcribe to different events
    await thingy.temperature.subscribe(event_handler)
    await thingy.pressure.subscribe(event_handler)
    await thingy.humidity.subscribe(event_handler)
    await thingy.air_quality.subscribe(event_handler)
    # run forever
    while True:
        await asyncio.sleep(1)

asyncio.run(main())