import tkinter as tk
from tkinter import Toplevel


class aiGUI:
    def __init__(self):
        pass

    def create_notification_popup(self, title="Listening...", comment=""):
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
        height = 70 if comment else 50

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

        # Draw a white line below the title if there's a comment
        if comment:
            canvas.create_line(10, 30, width - 10, 30, fill="white", width=1)
            # Add comment text below the line
            canvas.create_text(width / 2, 45, text=comment, fill="light gray", font=comment_font)

        # Function to close the popup
        def close_popup():
            popup.destroy()

        # Return the root, popup, and close_popup function to allow external control
        return root, popup, close_popup


# Example usage
if __name__ == "__main__":
    gui = aiGUI()
    root, popup, close_popup = gui.create_notification_popup(title="New Message", comment="This is a comment.")

    # Close the popup after 5 seconds
    root.after(5000, close_popup)

    # Keep the popup running
    root.mainloop()
