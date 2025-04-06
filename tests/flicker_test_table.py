import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.panda_util.display import Display
from rich.table import Table
import time

display = Display(hz=1000)

def new_table():
    table = Table(title="Test Table")
    table.add_column("Name", justify="right", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")
    return table

table = new_table()

display.start_display_loop()

counter = 0

while True:
    display.clear_buffer()
    display += table
    counter += 1
    if counter > 0:
        table.add_row(f"Hello", str(counter))
    if counter == 30:
        counter = 0
        table = new_table()
    time.sleep(1/display.hz)