from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
import json

class UserProfileScreen(Screen):
    def __init__(self, **kwargs):
        super(UserProfileScreen, self).__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical', spacing=25, size_hint=(0.8, 0.9), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.label = Label(text='User Profile', font_size=80, font_name='Montserrat-limited/Montserrat-ExtraBold.ttf')

        # Customizable TextInputs
        self.text_input1 = TextInput(hint_text='Name', background_color=[1, 1, 1, 1])
        self.text_input2 = TextInput(hint_text='Username', background_color=[1, 1, 1, 1])
        self.text_input3 = TextInput(hint_text='Email', background_color=[1, 1, 1, 1])
        self.text_input4 = TextInput(hint_text='Interest', background_color=[1, 1, 1, 1])
        self.text_input5 = TextInput(hint_text='City', background_color=[1, 1, 1, 1])
        # End Customizable TextInputs

        self.update_button = Button(text='Update', on_press=self.update_profile, size_hint=(0.55, 0.55), pos_hint={'center_x': 0.5})
        
        # Add all widgets to layout
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.text_input1)
        self.layout.add_widget(self.text_input2)
        self.layout.add_widget(self.text_input3)
        self.layout.add_widget(self.text_input4)
        self.layout.add_widget(self.text_input5)
        self.layout.add_widget(self.update_button)

        self.add_widget(self.layout)

    def on_pre_enter(self):
        with open('user_profile_data.json') as f:
            data = json.load(f)
        self.text_input1.text = data['name']
        self.text_input2.text = data['username']
        self.text_input3.text = data['email']
        self.text_input4.text = data['interest']
        self.text_input5.text = data['city']

    def update_profile(self, instance):
        name = self.text_input1.text
        username = self.text_input2.text
        email = self.text_input3.text
        interest = self.text_input4.text
        city = self.text_input5.text

        # update the user profile data in the JSON file
        with open('user_profile_data.json', 'w') as f:
            data = {
                'name': name,
                'username': username,
                'email': email,
                'interest': interest,
                'city': city
            }
            json.dump(data, f)

        # Clear text input fields after updating the data
        self.text_input1.text = ''
        self.text_input2.text = ''
        self.text_input3.text = ''
        self.text_input4.text = ''
        self.text_input5.text = ''

        # Go back to HomeScreen
        self.manager.current = 'home'
