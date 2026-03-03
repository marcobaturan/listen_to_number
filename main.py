import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import pyttsx3
import random
import threading
import time

def generate_random_number(length):
    minimum = 10 ** (int(length) - 1)
    maximum = (10 ** int(length)) - 1
    return random.randint(minimum, maximum)

class ListenToNumberApp:
    def __init__(self, root):
        self.root = root
        self.current_number = None
        self.is_reading = False

        root.geometry("420x560")
        root.title("Listen to Number")
        root.resizable(False, False)

        container = ttk.Frame(root, padding=15)
        container.pack(fill=BOTH, expand=True)

        ttk.Label(container, text="Listen to Number", font=("Helvetica", 18, "bold")).pack(pady=10)

        # Number length
        ttk.Label(container, text="Select number length:").pack(anchor=W)
        self.length_var = ttk.StringVar(value="1")
        ttk.Combobox(container, textvariable=self.length_var, values=[str(i) for i in range(1, 51)], state="readonly").pack(fill=X, pady=5)

        # Rate
        ttk.Label(container, text="Digits/min:").pack(anchor=W, pady=(15,0))
        self.rate_var = ttk.StringVar(value="30")
        ttk.Combobox(container, textvariable=self.rate_var, values=["1","5","10","20","30","40","50","60"], state="readonly").pack(fill=X, pady=5)

        # Read
        self.read_btn = ttk.Button(container, text="Read", bootstyle=PRIMARY, command=self.start_reading_thread)
        self.read_btn.pack(fill=X, pady=20)

        # Input
        ttk.Label(container, text="Type the number you heard:").pack(anchor=W)
        self.input_var = ttk.StringVar()
        ttk.Entry(container, textvariable=self.input_var).pack(fill=X, pady=5)

        # Buttons
        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill=X, pady=15)
        ttk.Button(btn_frame, text="Compare", bootstyle=SUCCESS, command=self.compare_numbers).pack(side=LEFT, expand=True, fill=X, padx=5)
        ttk.Button(btn_frame, text="Exit", bootstyle=DANGER, command=root.destroy).pack(side=LEFT, expand=True, fill=X, padx=5)

    def start_reading_thread(self):
        if self.is_reading:
            return
        self.is_reading = True
        self.read_btn.config(state=DISABLED)

        self.current_number = generate_random_number(self.length_var.get())
        rate = int(self.rate_var.get())
        threading.Thread(target=self.read_number_task, args=(self.current_number, rate), daemon=True).start()

    def read_number_task(self, number, digits_per_minute):
        try:
            engine = pyttsx3.init()
            engine.setProperty("rate", 150)
            pause_seconds = 60.0 / digits_per_minute

            for i, d in enumerate(str(number)):
                engine.say(d)
                engine.runAndWait()
                if i < len(str(number))-1:
                    time.sleep(pause_seconds)

            engine.stop()
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("TTS Error", str(e)))
        finally:
            self.is_reading = False
            self.root.after(0, lambda: self.read_btn.config(state=NORMAL))

    def compare_numbers(self):
        if self.current_number is None:
            messagebox.showwarning("No Number", "Please read a number first!")
            return

        user_val = self.input_var.get().strip()
        status = "CORRECT" if str(self.current_number) == user_val else "INCORRECT"
        messagebox.showinfo("Result", f"Expected: {self.current_number}\nYou typed: {user_val}\n\n{status}")

if __name__ == "__main__":
    root = ttk.Window(themename="superhero")   # Works and applies theme correctly :contentReference[oaicite:2]{index=2}
    ListenToNumberApp(root)
    root.mainloop()