import tkinter as tk
from tkinter import ttk
from .stopwatch import Stopwatch
from .stopwatch_database import StopwatchTable, ProjectTable
from .stopwatch_app_addentry import AddStopwatchPopup


class StopwatchWidget(ttk.Frame):
    def __init__(self, parent, stopwatch: Stopwatch, on_remove_callback):
        super().__init__(parent, padding=10)

        self.stopwatch = stopwatch
        self.on_remove_callback = on_remove_callback
        self.project_table_instance = ProjectTable()
        self.stopwatch_table_instance = StopwatchTable()

        self.project_label = ttk.Label(
            self,
            text=f"Projekt: {self.project_table_instance.get_project(id=stopwatch.project_id).name}",
            padding=(5, 5),
        )
        self.project_label.grid(row=0, column=0, padx=(5, 5), pady=(5, 5))

        self.elapsed_time_label = ttk.Label(self, text="00:00:00", padding=(5, 5))
        self.elapsed_time_label.grid(row=0, column=1, padx=(5, 5), pady=(5, 5))

        if stopwatch.state == "paused":
            self.start_pause_button = ttk.Button(
                self, text="Start", command=self.toggle
            )
        elif stopwatch.state == "running":
            self.start_pause_button = ttk.Button(
                self, text="Pause", command=self.toggle
            )
        self.start_pause_button.grid(row=0, column=2, padx=(5, 5), pady=(5, 5))

        self.note_entry_var = tk.StringVar()
        self.note_entry_var.trace_add("write", self.update_note_in_db)
        self.note_entry_var.set(self.stopwatch.note)
        self.note_entry = ttk.Entry(self, textvariable=self.note_entry_var, width=40, )
        self.note_entry.grid(row=0, column=3, padx=(5, 5), pady=(5, 5))

        self.save_button = ttk.Button(self, text="Speichern", command=self.save_time)
        self.save_button.grid(row=0, column=4, padx=(5, 5), pady=(5, 5))

        self.remove_button = ttk.Button(self, text="Entfernen", command=self.remove)
        self.remove_button.grid(row=0, column=5, padx=(5, 5), pady=(5, 5))

        self.update_elapsed_time()

    def toggle(self):
        self.stopwatch.toggle()
        if self.start_pause_button.cget("text") == "Start":
            button_text = "Pause"
        else:
            button_text = "Start"
        self.start_pause_button.config(text=button_text)

    def update_elapsed_time(self):
        self.elapsed_time_label.config(text=self.stopwatch.get_elapsed_time_str())
        self.after(1000, self.update_elapsed_time)

    def remove(self):
        self.stopwatch.remove()
        self.destroy()

    def save_time(self):
        if self.stopwatch.save_time(note=self.note_entry_var):
            self.stopwatch.reset()
            self.start_pause_button.config(text="Start")
            print("yes")

    def update_note_in_db(self, *args):
        self.stopwatch_table_instance.update_stopwatch(
            self.stopwatch.id, note=self.note_entry_var.get()
        )


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
        for widget in self.stopwatch_frame.winfo_children():
            widget.destroy()

        stopwatches = self.stopwatch_table.get_all_stopwatches()
        for stopwatch_data in stopwatches:
            stopwatch_data_dict = {
                "id": stopwatch_data.id,
                "project_id": stopwatch_data.project_id,
                "first_start_time": stopwatch_data.first_start_time,
                "latest_start_time": stopwatch_data.latest_start_time,
                "state": stopwatch_data.state,
                "actual_time": stopwatch_data.actual_time,
                "note": stopwatch_data.note,
            }
            stopwatch = Stopwatch(**stopwatch_data_dict)
            self.stopwatches.append(stopwatch)
            self.create_stopwatch_widget(stopwatch)

    def create_stopwatch_widget(self, stopwatch):
        widget = StopwatchWidget(self.stopwatch_frame, stopwatch, self.remove_stopwatch)
        widget.pack(fill=tk.X, pady=5)

    def add_stopwatch_popup(self):
        popup = AddStopwatchPopup(self, self.initial_save_stopwatch)
        self.wait_window(popup)

    def initial_save_stopwatch(self, project_id):
        stopwatch_data = {
            "project_id": project_id,
            "state": "paused",
            "first_start_time": None,
            "latest_start_time": None,
            "actual_time": 0.0,
            "note": None,
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
