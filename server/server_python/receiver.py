import secrets
import socket
import string
import uinput

DEFAULT_PORT = 6899
EVENTS = [
   uinput.REL_X,
   uinput.REL_Y,
   uinput.BTN_LEFT,
   uinput.BTN_RIGHT,
]
MOUSE_MOVE_EV = 0x01
MOUSE_BTN_EV = 0x02

EVS = {
    MOUSE_MOVE_EV: 'Mouse move event',
    MOUSE_BTN_EV: 'Mouse button event'
}

MID_VALUE = 20

class Receiver():
    def __init__(self, socket_type='INET', ip='', debug=False):
        if socket_type == 'INET':
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._standby = self._standby_inet
        self.conn = None
        self.ip = ip
        if debug:
            self._action = self._action_print
            self.device = None
        else:
            self._action = self._action_uinput
            self.device = uinput.Device(EVENTS)
    
    def destroy(self):
        self.sock.close()
        self.conn.close()
        if self.device:
            self.device.destroy()

    def _auth_string(self):
        alphabet = string.ascii_uppercase + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(5))

    def _auth(self, addr):
        '''
        Authentication is based on the trust of the connecting user's
        physical access to the server's machine; susceptible to MitM
        '''
        nonce = self._auth_string()
        self.conn.send(nonce.encode('ASCII'))
        print(f'Inbound connection from {addr}.')
        return input('Type in the received string: ') == nonce

    def _standby_inet(self, port=DEFAULT_PORT):
        self.sock.bind((self.ip, port))
        self.sock.listen()

    def standby(self):
        self._standby()
        self.conn, addr = self.sock.accept()
        self.sock.close()
        if not self._auth(addr):
            raise ConnectionRefusedError('Connection refused, shutting down.')
        self.conn.send(b'OK')

    def _action_print(self, event_type, event_arg1, event_arg2):
        print(f'Received \'{EVS[event_type]}\' with arg1={event_arg1} and arg2={event_arg2}')

    def _action_uinput(self, event_type, event_arg1, event_arg2):
        match event_type:
            case 0x01: # MOUSE_MOVE_EV
                self.device.emit(uinput.REL_X, event_arg1 - MID_VALUE, syn=False)
                self.device.emit(uinput.REL_Y, -(event_arg2 - MID_VALUE))       
            case 0x02: # MOUSE_BTN_EV
                match event_arg1:
                    case 0x11: # Left mouse button
                        self.device.emit(uinput.BTN_LEFT, event_arg2)
                    case 0x12: # Right mouse button
                        self.device.emit(uinput.BTN_RIGHT, event_arg2)
                    case _:
                        raise ValueError('Unsupported mouse button')
            case _:
                raise ValueError('Unsupported event type.')

    def play(self):
        while True:
            received = self.conn.recv(64)
            self._action(received[0], received[1], received[2])


if __name__=='__main__':
    rc = Receiver()
    try:
        rc.standby()
        rc.play()
    except Exception as e:
        print(e)
        rc.destroy()