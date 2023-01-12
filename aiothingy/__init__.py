from bleak import BleakClient
import struct

class Thingy52:

    def __init__(self, address='D7:FE:7E:D2:E2:73'):
        self.client = BleakClient(address)
        self.name = Name(self)
        self.temperature = Temperature(self)
        self.pressure = Pressure(self)
        self.humidity = Humidity(self)
        self.air_quality = AirQuality(self)
        self.color = Color(self)
        self.led = LED(self)
        self.button = Button(self)
        self.motion_config = MotionConfig(self)
        self.orientation = Orientation(self)
        self.step_counter = StepCounter(self)
        self.raw = Raw(self)
        self.euler = Euler(self)
        self.heading = Heading(self)
        self.gravity = Gravity(self)

    async def connect(self):
        await self.client.connect()

    async def disconnect(self):
        await self.client.disconnect()

    async def read(self, uuid):
        return await self.client.read_gatt_char(uuid)

    async def write(self, uuid, data, response=True):
        await self.client.write_gatt_char(uuid, data, response=response)


class Characteristic:

    def __init__(self, thingy):
        self.thingy = thingy
        self.subscribers = {}

    async def read(self):
        data = await self.thingy.read(self.uuid)
        return self.decode(data)

    async def write(self, value):
        data = self.encode(value)
        await self.thingy.write(self.uuid, data)

    async def subscribe(self, callback, *args, **kwargs):
        if len(self.subscribers) == 0:
            await self.thingy.client.start_notify(self.uuid, self.__notify)
        self.subscribers[callback] = (args, kwargs)

    async def __notify(self, char, data):
        value = self.decode(data)
        event = {
            'type': self.name,
            'data': value,
        }
        for callback, (args, kwargs) in self.subscribers.items():
            await callback(event, *args, **kwargs)


class Name(Characteristic):

    name = 'name'
    uuid = 'ef680101-9b35-4933-9b10-52ffa9740042'

    def encode(self, data):
        return data.encode()

    def decode(self, data):
        return data.decode()


class Temperature(Characteristic):

    name = 'temperature'
    uuid = 'ef680201-9b35-4933-9b10-52ffa9740042'

    def decode(self, data):
        i, d = struct.unpack('bB', data)
        return i + (d / 100)


class Pressure(Characteristic):

    name = 'pressure'
    uuid = 'ef680202-9b35-4933-9b10-52ffa9740042'

    def decode(self, data):
        i, d = struct.unpack('<IB', data)
        return i + (d / 100)


class Humidity(Characteristic):

    name = 'humidity'
    uuid = 'ef680203-9b35-4933-9b10-52ffa9740042'

    def decode(self, data):
        x = struct.unpack('B', data)
        return x[0]


class AirQuality(Characteristic):

    name = 'air_quality'
    uuid = 'ef680204-9b35-4933-9b10-52ffa9740042'

    def decode(self, data):
        co2, voc = struct.unpack('<HH', data)
        return {'co2': co2, 'voc': voc}


class Color(Characteristic):

    name = 'color'
    uuid = 'ef680205-9b35-4933-9b10-52ffa9740042'

    def decode(self, data):
        r, g, b, c = struct.unpack('<HHHH', data)
        return {'r': r, 'g': g, 'b': b, 'c': c}


class LED(Characteristic):

    name = 'led'
    uuid = 'ef680301-9b35-4933-9b10-52ffa9740042'
    colors = ['red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white']

    def encode(self, x):
        data = None
        if x['mode'] == 'off':
            return struct.pack('<B', 0)
        elif x['mode'] == 'constant':
            r = x['r']
            g = x['g']
            b = x['b']
            return struct.pack('<BBBB', 1, r, g, b)
        elif x['mode'] == 'breathe':
            color = x['color']
            if isinstance(color, str):
                color = self.colors.index(color) + 1
            intensity = x['intensity']
            delay = x['delay']
            return struct.pack('<BBBH', 2, color, intensity, delay)
        elif x['mode'] == 'oneshot':
            color = x['color']
            if isinstance(color, str):
                color = self.colors.index(color) + 1
            intensity = x['intensity']
            return struct.pack('<BBB', 3, color, intensity)
        raise ValueError('invalid mode for led')

    def decode(self, data):
        if data[0] == 0x00:
            return {'mode': 'off'}
        elif data[0] == 0x01:
            x = struct.unpack('<BBBB', data[0:4])
            return {'mode': 'constant', 'r': x[1], 'g': x[2], 'b': x[3]}
        elif data[0] == 0x02:
            x = struct.unpack('<BBBH', data[0:5])
            return {
                'mode': 'breathe',
                'color': self.colors[x[1] - 1],
                'intensity': x[2],
                'delay': x[3],
            }
        elif data[0] == 0x03:
            x = struct.unpack('<BBB', data[0:3])
            return {
                'mode': 'oneshot',
                'color': self.colors[x[1] - 1],
                'intensity': x[2],
            }

    async def off(self):
        await self.write({'mode': 'off'})

    async def rgb(self, r, g, b):
        await self.write({'mode': 'constant', 'r': r, 'g': g, 'b': b})

    async def breathe(self, color='white', intensity=100, delay=500):
        await self.write({
            'mode': 'breathe',
            'color': color,
            'intensity': intensity,
            'delay': delay,
        })

    async def oneshot(self, color='white', intensity=100):
        await self.write({
            'mode': 'oneshot',
            'color': color,
            'intensity': intensity,
        })


class Button(Characteristic):

    name = 'button'
    uuid = 'ef680302-9b35-4933-9b10-52ffa9740042'

    def decode(self, data):
        x = struct.unpack('B', data)
        return x[0] > 0


class MotionConfig(Characteristic):

    name = 'motion_config'
    uuid = 'ef680401-9b35-4933-9b10-52ffa9740042'

    def decode(self, data):
        x = struct.unpack('<HHHHB', data)
        return {
            'step_interval': x[0],
            'temp_comp_interval': x[1],
            'magnet_comp_interval': x[2],
            'motion_frequency': x[3],
            'wake_on_motion': x[4],
        }


class Orientation(Characteristic):

    name = 'orientation'
    uuid = 'ef680403-9b35-4933-9b10-52ffa9740042'

    def decode(self, data):
        x = struct.unpack('B', data)
        names = ['left', 'up', 'right', 'down']
        return names[x[0]]


class StepCounter(Characteristic):

    name = 'step_counter'
    uuid = 'ef680405-9b35-4933-9b10-52ffa9740042'

    def decode(self, data):
        count, time = struct.unpack('<II', data)
        return {
            'count': count,
            'time': time,
        }


class Raw(Characteristic):

    name = 'raw'
    uuid = 'ef680406-9b35-4933-9b10-52ffa9740042'

    def decode(self, data):
        s = struct.unpack('<hhhhhhhhh', data)
        return {
            'accelerometer': {
                'x': s[0] / 1024,
                'y': s[1] / 1024,
                'z': s[2] / 1024,
            },
            'gyroscope': {
                'x': s[3] / 256,
                'y': s[4] / 256,
                'z': s[5] / 256,
            },
            'compass': {
                'x': s[6] / 16,
                'y': s[7] / 16,
                'z': s[8] / 16,
            },
        }


class Euler(Characteristic):

    name = 'euler'
    uuid = 'ef680407-9b35-4933-9b10-52ffa9740042'

    def decode(self, data):
        roll, pitch, yaw = struct.unpack('<iii', data)
        return {
            'roll': roll / 65536,
            'pitch': pitch / 65536,
            'yaw': yaw / 65536,
        }


class Heading(Characteristic):

    name = 'heading'
    uuid = 'ef680409-9b35-4933-9b10-52ffa9740042'

    def decode(self, data):
        x = struct.unpack('<i', data)
        return x[0] / 65536


class Gravity(Characteristic):

    name = 'gravity'
    uuid = 'ef68040a-9b35-4933-9b10-52ffa9740042'

    def decode(self, data):
        x, y, z = struct.unpack('<fff', data)
        return {
            'x': x,
            'y': y,
            'z': z,
        }
