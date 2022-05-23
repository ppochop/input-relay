import asyncio
from math import floor
import socket

DEFAULT_PORT = 6899

MOUSE_MOVE_EV = 0x01
MOUSE_BTN_EV = 0x02

MOUSE_BTN_LEFT = 0x11
MOUSE_BTN_RIGHT = 0x12

BTN_PRESS = 0x01
BTN_RELEASE = 0x00

class Controller:
    def __init__(self, socket_type='INET'):
        if socket_type == 'INET':
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connect = self._connect_inet
        self._x = 0
        self._y = 0
    
    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @x.setter
    def x(self, value):
        self._x = floor(value*20+20)

    @y.setter
    def y(self, value):
        self._y = floor(value*20+20)


    def _connect_inet(self, ip, port=DEFAULT_PORT):
        try:
            self.sock.connect((ip, port))
            code = self.sock.recv(64)
            return code

        except:
            print(f'Failed to connect to {ip}:{port}')
            self.sock.close()
            raise Exception()

    def wait_for_accept(self):
        if self.sock.recv(64) != b'OK':
            raise ValueError('Expected \'OK\' message, got something else.')

    async def mouse_run(self):
        while True:
            if self.x or self.y:
                self.mouse_move(self.x, self.y)
            await asyncio.sleep(0.02)


    def mouse_move(self, X=0, Y=0):
        self.sock.send(bytes([MOUSE_MOVE_EV, X, Y]))
    
    def mouse_btn(self, btn, down):
        self.sock.send(bytes([MOUSE_BTN_EV, btn, down]))
