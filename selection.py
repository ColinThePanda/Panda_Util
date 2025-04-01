from typing import Any, List, Dict, Callable
from rich.table import Table
import time
import keyboard
from panda_util.display import Display

class ActionCallback:
    """
    A class that handles calling a specified action with arguments, optionally passing the caller object.
    """
    def __init__(self, action: Callable, pass_caller: bool, args: List[Any]):
        """Initializes the action callback.

        Args:
            action (Callable): The action function to be called.
            pass_caller (bool): Whether to pass the caller to the action.
            args (List[Any]): The arguments to pass to the action.
        """
        self.action = action
        self.pass_caller = pass_caller
        self.args = args

    def call(self, caller=None):
        """Calls the action, passing the caller object if required, along with any arguments.

        Args:
            caller (Any, optional): The caller to pass to the action if required.

        Returns:
            None
        """
        if self.pass_caller:
            self.action(caller, *self.args)  # Pass caller if specified
        else:
            self.action(*self.args)  # Otherwise, just pass arguments

class SelectionOption:
    """
    Represents an option in a selection menu with a name, description, value, and additional info.
    """
    def __init__(self, 
                 name: str, 
                 description: str = "", 
                 value: Dict[str, Any] = None,
                 additional_info: Dict[str, Any] = None):
        """Initializes a selection option.

        Args:
            name (str): The name of the selection option.
            description (str, optional): A description for the option. Defaults to "".
            value (Any, optional): A custom value for the option. Defaults to `name`.
            additional_info (Dict[str, Any], optional): Additional information for the option. Defaults to None.
        """
        self.name = name
        self.description = description
        self.value = value if value is not None else name  # Default value is name
        self.additional_info = additional_info or {}

    def __str__(self):
        """Returns the string representation of the selection option (its name).

        Returns:
            str: The name of the selection option.
        """
        return self.name

class Selection:
    """
    A class that handles displaying a selection menu with options and actions based on user input.
    """
    def __init__(self, title: str, options: List[SelectionOption], starting_index: int=0, highlight_style:str="bold white on blue", normal_style: str = "bold", cancellable: bool = False, action_callback: ActionCallback = None):
        """Initializes the selection menu with the provided title, options, and various display settings.

        Args:
            title (str): The title of the selection menu.
            options (List[SelectionOption]): The options to display in the menu.
            starting_index (int, optional): The initial index to start at. Defaults to 0.
            highlight_style (str, optional): The style for the highlighted option. Defaults to "bold white on blue".
            normal_style (str, optional): The style for the normal options. Defaults to "bold".
            cancellable (bool, optional): Whether the selection can be cancelled. Defaults to False.
            action_callback (ActionCallback, optional): A callback function to call when an option is selected. Defaults to None.
        """
        self.title = title
        self.options = options
        self.index = starting_index
        self.highlight_style = highlight_style
        self.normal_style = normal_style
        self.cancellable = cancellable
        self.action_callback = action_callback
        self.table = Table()  # Initialize the table to display options
        self.initialize_table()

    def initialize_table(self):
        """Initializes the table with columns for each selection option.

        Adds columns based on the attributes (name, description, value, etc.).

        Returns:
            None
        """
        if not self.options:
            return None

        self.table.title = self.title  # Set the title of the table

        # Add columns to the table based on the attributes of the first option
        item = self.options[0]
        if item.name: self.table.add_column("Name")
        if item.description: self.table.add_column("Description")
        if item.value: self.table.add_column("Value")
        for info in item.additional_info.keys():
            info[0] = info[0].upper()  # Capitalize the additional info keys
            self.table.add_column(info)

        # Add rows for each selection option
        for option in self.options:
            row = []
            if option.name: row.append(option.name)
            if option.description: row.append(option.description)
            if option.value: row.append(list(option.value.keys())[0])
            for info in option.additional_info.keys():
                if info: row.append(info)
            self.table.add_row(*row)

    def display(self, display: Display):
        """Displays the selection menu and handles user input to navigate and select options.

        Args:
            display (Display): Takes in a `Display` type to display the `Selection`.

        Returns:
            Any/None: Returns `None` if there are no options or if the selection is cancelled. 
                      Returns the value of the selected `SelectionOption` class.
        """
        if not self.options:
            return None

        running = True
        while running:
            display.clear()

            # Highlight the currently selected row
            for i, row in enumerate(self.table.rows):
                if i == self.index:
                    row.style = self.highlight_style

            # Display the table of options
            display += self.table

            # Display controls for navigating and selecting
            controls = ["[↑/↓] Navigate"]
            if self.cancellable:
                controls.append("[Esc] Cancel")
            controls.append("[Space/Enter] Select")
            display += " | ".join(controls)

            # Show the display text (if any)
            display.display_text()

            # Reset row styles to normal after displaying
            for i, row in enumerate(self.table.rows):
                if i == self.index:
                    row.style = self.normal_style

            time.sleep(0.2)

            # Wait for user input
            key = keyboard.read_key()

            # Handle navigation and selection
            if key == "up":
                self.index = (self.index - 1) % len(self.options)  # Navigate up
            elif key == "down":
                self.index = (self.index + 1) % len(self.options)  # Navigate down
            elif key in ["space", "enter"]:
                selected = self.options[self.index]

                # Call action callback if provided
                if self.action_callback:
                    self.action_callback.call(self)

                # Return the selected option's value
                return selected.value
            elif key == "esc" and self.cancellable:
                return None  # Return None if cancellable and Esc is pressed