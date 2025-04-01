from typing import Any, List
from rich.console import Console
import os, sys

class Display:
    """
    A class that handles the display of text or tables to the console.
    """
    def __init__(self):
        """Initializes the Display class."""
        self.text: List[Any] = []  # List to hold the text to display

    def clear(self):
        """Clears the console screen based on the platform (Windows or others)."""
        os.system('cls' if sys.platform == 'win32' else 'clear')

    def display_text(self, rich=True):
        """Displays the accumulated text to the console.

        Args:
            rich (bool): Whether to use the rich library for styled output. Defaults to True.

        Returns:
            None
        """
        console = Console() if rich else None
        self.clear()  # Clear the screen before displaying
        for item in self.text:
            try:
                if rich:
                    console.print(item)  # Use rich console to print item
                else:
                    print(str(item))  # Use basic print
            except Exception:
                # Handle any exception that occurs while printing
                print("ERROR OCCURRED") if not rich else console.print("ERROR OCCURRED")
        self.text.clear()  # Clear the text after displaying

    def __iadd__(self, other):
        """Adds an item to the text list for display.

        Args:
            other (Any): The item to add to the text list.

        Returns:
            Display: The Display object with the new item added.
        """
        self.text.append(other)
        return self
