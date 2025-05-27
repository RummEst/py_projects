import sys

class c:
    def __init__(self):
        self.formats = {
            # Regular Colors
            "BLACK": "\033[0;30m",
            "RED": "\033[0;31m",
            "GREEN": "\033[0;32m",
            "YELLOW": "\033[0;33m",
            "BLUE": "\033[0;34m",
            "MAGENTA": "\033[0;35m",
            "CYAN": "\033[0;36m",
            "WHITE": "\033[0;37m",

            # Bold Colors
            "BOLD_BLACK": "\033[1;30m",
            "BOLD_RED": "\033[1;31m",
            "BOLD_GREEN": "\033[1;32m",
            "BOLD_YELLOW": "\033[1;33m",
            "BOLD_BLUE": "\033[1;34m",
            "BOLD_MAGENTA": "\033[1;35m",
            "BOLD_CYAN": "\033[1;36m",
            "BOLD_WHITE": "\033[1;37m",

            # Text styles
            "BOLD": "\033[1m",
            "UNDERLINE": "\033[4m",
            "REVERSED": "\033[7m",
            "RESET": "\033[0m"
        }

    def set(self, key):
        if key in self.formats:
            sys.stdout.write(self.formats[key])
        else:
            sys.stdout.write(self.formats["RESET"])

    def reset(self):
        sys.stdout.write(self.formats["RESET"])

    def cprint(self, key, string):
        self.set(key)
        print(string)
        self.reset()

    def xprint(self, complex_string):
        parts = complex_string.split('$')
        for part in parts:
            if part in self.formats:
                sys.stdout.write(self.formats[part])
            else:
                print(part, end="")
        print()

    def help(self):
        """Print documentation on how to use the class."""
        print("Usage:")
        print("- To set text color or style, use the 'set' method with a key from the formats dictionary.")
        print("- To reset text color and style to default, use the 'reset' method.")
        print("- To print a string with a specified color or style, use the 'cprint' method with a key and a string.")
        print(
            "- To print a complex string with embedded color or style markers, use the 'xprint' method with the string.")
        print()
        print("Formatting Options:")
        for key in self.formats:
            print("-", key)
        print()
        print("Usage of 'cprint':")
        print("cprint(key, string) - Prints the provided string with the specified color or style.")
        print("   'key' should be a key from the formats dictionary.")
        print("   'string' is the text to be printed.")
        print()
        print("Usage of 'xprint':")
        print("xprint(complex_string) - Prints a complex string with embedded color or style markers.")
        print("   'complex_string' should contain markers ('$key$') representing colors or styles.")
        print("   Example: 'xprint(\"$RED$This is red text $RESET$\")'")



