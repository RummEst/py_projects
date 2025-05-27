import win32com.client
import pythoncom
import time
from windows_toasts import Toast, WindowsToaster

import subprocess

SCRCPY_COMMAND = "scrcpy-win64-v3.2\\scrcpy.exe --video-bit-rate 16M --turn-screen-off --stay-awake --show-touches"


#def on_notification_click():
 #   subprocess.Popen(SCRCPY_COMMAND, shell=True)


toaster = WindowsToaster('Python')
newToast = Toast()
newToast.text_fields = ['Hello, world!']
newToast.on_activated = lambda _: print('Toast clicked!')
toaster.show_toast(newToast)

#  "Samsung S24 Connected",
#  "Open scrcpy?",
#   icon_path=None,
#   duration=10,
#  threaded=True
