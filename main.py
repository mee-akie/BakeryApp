from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import MDList, OneLineIconListItem
from kivy.properties import StringProperty



KV = '''
#:import get_color_from_hex kivy.utils.get_color_from_hex

#:set text_color get_color_from_hex("#4a4939")
#:set focus_color get_color_from_hex("#e7e4c0")
#:set bg_color get_color_from_hex("#f7f4e7")
#:set selected_color get_color_from_hex("#0c6c4d")


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

        MDBottomNavigationItem:
            name: 'screen 2'
            text: 'botao 2'
            icon: 'barcode'

        MDBottomNavigationItem:
            name: 'screen 3'
            text: 'botao 3'
            icon: 'account-circle-outline'

'''


class NavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

class TestNavigationDrawer(MDApp):
    def build(self):
        return Builder.load_string(KV)


TestNavigationDrawer().run()