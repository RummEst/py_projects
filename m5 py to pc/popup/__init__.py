import tkinter as tk
from gc import collect

def show_popup(text, bgColor="black", fgColor="white", fontSize=24, timeout=5000):
    # Create the main window
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Create a top-level window for the popup
    popup = tk.Toplevel(root)
    popup.title("Popup")

    # Remove window border
    popup.overrideredirect(True)

    # Make the popup always on top
    popup.attributes("-topmost", True)

    # Set the size of the popup window
    popup.geometry("300x100")

    x_position = int((root.winfo_screenwidth() / 2) - (300 / 2))
    y_position = int((root.winfo_screenheight() / 2) - (100 / 2))
    popup.geometry(f"+{x_position}+{y_position}")

    # Add the label with the input text
    label = tk.Label(popup, text=text, font=("Helvetica", fontSize), bg=bgColor, fg=fgColor)
    label.pack(expand=True, fill='both')

    # Define a function to close the popup and stop the mainloop
    def close_popup():
        popup.destroy()  # Close the popup window
        root.quit()  # Stop the mainloop
        collect()

    # Set the popup to close after 5 seconds
    root.after(timeout, close_popup)

    # Start the tkinter event loop
    root.mainloop()

    return True
