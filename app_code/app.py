# app.py
from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Default password for authentication
DEFAULT_PASSWORD = '520@project'

# File to communicate with Kivy app
COMMUNICATION_FILE = 'communication.txt'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    entered_password = request.form.get('password')

    if entered_password == DEFAULT_PASSWORD:
        # Write a message to the communication file
        with open(COMMUNICATION_FILE, 'w') as file:
            file.write('success')

        return render_template('success.html', message='Password authentication successful!')
    else:
        return render_template('index.html', message='Incorrect password. Authentication failed.')

if __name__ == '__main__':
    # Remove the debug=True in production
    app.run(debug=True)




