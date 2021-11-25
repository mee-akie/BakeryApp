from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import MDList, OneLineIconListItem
from kivy.properties import StringProperty
import psycopg2
from kivy.uix.screenmanager import ScreenManager, Screen


KV = '''
#:import get_color_from_hex kivy.utils.get_color_from_hex


ScreenManager:
    HomePage:
    FuncionarioPage:


<NavigationDrawer>
    orientation: "vertical"
    padding: "8dp"
    spacing: "8dp"

    AnchorLayout:
        anchor_x: "left"
        size_hint_y: None
        height: avatar.height

        Image:
            id: avatar
            size_hint: None, None
            size: "56dp", "56dp"
            source: "user.png"

    MDLabel:
        text: "USERNAME"
        font_style: "Button"
        size_hint_y: None
        height: self.texture_size[1]

    MDLabel:
        text: "userEmail@gmail.com"
        font_style: "Caption"
        size_hint_y: None
        height: self.texture_size[1]


    ScrollView:
        MDList:
            OneLineListItem:
                text: "Pagina 1"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "item 1"

            OneLineListItem:
                text: "Pagina 2"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "item 2"

            OneLineListItem:
                text: "Pagina 3"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "item 3"


<HomePage>:
    name: 'home'
    MDScreen:
        MDToolbar:
            id: toolbar
            pos_hint: {"top": 1}
            elevation: 10
            title: "Bakery ABC"
            left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
            md_bg_color: get_color_from_hex("#854442")

        MDNavigationLayout:
            x: toolbar.height
            ScreenManager:
                id: screen_manager
                MDScreen:
                    name: "item 1"
                    MDLabel:
                        text: "Screen 1"
                        halign: "center"
                MDScreen:
                    name: "item 2"
                    MDLabel:
                        text: "Screen 2"
                        halign: "center"
                MDScreen:
                    name: "item 3"
                    MDLabel:
                        text: "Screen 3"
                        halign: "center"
            MDNavigationDrawer:
                id: nav_drawer
                NavigationDrawer:
                    screen_manager: screen_manager
                    nav_drawer: nav_drawer

        MDBottomNavigation:
            size_hint_y: .09
            panel_color: get_color_from_hex("#854442")
            text_color_active: get_color_from_hex("#fff4e6")
            
            MDBottomNavigationItem:
                name: 'screen 1'
                text: 'home'
                icon: 'home-circle'
                on_enter: root.switchHome()

            MDBottomNavigationItem:
                name: 'screen 2'
                text: 'botao 2'
                icon: 'barcode'

            MDBottomNavigationItem:
                name: 'screen 3'
                text: 'Funcionarios'
                icon: 'account-group'
                on_enter: root.switchFuncionario()
                
 
<FuncionarioPage>:
    name: 'funcionario'

    MDScreen:
        MDToolbar:
            id: toolbar
            pos_hint: {"top": 1}
            elevation: 10
            title: "Bakery ABC"
            md_bg_color: get_color_from_hex("#854442")

        MDBottomNavigation:
            size_hint_y: .09
            panel_color: get_color_from_hex("#854442")
            text_color_active: get_color_from_hex("#fff4e6")
            
            MDBottomNavigationItem:
                name: 'screen 1'
                text: 'home'
                icon: 'home-circle'
                on_enter: root.switchHome()

            MDBottomNavigationItem:
                name: 'screen 2'
                text: 'botao 2'
                icon: 'barcode'

            MDBottomNavigationItem:
                name: 'screen 3'
                text: 'Funcionarios'
                icon: 'account-group'
                on_enter: root.switchFuncionario()

        MDFillRoundFlatIconButton :
            text : 'Cadastrar um empregado'
            icon : "account-plus"
            pos_hint : {"center_x":.5,"center_y":.8}
            text_color : get_color_from_hex("#7E6B73")
            md_bg_color : get_color_from_hex("#FCE18E")
            font_size : 20
            on_press : app.callback()
            user_font_size: "64sp"

        MDFillRoundFlatIconButton :
            text : 'Remover um empregado'
            icon : "account-minus"
            pos_hint : {"center_x":.5,"center_y":.6}
            text_color : get_color_from_hex("#7E6B73")
            md_bg_color : get_color_from_hex("#FCE18E")
            font_size : 20
            on_press : app.callback()

        MDFillRoundFlatIconButton :
            text : 'Alterar dados de um empregado'
            icon : "account-edit"
            pos_hint : {"center_x":.5,"center_y":.4}
            text_color : get_color_from_hex("#7E6B73")
            md_bg_color : get_color_from_hex("#FCE18E")
            font_size : 20
            on_press : app.callback()



'''


class HomePage(Screen):
    def switchHome(self):
        self.parent.current = 'home'
    def switchFuncionario(self):
        self.parent.current = 'funcionario'

class FuncionarioPage(Screen):
    def switchHome(self):
        self.parent.current = 'home'
    def switchFuncionario(self):
        self.parent.current = 'funcionario'


class NavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

# Create the screen manager
sm = ScreenManager()
sm.add_widget(HomePage(name='home'))
sm.add_widget(FuncionarioPage(name='funcionario'))


class Main(MDApp):
    def build(self):

        conn = psycopg2.connect(
            host = "ec2-44-198-211-34.compute-1.amazonaws.com",
            database = "ddj7ffdunshjqf", 
            user = "vuxxgxylynkvnk",
            password = "e7f1713e3c7c4907b83a8e412f5373c52e1bf5e7a741e6667957bb41bcbecd69",
            port = "5432"
        )

        # Create A Cursor
        c = conn.cursor()

        # Create A Table
        c.execute("""CREATE TABLE if not exists customers(
            name TEXT);
            """)

        # Commit our changes
        conn.commit()

        # Close our connection
        conn.close()

        return Builder.load_string(KV)
    

    def submit(self):
        # Create Database Or Connect To One
        #conn = sqlite3.connect('first_db.db')
        conn = psycopg2.connect(
            host = "ec2-44-198-211-34.compute-1.amazonaws.com",
            database = "ddj7ffdunshjqf", 
            user = "vuxxgxylynkvnk",
            password = "e7f1713e3c7c4907b83a8e412f5373c52e1bf5e7a741e6667957bb41bcbecd69",
            port = "5432"
        )

        # Create A Cursor
        c = conn.cursor()

        # Add A Record
        sql_command = "INSERT INTO customers (name) VALUES (%s)"
        values = (self.root.ids.word_input.text,)
        
        # Execute SQL Command
        c.execute(sql_command, values)	
        

        # Add a little message
        self.root.ids.word_label.text = f'{self.root.ids.word_input.text} Added'

        # Clear the input box
        
        self.root.ids.word_input.text = ''


        # Commit our changes
        conn.commit()

        # Close our connection
        conn.close()


Main().run()