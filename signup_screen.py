import json
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen


class User:
    def __init__(self, name, username, email, password, interest, city):
        self.name = name
        self.username = username
        self.email = email
        self.password = password
        self.interest = interest
        self.city = city


class SignUpScreen(Screen):
    def __init__(self, **kwargs):
        super(SignUpScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=25, size_hint=(0.8, 0.9), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.label = Label(text='Sign Up', font_size=80, font_name='Montserrat-limited/Montserrat-ExtraBold.ttf')
        self.layout.add_widget(self.label)
        self.text_input1 = TextInput(hint_text='Name')
        self.text_input2 = TextInput(hint_text='Username')
        self.text_input3 = TextInput(hint_text='Email')
        self.text_input4 = TextInput(hint_text='Password', password=True)
        self.text_input5 = TextInput(hint_text='Interest')
        self.text_input6 = TextInput(hint_text='City')
        self.layout.add_widget(self.text_input1)
        self.layout.add_widget(self.text_input2)
        self.layout.add_widget(self.text_input3)
        self.layout.add_widget(self.text_input4)
        self.layout.add_widget(self.text_input5)
        self.layout.add_widget(self.text_input6)
        
        # Set the background image of the button and adjust its size
        self.submit_button = Button(text='Submit', on_press=self.submit_form, size_hint=(None, None), size=(600, 300), pos_hint={'center_x': 0.5}, font_size=50)
        self.submit_button.background_normal = 'picture.png'
        self.layout.add_widget(self.submit_button)
        self.add_widget(self.layout)

        # Initialize an empty array to hold user objects
        self.users = []

    def on_pre_enter(self, *args):
        # Load previously entered data, if any
        try:
            with open('user_profile_data.json', 'r') as f:
                data = json.load(f)
                self.text_input1.text = data['name']
                self.text_input2.text = data['username']
                self.text_input3.text = data['email']
                self.text_input4.text = ''
                self.text_input5.text = data['interest']
                self.text_input6.text = data['city']

        except:
            pass

    def submit_form(self, instance):
        name = self.text_input1.text
        username = self.text_input2.text
        email = self.text_input3.text
        password = self.text_input4.text
        interest = self.text_input5.text
        city = self.text_input6.text

        # Create a user object with the provided data
        user = User(name, username, email, password, interest, city)

        # Append the user object to the array
        self.users.append(user)

        # Serialize the form data to JSON format
        form_data = {
            'name': name,
            'username': username,
            'email': email,
            'password': password,
            'interest': interest,
            'city': city
        }
        serialized_form_data = json.dumps(form_data)

        # Write the serialized form data to a file
        with open('user_profile_data.json', 'w') as f:
            f.write(serialized_form_data)

        # Print the serialized form data to the console
        print(serialized_form_data)

        # Create a user account with the provided data
        with open('user_accounts.txt', 'a') as f:
            f.write(f'{name}, {username}, {email}, {password}, {interest}, {city}\n')
        print('Saved form data:', serialized_form_data)

        # Clear the form fields
        self.text_input1.text = ''
        self.text_input2.text = ''
        self.text_input3.text = ''
        self.text_input4.text = ''
        self.text_input5.text = ''
        self.text_input6.text = ''

        # Switch back to the home screen
        self.manager.current = 'home'


