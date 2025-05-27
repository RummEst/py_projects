import tkinter as tk
from tkinter import Toplevel
import threading
import time

class aiGUI:
    def __init__(self):
        self.popups = []
        self.popup_threads = []

    def create_notification_popup(self, title="Listening...", comment="", use_comment=True):
        def popup_thread():
            # Create the root window and hide it
            root = tk.Tk()
            root.withdraw()  # Hide the root window

            # Create a new top-level window
            popup = Toplevel(root)
            popup.overrideredirect(True)  # Remove the window border
            popup.attributes('-topmost', True)  # Keep the popup on top of other windows

            # Dynamically adjust size based on title length
            title_font = ("Helvetica", 14)
            comment_font = ("Helvetica", 10)
            padding = 20
            width = max(200, len(title) * 10 + padding)
            height = 50 if not use_comment else 70

            # Get screen width and height
            screen_width = popup.winfo_screenwidth()
            screen_height = popup.winfo_screenheight()

            # Position the window in the top-right corner
            x = screen_width - width - 10
            y = 10
            popup.geometry(f'{width}x{height}+{x}+{y}')

            # Create rounded corners by setting an alpha mask (works better on Windows 11)
            popup.attributes('-transparentcolor', '#abc123')  # Transparent color hack
            canvas = tk.Canvas(popup, width=width, height=height, bg='#abc123', highlightthickness=0)
            canvas.pack()

            # Draw rounded rectangle
            def round_rectangle(x1, y1, x2, y2, radius=25, **kwargs):
                points = [x1 + radius, y1,
                          x1 + radius, y1,
                          x2 - radius, y1,
                          x2 - radius, y1,
                          x2, y1,
                          x2, y1 + radius,
                          x2, y1 + radius,
                          x2, y2 - radius,
                          x2, y2 - radius,
                          x2, y2,
                          x2 - radius, y2,
                          x2 - radius, y2,
                          x1 + radius, y2,
                          x1 + radius, y2,
                          x1, y2,
                          x1, y2 - radius,
                          x1, y2 - radius,
                          x1, y1 + radius,
                          x1, y1 + radius,
                          x1, y1]
                return canvas.create_polygon(points, **kwargs, smooth=True)

            round_rectangle(0, 0, width, height, radius=20, fill='#333333')

            # Add title text in the center
            canvas.create_text(width / 2, 15, text=title, fill="white", font=title_font)

            # Draw a white line and add comment if use_comment is True
            if use_comment:
                canvas.create_line(10, 30, width - 10, 30, fill="white", width=1)
                # Add comment text below the line
                canvas.create_text(width / 2, 45, text=comment, fill="light gray", font=comment_font)

            # Function to close the popup
            def close_popup():
                popup.destroy()

            # Close the popup after 5 seconds
            root.after(5000, close_popup)

            # Keep track of this popup and its root for later destruction
            self.popups.append(popup)
            self.popups.append(root)

            # Keep the popup running
            root.mainloop()

        # Start the popup in a new thread
        thread = threading.Thread(target=popup_thread)
        thread.start()
        self.popup_threads.append(thread)

    def kill_all_popups(self):
        # Close all popup windows
        for popup in self.popups:
            try:
                popup.destroy()
            except Exception as e:
                pass
        self.popups.clear()

        # Stop all threads
        for thread in self.popup_threads:
            if thread.is_alive():
                thread.join()  # Ensure the thread ends
        self.popup_threads.clear()


# Example usage
if __name__ == "__main__":
    gui = aiGUI()
    # This will create a popup with a comment
    gui.create_notification_popup(title="New Message", comment="This is a comment.")
    time.sleep(2)
    # Create another popup without the comment
    gui.create_notification_popup(title="No Comment Popup", use_comment=False)

    # Main code continues to run while the popups are displayed
    for i in range(10):
        print(f"Main code is running {i}")

    # After some time, you can kill all popups
    import time

    time.sleep(10)
    gui.kill_all_popups()
