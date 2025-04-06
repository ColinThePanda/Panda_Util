import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.panda_util.display import Display
from src.panda_util.selection import BoxSelection, SelectionOption

display = Display(hz=200)

selection = BoxSelection(title="Test Selection", options=[
    SelectionOption(name="Option 1", description="Description 1", value="value1"),
    SelectionOption(name="Option 2", description="Description 2", value="value2"),
    SelectionOption(name="Option 3", description="Description 3", value="value3")
])

value = selection.run(display)