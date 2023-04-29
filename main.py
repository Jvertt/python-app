from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.label = Label(text='Welcome Home!')
        self.layout.add_widget(self.label)
        
        # Customizable Widgets
        self.text_input1 = TextInput(hint_text='Widget 1')
        self.text_input2 = TextInput(hint_text='Widget 2')
        self.text_input3 = TextInput(hint_text='Widget 3')
        self.layout.add_widget(self.text_input1)
        self.layout.add_widget(self.text_input2)
        self.layout.add_widget(self.text_input3)
        # End Customizable Widgets

        # Add a button that takes the user to their profile page
        self.profile_button = Button(text='Profile', on_press=self.go_to_profile)
        self.layout.add_widget(self.profile_button)

        self.add_widget(self.layout)
    
    def go_to_profile(self, instance):
        # TODO: define what should happen when the button is pressed
        pass


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        
        # Set background color to a light gray
        self.background_color = [0.8,0.8,0.8,1]
        
        # Create a vertical box layout
        self.layout = BoxLayout(orientation='vertical', spacing=30, padding=30)
        
        # Add a label with dark text and a modern font
        self.label = Label(text='Welcome to my app!', color=[0.2,0.2,0.2,1], font_name='RobotoMono-Regular', font_size=48, bold=True)
        
        # Add a button with a light gray background, dark text, and a modern font
        self.button = Button(text='Sign Up', background_color=[0.9,0.9,0.9,1], color=[0.2,0.2,0.2,1], font_name='RobotoMono-Regular', font_size=24, bold=True, size_hint=(0.6, 0.2), pos_hint={'center_x': 0.5})
        
        # Bind button press to sign_up method
        self.button.bind(on_press=self.sign_up)
        
        # Add label and button to layout
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.button)
        
        # Add layout to screen
        self.add_widget(self.layout)

    def sign_up(self, instance):
        self.manager.current = 'signup'


class SignUpScreen(Screen):
    def __init__(self, **kwargs):
        super(SignUpScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.label = Label(text='Sign Up')
        self.layout.add_widget(self.label)
        self.text_input1 = TextInput(hint_text='Name')
        self.text_input2 = TextInput(hint_text='Username')
        self.text_input3 = TextInput(hint_text='Email')
        self.text_input4 = TextInput(hint_text='Interest')
        self.text_input5 = TextInput(hint_text='City')
        self.layout.add_widget(self.text_input1)
        self.layout.add_widget(self.text_input2)
        self.layout.add_widget(self.text_input3)
        self.layout.add_widget(self.text_input4)
        self.layout.add_widget(self.text_input5)
        self.submit_button = Button(text='Submit', on_press=self.submit_form)
        self.layout.add_widget(self.submit_button)
        self.add_widget(self.layout)

    def submit_form(self, instance):
        name = self.text_input1.text
        username = self.text_input2.text
        email = self.text_input3.text
        interest = self.text_input4.text
        city = self.text_input5.text

        # TODO: log or store the form data
        # For example, you can write the form data to a file or database
        # or send it to a remote server using an API.

        self.text_input1.text = ''
        self.text_input2.text = ''
        self.text_input3.text = ''
        self.text_input4.text = ''
        self.text_input5.text = ''
        
        self.manager.current = 'home'


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(SignUpScreen(name='signup'))
        sm.add_widget(HomeScreen(name='home'))
        return sm

if __name__ == '__main__':
    MyApp().run()
