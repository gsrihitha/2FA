# main.py
import hashlib
import time
from pyfingerprint.pyfingerprint import PyFingerprint
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup

class FingerprintApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10)

        label = Label(text='Fingerprint Authentication App', font_size=20)
        button = Button(text='Authenticate', size_hint=(None, None), size=(200, 50), on_press=self.show_authentication_popup)

        layout.add_widget(label)
        layout.add_widget(button)

        self.captured_fingerprint = None
        self.first_authentication = True
        self.result_label = Label(text='', font_size=16)  # New label for displaying the result

        layout.add_widget(self.result_label)

        return layout

    def show_authentication_popup(self, instance):
    
        if self.check_success_message():
            popup_layout = BoxLayout(orientation='vertical', padding=10)
            popup_label = Label(text='Please enter fingerprint data:')
            popup_button = Button(text='Capture Fingerprint', size_hint=(None, None), size=(200, 50),
                                  on_press=self.capture_and_verify_fingerprint)
            popup_layout.add_widget(popup_label)
            popup_layout.add_widget(popup_button)

            self.popup = Popup(title='Fingerprint Authentication', content=popup_layout, size_hint=(None, None), size=(300, 200))
            self.popup.open()
        else:
            print("Authentication failed. Success message not received.")

    def capture_and_verify_fingerprint(self, instance):
        self.popup.dismiss()  # Close the authentication popup
        if not self.captured_fingerprint:
            self.captured_fingerprint = self.capture_fingerprint()
            print('Fingerprint captured. Please re-run the app for subsequent authentications.')
        else:
            stored_template = self.get_stored_template()
            if self.verify_fingerprint(self.captured_fingerprint, stored_template):
                self.result_label.text = 'Authentication successful!'
            else:
                self.result_label.text = 'Authentication failed.'

    def capture_fingerprint(self):
        try:
            # Initialize the Fingerprint sensor
            f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

            if f.verifyPassword() is False:
                raise ValueError('The given fingerprint sensor password is wrong!')

            # Capture a fingerprint template
            print('Waiting for finger...')
            while f.readImage() is False:
                pass
            f.convertImage(0x01)
            fingerprint_data = f.downloadCharacteristics()

            return fingerprint_data

        except Exception as e:
            print('Error:', str(e))

    def get_stored_template(self):
        try:
             with open('stored_template.dat', 'rb') as file:
                    stored_template = file.read()
                    return stored_template
        except FileNotFoundError:
            print("Stored template not found. Please enroll a fingerprint first.")
            return None

        return b'stored_fingerprint_template'  

    def verify_fingerprint(self, captured_data, stored_template):
    
        captured_hash = hashlib.sha256(captured_data).hexdigest()
        stored_hash = hashlib.sha256(stored_template).hexdigest()
        
        if captured_hash == stored_hash:
            print("Fingerprint verification successful.")
            return True
        else:
            print("Fingerprint verification failed.")
            return False

    def check_success_message(self):
        try:
            with open('communication.txt', 'r') as file:
                content = file.read().strip()
                return content == 'success'
        except FileNotFoundError:
            return False

if __name__ == '__main__':
    FingerprintApp().run()

