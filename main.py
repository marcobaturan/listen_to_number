import tkinter as tk
from tkinter import messagebox, ttk
import pyttsx3
import random
import threading
import time

"""
Listen to Number Application
----------------------------
A desktop application built with Tkinter that helps users practice 
listening to numbers in various lengths and speeds.
"""

def generate_random_number(length):
    """
    Generates a random integer of the specified digit length.
    
    Args:
        length (int/str): The number of digits the generated number should have.
        
    Returns:
        int: A random number within the range [10^(length-1), 10^length - 1].
    """
    minimum = 10 ** (int(length) - 1)
    maximum = (10 ** int(length)) - 1
    return random.randint(minimum, maximum)

class ListenToNumberApp:
    """
    Main Application Class for the Listen to Number game.
    Manages the GUI and the Text-to-Speech (TTS) engine interaction.
    """
    
    def __init__(self, root):
        """
        Initializes the application window and widgets.
        
        Args:
            root (tk.Tk): The root Tkinter window instance.
        """
        self.root = root
        self.root.title("Listen to Number")
        self.root.geometry("400x550")
        
        # Application state
        self.current_number = None
        self.is_reading = False
        
        # Configure UI styles
        style = ttk.Style()
        style.configure("TButton", padding=5)
        style.configure("TLabel", padding=5)

        # Number Length Selection
        ttk.Label(root, text="Select the length of the number", font=("Arial", 10, "bold")).pack(pady=(10, 0))
        self.length_var = tk.StringVar(value="1")
        length_options = [str(i) for i in range(1, 51)]
        self.length_dropdown = ttk.Combobox(root, textvariable=self.length_var, values=length_options, state="readonly")
        self.length_dropdown.pack(pady=5)

        # Speech Rate Selection
        ttk.Label(root, text="Recitation speed (Digits/min)", font=("Arial", 10, "bold")).pack(pady=(10, 0))
        ttk.Label(root, text="1 (Slowest) to 60 (Fastest)", font=("Arial", 8, "italic")).pack()
        self.rate_var = tk.StringVar(value="30")
        rate_options = ["1", "5", "10", "20", "30", "40", "50", "60"]
        self.rate_dropdown = ttk.Combobox(root, textvariable=self.rate_var, values=rate_options, state="readonly")
        self.rate_dropdown.pack(pady=5)

        # Main Read Button
        self.read_btn = ttk.Button(root, text="Read", command=self.start_reading_thread)
        self.read_btn.pack(pady=20)

        # User Input Area
        ttk.Label(root, text="Type the number you heard:", font=("Arial", 10, "bold")).pack(pady=(10, 0))
        self.input_var = tk.StringVar()
        self.number_entry = ttk.Entry(root, textvariable=self.input_var)
        self.number_entry.pack(pady=5)

        # Navigation and Action Buttons
        button_frame = ttk.Frame(root)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Compare", command=self.compare_numbers).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exit", command=root.destroy).pack(side=tk.LEFT, padx=5)

    def start_reading_thread(self):
        """
        Starts a background thread to handle the speech synthesis.
        Prevents the main GUI thread from freezing during playback.
        """
        if self.is_reading:
            return
        
        self.is_reading = True
        self.read_btn.config(state="disabled")
        
        # Prepare data in main thread
        length = int(self.length_var.get())
        self.current_number = generate_random_number(length)
        
        # Fetch target rate (1-300 scale, to be mapped internally)
        target_rate = int(self.rate_var.get())
        
        # Launch thread
        threading.Thread(target=self.read_number_task, args=(self.current_number, target_rate), daemon=True).start()

    def read_number_task(self, number, digits_per_minute):
        """
        Worker task for the speech thread. 
        Initializes TTS engine and recites the number digit by digit with custom delay.
        
        Args:
            number (int): The number to recite.
            digits_per_minute (int): Speed in digits per minute.
        """
        try:
            # Initialize engine locally within the thread
            local_engine = pyttsx3.init()
            
            # Set a standard comfortable rate for the voice itself
            local_engine.setProperty('rate', 150)
            
            # Calculate pause duration between digits
            # pause_seconds = 60 / digits_per_minute
            pause_seconds = 60.0 / digits_per_minute
            
            digits = str(number)
            for i, digit in enumerate(digits):
                local_engine.say(digit)
                local_engine.runAndWait()
                
                # Add delay if not the last digit
                if i < len(digits) - 1:
                    time.sleep(pause_seconds)
            
            # Resource cleanup
            local_engine.stop()
            del local_engine
            
        except Exception as e:
            # Re-sync with main thread to show error
            self.root.after(0, lambda: messagebox.showerror("Read Error", f"Speech engine failed: {e}"))
        finally:
            # Re-enable button and reset state
            self.is_reading = False
            self.root.after(0, lambda: self.read_btn.config(state="normal"))

    def compare_numbers(self):
        """
        Compares user input with the last generated number and displays feedback.
        """
        if self.current_number is None:
            messagebox.showwarning("No Number", "Generate and listen to a number first!")
            return
            
        user_input = self.input_var.get().strip()
        
        # Validate match
        match = str(user_input) == str(self.current_number)
        
        # Prepare feedback message
        status = "CORRECT!" if match else "INCORRECT!"
        result_msg = (
            f"Expected: {self.current_number}\n"
            f"You Typed: {user_input}\n\n"
            f"Result: {status}"
        )
        
        messagebox.showinfo("Result Comparison", result_msg)

if __name__ == "__main__":
    # Create main application loop
    root = tk.Tk()
    app = ListenToNumberApp(root)
    root.mainloop()
