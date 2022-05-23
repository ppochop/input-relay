from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen


class ConnectScreen(Screen):
    label_text = StringProperty('Type the remote host\'s IP address below\nand click the \'Connect\' button.')

    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller
    
    def connect(self, ip):
        code = self.controller.connect(ip)
        self.label_text = f'Connection established.\n On the remote host, \
            type in the following code:\n {code.decode("ASCII")}\n \
            Then click the \'Start the mouse\' button.'
        self.ids['btn2'].disabled = False