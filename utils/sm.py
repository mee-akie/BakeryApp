from kivy.uix.screenmanager import ScreenManager, Screen
from components.loginComponent.login import LoginPage

class GeneralScreenManager:

    def getSm():
        sm = ScreenManager()
        sm.add_widget(LoginPage(name='login'))

        return sm