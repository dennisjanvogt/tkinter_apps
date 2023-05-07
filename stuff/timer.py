import tkinter as tk
from tkinter import ttk
import time
import csv


class Stopwatch:
    def __init__(self, master, index):
        self.master = master
        self.index = index

        self.frame = ttk.Frame(self.master)

        self.timer_label = ttk.Label(self.frame, text="00:00:00", font=("Arial", 24))
        self.timer_label.pack(pady=10)

        self.start_button = ttk.Button(
            self.frame, text="Start", command=self.start_timer
        )
        self.start_button.pack(side="left", padx=5)

        self.pause_button = ttk.Button(
            self.frame, text="Pause", command=self.pause_timer, state="disabled"
        )
        self.pause_button.pack(side="left", padx=5)

        self.stop_button = ttk.Button(
            self.frame, text="Stop", command=self.stop_timer, state="disabled"
        )
        self.stop_button.pack(side="left", padx=5)

        self.save_button = ttk.Button(
            self.frame, text="Save", command=self.save_entry, state="disabled"
        )
        self.save_button.pack(side="left", padx=5)

        self.delete_button = ttk.Button(
            self.frame, text="X", command=self.delete_stopwatch
        )
        self.delete_button.pack(side="left")

        self.entry_text = tk.StringVar()
        self.entry_label = ttk.Label(self.frame, text="Entry Name:")
        self.entry_label.pack(pady=10)

        self.entry_box = ttk.Entry(self.frame, textvariable=self.entry_text)
        self.entry_box.pack()

        self.times = []
        self.start_time = None
        self.paused_time = None
        self.running = False

        self.frame.pack()

    def start_timer(self):
        if not self.running:
            self.start_time = time.time()
        else:
            self.start_time = time.time() - self.paused_time
        self.master.after(1000, self.update_timer)
        self.start_button.config(state="disabled")
        self.pause_button.config(state="normal")
        self.stop_button.config(state="normal")
        self.save_button.config(state="disabled")
        self.running = True

    def pause_timer(self):
        if self.running:
            self.paused_time = time.time() - self.start_time
            self.master.after_cancel(self.update_timer)
            self.start_button.config(state="normal")
            self.pause_button.config(text="Resume")
            self.running = False
        else:
            self.start_time = time.time() - self.paused_time
            self.master.after(1000, self.update_timer)
            self.start_button.config(state="disabled")
            self.pause_button.config(text="Pause")
            self.running = True

    def stop_timer(self):
        self.times.append(time.time() - self.start_time)
        self.start_time = None
        self.master.after_cancel(self.update_timer)
        self.timer_label.config(text="00:00:00")
        self.start_button.config(state="normal")
        self.pause_button.config(state="disabled", text="Pause")
        self.stop_button.config(state="disabled")
        self.save_button.config(state="normal")
        self.running = False

    def update_timer(self):
        if self.start_time:
            elapsed_time = time.time() - self.start_time
            minutes, seconds = divmod(elapsed_time, 60)
            hours, minutes = divmod(minutes, 60)
            self.timer_label.config(
                text=f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
            )
            self.master.after(1000, self.update_timer)

    def save_entry(self):
        with open("entries.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            entry_name = self.entry_text.get()
            total_time = sum(self.times)
            writer.writerow([entry_name, f"{total_time:.2f}"])
            self.times = []
        self.save_button.config(state="disabled")
        self.entry_box.delete(0, tk.END)

    def delete_stopwatch(self):
        self.frame.destroy()
        self.master.stopwatches.pop(self.index)


class StopwatchApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Stopwatch App")
        self.geometry("500x500")

        self.stopwatches = [Stopwatch(self, 0)]

        self.add_button = ttk.Button(self, text="+", command=self.add_stopwatch)
        self.add_button.pack(pady=10)

        self.save_button = ttk.Button(
            self,
            text="Save All Entries",
            command=self.save_entries,
            state="disabled",
        )
        self.save_button.pack(pady=10)

        self.bottom_frame = ttk.Frame(self)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

        self.theme_switch_var = tk.BooleanVar(value=False)
        self.theme_switch = ttk.Checkbutton(
            self.bottom_frame,
            text="Dark Mode",
            variable=self.theme_switch_var,
            command=self.toggle_theme,
        )
        self.theme_switch.pack(side=tk.RIGHT, anchor="e", pady=5, padx=5)

    def add_stopwatch(self):
        new_stopwatch = Stopwatch(self, len(self.stopwatches))
        self.stopwatches.append(new_stopwatch)
        self.add_button.pack_forget()
        self.add_button.pack(pady=10)

    def save_entries(self):
        with open("entries.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Name", "Time (s)"])
            for stopwatch in self.stopwatches:
                entry_name = stopwatch.entry_text.get()
                total_time = sum(stopwatch.times)
                writer.writerow([entry_name, f"{total_time:.2f}"])
                stopwatch.times = []
                stopwatch.entry_box.delete(0, tk.END)
        self.save_button.config(state="disabled")

    def check_save_button(self):
        for stopwatch in self.stopwatches:
            if stopwatch.times:
                self.save_button.config(state="normal")
                return
        self.save_button.config(state="disabled")
        self.after(1000, self.check_save_button)

    def toggle_theme(self):
        if self.theme_switch_var.get():
            self.configure(bg="black")
            for stopwatch in self.stopwatches:
                stopwatch.frame.configure(style="dark")
        else:
            self.configure(bg="")
            for stopwatch in self.stopwatches:
                stopwatch.frame.configure(style="light")
        self.theme_switch.invoke()


app = StopwatchApp()
app.after(1000, app.check_save_button)
app.mainloop()
