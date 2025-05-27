
import pygetwindow as gw
from popup import show_popup as popup
from datetime import datetime
import subprocess
import os


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


# Run the Flask server on the local network
if __name__ == '__main__':
    toggleReoWindow()
    print("done")
