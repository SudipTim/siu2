import tkinter as tk
from tkinter import messagebox
import threading
import time

class EyeCareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Eye Care Reminder")
        self.root.geometry("300x250")

        self.label = tk.Label(root, text="You will be reminded to look away from the screen.")
        self.label.pack(pady=10)

        self.timer_label = tk.Label(root, text="Next reminder in: 20:00")
        self.timer_label.pack(pady=10)

        self.time_entry = tk.Entry(root)
        self.time_entry.insert(0, "20")  # Default to 20 minutes
        self.time_entry.pack(pady=5)

        self.set_time_button = tk.Button(root, text="Set Reminder Time (minutes)", command=self.set_reminder_time)
        self.set_time_button.pack(pady=5)

        self.start_button = tk.Button(root, text="Start Reminder", command=self.start_reminder)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(root, text="Stop Reminder", command=self.stop_reminder)
        self.stop_button.pack(pady=5)

        self.reminder_thread = None
        self.reminding = False
        self.remaining_time = 1200  # Default 20 minutes in seconds

    def remind(self):
        while self.reminding:
            for remaining in range(self.remaining_time, 0, -1):
                self.update_timer(remaining)
                time.sleep(1)
            if self.reminding:  # Check again to avoid message after stopping
                self.show_reminder()

    def show_reminder(self):
        messagebox.showinfo("Reminder", "Time to look away from the screen!")
        self.update_timer(self.remaining_time)  # Reset timer after reminder

    def update_timer(self, remaining):
        minutes, seconds = divmod(remaining, 60)
        timer_text = f"Next reminder in: {minutes:02}:{seconds:02}"
        self.timer_label.config(text=timer_text)

    def set_reminder_time(self):
        try:
            minutes = int(self.time_entry.get())
            if minutes <= 0:
                raise ValueError("Please enter a positive number.")
            self.remaining_time = minutes * 60  # Convert to seconds
            self.update_timer(self.remaining_time)  # Update the display
            messagebox.showinfo("Set Time", f"Reminder time set to {minutes} minutes.")
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))

    def start_reminder(self):
        if not self.reminding:
            self.reminding = True
            self.reminder_thread = threading.Thread(target=self.remind)
            self.reminder_thread.start()

    def stop_reminder(self):
        self.reminding = False
        if self.reminder_thread is not None:
            self.reminder_thread.join()  # Wait for the thread to finish
        self.update_timer(self.remaining_time)  # Reset timer display

if __name__ == "__main__":
    root = tk.Tk()
    app = EyeCareApp(root)
    root.mainloop()
