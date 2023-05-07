import sqlite3
import tkinter as tk
from tkinter import ttk
from functools import partial
from stopwatch import Stopwatch

import datetime

from stopwatch_database import StopWatchDatabase


class StopwatchApp(ttk.Frame):
    title = "Beispiel-App 1"

    def __init__(self, parent, *args):
        super().__init__(parent)
        self.stopwatches = []
        self.projekte = []
        StopWatchDatabase.load_projects(projekte=self.projekte)

        StopWatchDatabase.create_database()

        self.add_stopwatch_button = ttk.Button(
            self, text="Stopuhr hinzufügen", command=self.add_stopwatch
        )
        self.add_stopwatch_button.pack(pady=(5, 5))

    def add_stopwatch(self):
        stopwatch = Stopwatch()
        self.stopwatches.append(stopwatch)

        frame = ttk.Frame(self)
        frame.pack(pady=(5, 5))

        row = len(self.stopwatches)

        timer_label = ttk.Label(frame, text="00:00:00")
        timer_label.grid(row=row, column=0, padx=(5, 5))

        project_var = tk.StringVar()
        project_var.set(self.projekte[0])
        project_menu = ttk.OptionMenu(frame, project_var, *self.projekte)
        project_menu.grid(row=row, column=1, padx=(5, 5))

        def update_timer_label():
            elapsed_time = stopwatch.get_time()
            minutes, seconds = divmod(elapsed_time, 60)
            hours, minutes = divmod(minutes, 60)
            timer_label.config(
                text=f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
            )
            timer_label.after(100, update_timer_label)

        update_timer_label()

        def on_start_pause_button_click():
            self.start_pause_stopwatch(stopwatch, start_pause_button)

        start_pause_button = ttk.Button(
            frame,
            text="Start",
            command=on_start_pause_button_click,
            takefocus=False,
        )
        start_pause_button.grid(row=row, column=2, padx=(5, 5))

        reset_button = ttk.Button(
            frame,
            text="Zurücksetzen",
            command=partial(self.reset_stopwatch, stopwatch),
            takefocus=False,
        )
        reset_button.grid(row=row, column=3, padx=(5, 5))

        save_button = ttk.Button(
            frame,
            text="Speichern",
            command=lambda: self.save_entry(
                project_var.get(),
                stopwatch,
                stopwatch.get_time(),
                frame,
            ),
            takefocus=False,
        )
        save_button.grid(row=row, column=4, padx=(5, 5))

        remove_button = ttk.Button(
            frame,
            text="Entfernen",
            command=lambda: self.remove_stopwatch(frame),
            takefocus=False,
        )
        remove_button.grid(row=row, column=5, padx=(5, 5))

    def start_pause_stopwatch(self, stopwatch, button):
        if stopwatch.running:
            stopwatch.pause()
            button.config(text="Start")
        else:
            stopwatch.start()
            button.config(text="Pausieren")

    def reset_stopwatch(self, stopwatch):
        stopwatch.reset()

    def remove_stopwatch(self, stopwatch, frame):
        conn = sqlite3.connect("stopwatch_data.db")
        c = conn.cursor()
        c.execute(
            "DELETE FROM stopwatches WHERE first_start=?",
            (
                datetime.datetime.fromtimestamp(
                    stopwatch.first_start_timestamp
                ).strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )
        conn.commit()
        conn.close()

        frame.pack_forget()
        frame.destroy()

    def update_entry(self, description, stopwatch):
        conn = sqlite3.connect("stopwatch_data.db")
        c = conn.cursor()
        c.execute(
            "UPDATE stopwatch_data SET description=?, elapsed_time=? WHERE first_start=?",
            (
                description,
                stopwatch.get_time(),
                datetime.datetime.fromtimestamp(
                    stopwatch.first_start_timestamp
                ).strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )
        conn.commit()
        conn.close()

    def save_entry(self, project, stopwatch, saved_label, frame):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        first_start_timestamp = datetime.datetime.fromtimestamp(
            stopwatch.first_start_timestamp
        ).strftime("%Y-%m-%d %H:%M:%S")
        conn = sqlite3.connect("stopwatch_data.db")
        c = conn.cursor()
        c.execute(
            "INSERT INTO stopwatch_data (timestamp, project, elapsed_time, first_start) VALUES (?, ?, ?, ?)",
            (timestamp, project, stopwatch.get_time(), first_start_timestamp),
        )
        conn.commit()
        conn.close()
        saved_label.config(text="Gespeichert")
        self.after(2000, lambda: self.remove_stopwatch(frame))
