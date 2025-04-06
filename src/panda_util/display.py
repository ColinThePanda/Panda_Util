from typing import Any, List
from rich.console import Console
import os, sys
import io
import threading
import time
import shutil

class Display:
    """
    A class that handles the display of text or tables to the console using minimal
    ANSI control sequences to prevent flickering during fast updates.
    """
    def __init__(self, hz: float = 25):
        """Initializes the Display class."""
        # Enable ANSI escape sequences on Windows
        if sys.platform == 'win32':
            os.system('')
            
        # Rich console setup
        self._string_buffer = io.StringIO()
        self.console = Console(force_terminal=True, file=self._string_buffer)
        
        # Buffer for content that will be displayed
        self._content_buffer = []
        
        # Screen management
        self.terminal_width, self.terminal_height = shutil.get_terminal_size()
        self._last_line_count = 0
        
        # Thread control
        self._display_lock = threading.Lock()
        self._display_thread = None
        self._stop_display = False
        self.hz = hz
        # Clear screen once at start
        print('\033[2J\033[H', end='', flush=True)

    def clear(self):
        """Clears the console screen."""
        with self._display_lock:
            print('\033[2J\033[H', end='', flush=True)
            self._last_line_count = 0
            self._content_buffer.clear()
    
    def clear_buffer(self):
        """Clears the content buffer."""
        with self._display_lock:
            self._content_buffer.clear()

    def _render_to_screen(self, rich=True):
        """Renders current content buffer to screen.
        
        Args:
            rich: Whether to use Rich formatting
        """
        if not self._content_buffer:
            return
            
        # Move cursor to home position
        print('\033[H', end='', flush=False)
        
        # Check if terminal size changed
        current_width, current_height = shutil.get_terminal_size()
        if (current_width, current_height) != (self.terminal_width, self.terminal_height):
            self.terminal_width, self.terminal_height = current_width, current_height
            print('\033[2J', end='', flush=False)  # Clear screen without moving cursor
            self._last_line_count = 0
        
        # Render content
        if rich:
            # Reset buffer
            self._string_buffer.seek(0)
            self._string_buffer.truncate(0)
            
            # Render all items with Rich
            for item in self._content_buffer:
                try:
                    self.console.print(item)
                except Exception:
                    self._string_buffer.write("ERROR OCCURRED\n")
            
            output = self._string_buffer.getvalue()
        else:
            # Simple string join for non-rich mode
            output = '\n'.join(str(item) for item in self._content_buffer)
        
        # Count lines
        line_count = output.count('\n') + 1
        
        # Print content
        print(output, end='', flush=False)
        
        # Clear any remaining lines from previous render
        if self._last_line_count > line_count:
            # Add empty lines and clear them
            for _ in range(line_count, self._last_line_count):
                print('\n\033[K', end='', flush=False)
            
            # Move cursor back up
            print(f'\033[{self._last_line_count - line_count}A', end='', flush=False)
        
        # Update line count and flush output
        self._last_line_count = line_count
        sys.stdout.flush()

    def display_text(self, rich=True):
        """Displays the accumulated text to the console.

        Args:
            rich (bool): Whether to use Rich library for styled output. Defaults to True.

        Returns:
            None
        """
        if self._display_thread and self._display_thread.is_alive():
            return  # Do nothing if display loop is running
            
        with self._display_lock:
            # Render current buffer to screen
            self._render_to_screen(rich)
            # Clear buffer after rendering
            self._content_buffer.clear()

    def start_display_loop(self):
        """Starts a display loop in a separate thread.
        
        Args:
            hz (float): Refresh rate in Hz. Defaults to 25.
        """
        if self._display_thread and self._display_thread.is_alive():
            raise RuntimeError("Display loop is already running")
        
        self._stop_display = False
        self._display_thread = threading.Thread(target=self._display_loop)
        self._display_thread.daemon = True
        self._display_thread.start()

    def stop_display_loop(self):
        """Stops the display loop if it's running."""
        if not (self._display_thread and self._display_thread.is_alive()):
            return
        
        self._stop_display = True
        self._display_thread.join(timeout=1.0)
        self._display_thread = None

    def _display_loop(self):
        """Internal method that runs the display loop.
        
        Args:
            hz (float): Refresh rate in Hz
        """
        interval = 1.0 / self.hz
        
        while not self._stop_display:
            start_time = time.time()
            
            # Render content
            with self._display_lock:
                self._render_to_screen()
            
            # Sleep to maintain frame rate
            elapsed = time.time() - start_time
            sleep_time = max(0, interval - elapsed)
            time.sleep(sleep_time)

    def __iadd__(self, other):
        """Adds an item to the text list for display.

        Args:
            other (Any): The item to add to the text list.

        Returns:
            Display: The Display object with the new item added.
        """
        with self._display_lock:
            self._content_buffer.append(other)
        return self

    def __del__(self):
        """Clean up resources."""
        self.stop_display_loop()
