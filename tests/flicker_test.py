import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.panda_util.display import Display
import time

display = Display(hz=600)
text = "".join(["Hello World " for _ in range(100)])
counter = 0

print("Press Ctrl+C to exit")
print("Using Display class with loop")
time.sleep(1)

try:
    # Clear any old content first
    display.clear()
    
    # Start display loop at 50Hz
    display.start_display_loop()
    
    # Run update loop
    while True:
        # Clear buffer before adding new content
        display.clear_buffer()
        
        # Add new content
        counter += 1
        display += f"Counter: {counter}"
        display += text
        
        # Sleep to control update rate
        time.sleep(1/display.hz)  # 50Hz content updates
except KeyboardInterrupt:
    display.stop_display_loop()
    print("\nTest ended by user")