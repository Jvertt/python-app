from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle

from home_screen import HomeScreen
from user_profile_screen import UserProfileScreen
from main_screen import MainScreen
from signup_screen import SignUpScreen

class Background(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            self.bg_rect = Rectangle(source='background.jpeg', pos=self.pos, size=self.size,
                                      size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

class MyApp(App):
    def build(self):
        bg = Background()
        Window.add_widget(bg)
        
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(SignUpScreen(name='signup'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(UserProfileScreen(name='profile'))
        return sm

if __name__ == '__main__':
    MyApp().run()
