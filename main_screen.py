from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        
        # Set background color to dark blue
        self.background_color = "[0.05, 0.10, 0.8, 1]"
        
        # Create a vertical box layout
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=100)
        
        # Add a label with light blue text and Montserrat Extra Bold font
        self.label = Label(text='Gaussian', color=[0.53, 0.81, 0.92, 1], font_size=60, font_name='Montserrat-limited/Montserrat-ExtraBold.ttf')

        # Add a button with a light blue background and white text
        self.sign_up_button = Button(text='Sign Up', background_color=[0.53, 0.81, 0.92, 1], color=[1, 1, 1, 1], font_size=30, bold=True, size_hint=(None, None), size=(300, 80), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Bind button press to sign_up method
        self.sign_up_button.bind(on_press=self.sign_up)
        
        # Add label and button to layout
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.sign_up_button)
        
        # Add layout to screen
        self.add_widget(self.layout)

    def sign_up(self, instance):
        self.manager.current = 'signup'
