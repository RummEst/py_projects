import win32com.client
import time
from win10toast_click import ToastNotifier
import subprocess
import logging
import argparse

# Configure logging to a file for background execution
logging.basicConfig(filename='usb_monitor.log', level=logging.INFO, format='%(asctime)s - %(message)s')

class USBListener:
    def __init__(self):
        """Initialize WMI and toast notifier."""
        self.wmi = win32com.client.GetObject("winmgmts:")
        self.notifier = ToastNotifier()
        self.SCRCPY_COMMAND = "scrcpy-win64-v3.2\\scrcpy.exe --video-bit-rate 16M --turn-screen-off --stay-awake --show-touches"

    def on_notification_click(self):
        """Handle toast notification click to launch scrcpy."""
        try:
            subprocess.Popen(self.SCRCPY_COMMAND, shell=True)
        except Exception as e:
            logging.error(f"Failed to run scrcpy: {e}")

    def check_existing_devices(self, targetname):
        """Check if the target device is already connected at startup."""
        try:
            devices = self.wmi.ExecQuery("SELECT * FROM Win32_USBHub")
            for device in devices:
                if device.Name.strip() == targetname:
                    logging.info(f"Target device already connected: {targetname}")
                    self.notifier.show_toast(
                        "Samsung S24 Connected",
                        "Open scrcpy?",
                        icon_path=None,
                        duration=10,
                        threaded=True,
                        callback_on_click=self.on_notification_click
                    )
                    break
        except Exception as e:
            logging.error(f"Error checking existing devices: {e}")

    def monitor_usb_by_name(self, targetname='SAMSUNG Mobile USB Composite Device'):
        """Monitor USB devices for a specific device name."""
        self.check_existing_devices(targetname)
        watcher = self.wmi.ExecNotificationQuery(
            "SELECT * FROM __InstanceOperationEvent WITHIN 2 "
            "WHERE TargetInstance ISA 'Win32_USBHub'"
        )
        logging.info(f"Monitoring for device name '{targetname}'")
        while True:
            try:
                event = watcher.NextEvent()
                device = event.TargetInstance
                device_name = getattr(device, 'Name', '').strip()
                if device_name == targetname:
                    if event.Path_.Class == '__InstanceCreationEvent':
                        logging.info(f"Target device connected: {device_name}")
                        self.notifier.show_toast(
                            "Samsung S24 Connected",
                            "Open scrcpy?",
                            icon_path=None,
                            duration=10,
                            threaded=True,
                            callback_on_click=self.on_notification_click
                        )
                    elif event.Path_.Class == '__InstanceDeletionEvent':
                        logging.info(f"Target device disconnected: {device_name}")
            except Exception as e:
                logging.error(f"Error: {e}")

if __name__ == "__main__":
    logging.info("USB Monitor started")
    parser = argparse.ArgumentParser(description='USB Device Monitor')
    parser.add_argument('--target', default='SAMSUNG Mobile USB Composite Device', help='Target device name')
    args = parser.parse_args()
    usbL = USBListener()
    usbL.monitor_usb_by_name(args.target)