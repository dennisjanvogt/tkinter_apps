import tkinter as tk
from tkinter import ttk
from stopwatch import Stopwatch
from stopwatch_database import StopwatchTable, ProjectTable
from stopwatch_app_addentry import AddStopwatchPopup


class StopwatchWidget(ttk.Frame):
    def __init__(self, parent, stopwatch, on_remove_callback):
        super().__init__(parent, padding=10)

        self.stopwatch = stopwatch
        self.on_remove_callback = on_remove_callback

        self.project_label = ttk.Label(
            self, text=f"Projekt: {stopwatch.project_id}", padding=(5, 5)
        )
        self.project_label.pack(side=tk.LEFT)

        self.elapsed_time_label = ttk.Label(self, text="00:00:00", padding=(5, 5))
        self.elapsed_time_label.pack(side=tk.LEFT)

        # add blank labels with fixed width to create space between the buttons
        ttk.Label(self, width=1).pack(side=tk.LEFT)
        self.start_pause_button = ttk.Button(self, text="Start", command=self.toggle)
        self.start_pause_button.pack(side=tk.LEFT)

        ttk.Label(self, width=1).pack(side=tk.LEFT)
        self.save_button = ttk.Button(self, text="Speichern", command=self.save_time)
        self.save_button.pack(side=tk.LEFT)

        ttk.Label(self, width=1).pack(side=tk.LEFT)
        self.remove_button = ttk.Button(self, text="Entfernen", command=self.remove)
        self.remove_button.pack(side=tk.LEFT)

        self.update_elapsed_time()

    def toggle(self):
        if self.stopwatch.toggle():
            button_text = "Start" if self.stopwatch.state == "paused" else "Pause"
            self.start_pause_button.config(text=button_text)

    def update_elapsed_time(self):
        self.elapsed_time_label.config(text=self.stopwatch.get_elapsed_time_str())
        self.after(1000, self.update_elapsed_time)

    def remove(self):
        self.stopwatch.remove()
        self.destroy()

    def save_time(self):
        if self.stopwatch.save_time():
            self.stopwatch.reset()


class StopwatchApp(ttk.Frame):
    title = "StopwatchApp"

    def __init__(self, parent, *args):
        super().__init__(parent)

        self.stopwatch_frame = ttk.Frame(self)
        self.stopwatch_frame.pack(fill=tk.BOTH, expand=True)

        self.stopwatch_table = StopwatchTable()
        self.project_table = ProjectTable()
        self.stopwatches = []
        self.load_stopwatches()

        self.add_stopwatch_button = ttk.Button(
            self, text="Stoppuhr hinzufügen", command=self.add_stopwatch_popup
        )
        self.add_stopwatch_button.pack()

    def load_stopwatches(self):
        stopwatches = self.stopwatch_table.get_all_stopwatches()
        for stopwatch_data in stopwatches:
            stopwatch_data_dict = {
                "id": stopwatch_data.id,
                "project_id": stopwatch_data.project_id,
                "start_time": stopwatch_data.start_time,
                "state": stopwatch_data.state,
                "note": stopwatch_data.note,
            }
            stopwatch = Stopwatch(**stopwatch_data_dict)
            self.stopwatches.append(stopwatch)
            self.create_stopwatch_widget(stopwatch)

    def create_stopwatch_widget(self, stopwatch):
        widget = StopwatchWidget(self.stopwatch_frame, stopwatch, self.remove_stopwatch)
        widget.pack()

    def add_stopwatch_popup(self):
        popup = AddStopwatchPopup(self, self.save_stopwatch)
        self.wait_window(popup)

    def save_stopwatch(self, project_id):
        stopwatch_data = {
            "project_id": project_id,
            "state": "paused",
            "start_time": None,
        }
        stopwatch_id = self.stopwatch_table.add_stopwatch(stopwatch_data)
        stopwatch_data["id"] = stopwatch_id
        stopwatch = Stopwatch(**stopwatch_data)
        self.create_stopwatch_widget(stopwatch)

    def remove_stopwatch(self, stopwatch_id):
        self.stopwatch_table.delete_stopwatch(stopwatch_id)
        self.load_stopwatches()


if __name__ == "__main__":
    app = StopwatchApp()
    app.mainloop()
