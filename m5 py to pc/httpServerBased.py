import os
import socket
import subprocess
from datetime import datetime

import pygetwindow as gw
from flask import Flask, render_template_string, request, redirect

from popup import show_popup as popup

app = Flask(__name__)



def run_shortcut(shortcut_path=r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Reolink.lnk"):
    # Use os.startfile to run the shortcut, which automatically does not wait for it to finish
    os.startfile(shortcut_path)





def toggleReoWindow():
    winList = gw.getWindowsWithTitle('Reolink')
    if not winList:
        print("Reolink not opened, opening")
        run_shortcut()
        popup("open Reolink...")
    else:
        reoWin = winList[0]
        if reoWin.isMaximized:
            reoWin.minimize()
            print("reoWin.minimize()")
        elif not reoWin.isMaximized:
            reoWin.maximize()
            print("reoWin.maximize()")
        else:
            print("toggleReoWin() -> Error")

# Route to serve the main page
@app.route('/')
def index():
    # Simple HTML page with a button
    html = '''
    <html>
        <head>
            <title>Run exampleFunc</title>
        </head>
        <body>
            <h1>Click the button to run exampleFunc()</h1>
            <form action="/run-function" method="post">
                <button type="submit">Run Function</button>
            </form>
        </body>
    </html>
    '''
    return render_template_string(html)

# Route to handle the button click
@app.route('/run-function', methods=['POST'])
def run_function():
    toggleReoWindow()  # Run the example function
    return redirect("/")

# Run the Flask server on the local network
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
