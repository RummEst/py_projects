import win32com.client
import pythoncom
import time
from win10toast_click import ToastNotifier
import subprocess


class USBEventHandler:
    def OnDeviceChange(self, event, device):
        if event == 2:  # DBT_DEVICEARRIVAL
            print("Device connected.")
        elif event == 3:  # DBT_DEVICEREMOVECOMPLETE
            print("Device removed.")


import win32com.client
import time

class USBListener:
    def __init__(self):
        self.wmi = win32com.client.GetObject("winmgmts:")
        self.notifier = ToastNotifier()
        self.SCRCPY_COMMAND = "scrcpy-win64-v3.2\\scrcpy.exe --video-bit-rate 16M --turn-screen-off --stay-awake --show-touches"

    def on_notification_click(self):
        subprocess.Popen(self.SCRCPY_COMMAND, shell=True)

    def monitor_usb(self):
        """Monitor all USB devices and report connection/disconnection events."""
        watcher = self.wmi.ExecNotificationQuery(
            "SELECT * FROM __InstanceOperationEvent WITHIN 2 "
            "WHERE TargetInstance ISA 'Win32_USBHub'"
        )

        print("Monitoring all USB devices... (press Ctrl+C to stop)")
        while True:
            try:
                event = watcher.NextEvent()
                device = event.TargetInstance
                device_name = getattr(device, 'Name', '').strip()

                if event.Path_.Class == '__InstanceCreationEvent':
                    print("USB device connected.")
                    print(" + " + device_name)
                elif event.Path_.Class == '__InstanceDeletionEvent':
                    print("USB device disconnected.")
                    print(" - " + device_name)


            except Exception as e:
                print(f"Error: {e}")
                time.sleep(1)

    def monitor_usb_by_name(self, targetname='SAMSUNG Mobile USB Composite Device'):
        """Monitor USB devices and report when the specific device is connected or disconnected."""
        watcher = self.wmi.ExecNotificationQuery(
            "SELECT * FROM __InstanceOperationEvent WITHIN 2 "
            "WHERE TargetInstance ISA 'Win32_USBHub'"
        )

        print(f"Monitoring for device name 'SAMSUNG Mobile USB Composite Device' (press Ctrl+C to stop)")
        while True:
            try:
                event = watcher.NextEvent()
                device = event.TargetInstance
                device_name = getattr(device, 'Name', '').strip()

                if device_name == targetname:
                    if event.Path_.Class == '__InstanceCreationEvent':
                        print(f"Target device connected: {device_name}")
                        self.notifier.show_toast(
                            "Samsung S24 Connected",
                            "Open scrcpy?",
                            icon_path=None,
                            duration=10,
                            threaded=True,
                            callback_on_click=self.on_notification_click
                        )
                    elif event.Path_.Class == '__InstanceDeletionEvent':
                        print(f"Target device disconnected: {device_name}")
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(1)


# Example usage:
# listener = USBListener()
# device_id = listener.print_id()
# listener.monitor_usb_by_id(device_id)



if __name__ == "__main__":
    usbL = USBListener()
    usbL.monitor_usb_by_name()
