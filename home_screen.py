import subprocess

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import RoundedRectangle
from kivy.uix.floatlayout import FloatLayout
from scrpy import scrape_and_process
from scrpy import *


Builder.load_string('''
<HomeScreen>:

    FloatLayout:
        id: float_layout
        BoxLayout:
            id: layout
            orientation: 'vertical'
            size_hint: 0.8, 0.8
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}

            Label:
                id: label
                text: 'Welcome Home!'
                font_size: 60
                font_name: 'Montserrat-limited/Montserrat-ExtraBold.ttf'

            TextInput:
                id: text_input1
                hint_text: 'Widget 1'

        BoxLayout:
            size_hint: None, None
            size: 130, 130
            pos_hint: {'top': 1, 'right': 1}

            Button:
                id: profile_button
                background_normal: 'profile.png'
                background_down: 'profile.png'
                size_hint: None, None
                size: 130, 130
                on_press: root.go_to_profile()

<ProfileScreen>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Profile Screen'
        Button:
            text: 'Go back home'
            on_press: root.go_back_home()

''')


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

        self.float_layout = FloatLayout()
        self.layout = BoxLayout(orientation='vertical', size_hint=(0.8, 0.8),
                                pos_hint={'center_x': 0.5, 'center_y': 0.5})

        self.label = Label(text='Welcome Home!', font_size=80, font_name='Montserrat-limited/Montserrat-ExtraBold.ttf')

        # Customizable Widgets
        self.text_input1 = TextInput(hint_text='Widget 1')
        self.layout.add_widget(self.text_input1)

        # End Customizable Widgets

        self.float_layout.add_widget(self.layout)

        # set position and size for the button
        self.profile_button = Button(background_normal='profile.png', background_down='profile.png', on_press=self.go_to_profile,
                             size=(130, 130), size_hint=(None, None), pos_hint={'top': 1, 'right': 1})
        self.float_layout.add_widget(self.profile_button)

        # add the new button to run scrape_and_process()
        self.scrape_button = Button(text='run', on_press=self.run_scrape_and_process, size_hint=(0.4, 0.4), 
                            pos_hint={'center_x': 0.5, 'center_y': 0.4}, 
                            background_normal='picture.png', background_down='picture.png',
                            color=[1,1,1,1])

        self.layout.add_widget(self.scrape_button)

        self.add_widget(self.float_layout)

    def go_to_profile(self, *args):
        self.manager.current = 'profile'

    def run_scrape_and_process(self, *args):
    # call scrape_and_process() and get the resulting dictionary
        category_summaries = scrape_and_process(ORGANIZATIONS, interest, 15, 5, 15)

    # access the "Stocks" summary from the dictionary
        stocks_summary = category_summaries["Stocks"]
        laws_summary = category_summaries["US Laws"]
        companies_summary = category_summaries["Companies"]
        news_summary = category_summaries["News"]

    # update the text of the text_input1 widget with the resulting text
        self.text_input1.text = 'stocks:\n{}\n\nlaws:\n{}\n\ncompanies:\n{}\n\nnews:\n{}'.format(stocks_summary, 
                                                                                            laws_summary, 
                                                                                            companies_summary, 
                                                                                            news_summary)

class ProfileScreen(Screen):
    pass

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(ProfileScreen(name='profile'))
        return sm

if __name__ == '__main__':
    MyApp().run()