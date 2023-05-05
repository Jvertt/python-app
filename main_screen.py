from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        
        # Set background color to a darker shade of blue
        self.background_color = (0.05, 0.10, 0.6, 1)
        
        # Create a vertical box layout with padding and spacing
        self.layout = BoxLayout(orientation='vertical', spacing=20, padding=60)
        
        # Add a label with white text and a modern font
        self.label = Label(text='GAUSSIAN', color=[1,1,1,1], font_size=60, font_name='Montserrat-limited/Montserrat-ExtraBold.ttf')

        # Add a button with white text and a gradient background
        self.sign_up_button = Button(text='Sign Up', size_hint=(0.4, 0.4), pos_hint={'center_x': 0.5},
                                     background_normal='picture.png', background_down='picture.png',
                                     font_size=30, font_name='Montserrat-limited/Montserrat-ExtraBold.ttf', bold=True)

        # Bind button press to sign_up method
        self.sign_up_button.bind(on_press=self.sign_up)
        
        # Add label and button to layout
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.sign_up_button)
        
        # Add layout to screen
        self.add_widget(self.layout)

    def sign_up(self, instance):
        self.manager.current = 'signup'
