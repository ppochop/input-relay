import asyncio

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from connect_screen import ConnectScreen
from controller import Controller
from controller_screen import ControllerScreen


class InputClientApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controller = Controller()

    def build(self):
        sm = ScreenManager()
        sm.add_widget(ConnectScreen(self.controller, name='menu'))
        sm.add_widget(ControllerScreen(self.controller, name='control'))
        return sm

    def app_func(self):
        self.other_task = asyncio.ensure_future(self.controller.mouse_run())

        async def run_wrapper():
            await self.async_run(async_lib='asyncio')
            self.other_task.cancel()
        
        return asyncio.gather(run_wrapper(), self.other_task)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    ic = InputClientApp()
    loop.run_until_complete(ic.app_func())
    loop.close()
