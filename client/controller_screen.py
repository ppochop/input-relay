from garden_joystick import Joystick
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from controller import BTN_PRESS, BTN_RELEASE, MOUSE_BTN_LEFT, MOUSE_BTN_RIGHT

class MouseButtons(BoxLayout):
    def __init__(self, mouse_btn_func, **kwargs):
        super().__init__(**kwargs)
        self.mouse_btn_func = mouse_btn_func

    def press_lmb(self):
        self.mouse_btn_func(MOUSE_BTN_LEFT, BTN_PRESS)

    def release_lmb(self):
        self.mouse_btn_func(MOUSE_BTN_LEFT, BTN_RELEASE)

    def press_rmb(self):
        self.mouse_btn_func(MOUSE_BTN_RIGHT, BTN_PRESS)

    def release_rmb(self):
        self.mouse_btn_func(MOUSE_BTN_RIGHT, BTN_RELEASE)


class ControllerUI(BoxLayout):
    def __init__(self, controller):
        super().__init__(orientation='vertical')
        self.controller = controller
        btnz = MouseButtons(controller.mouse_btn)
        self.add_widget(btnz)
        joystick = Joystick()
        joystick.bind(pad=self.update_coordinates)
        self.add_widget(joystick)
        self.label = Label()
        self.add_widget(self.label)

    def update_coordinates(self, joystick, pad):
        x = pad[0]
        y = pad[1]
        self.controller.x = x
        self.controller.y = y


class ControllerScreen(Screen):
    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(ControllerUI(controller))
