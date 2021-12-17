import kivy
kivy.require('1.0.6')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import psycopg2

class LoginPage(Screen):

    def __init__(self, **kwargs):
        super(LoginPage, self).__init__(**kwargs)
        Builder.load_file('components\loginComponent\login.kv')
    
    def validaLogin(self, *args):


        print(cpfUsuario)
