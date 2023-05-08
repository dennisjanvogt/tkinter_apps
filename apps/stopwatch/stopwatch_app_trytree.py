import tkinter as tk
from tkinter import ttk
from .stopwatch import Stopwatch
from .stopwatch_database import StopwatchTable, ProjectTable
from .stopwatch_app_addentry import AddStopwatchPopup


class StopwatchApp(ttk.Frame):
    title = "StopwatchApp"

    def __init__(self, parent, *args):
        super().__init__(parent)

        self.stopwatch_table = StopwatchTable()
        self.project_table = ProjectTable()
        self.stopwatches = []

        self.treeview = ttk.Treeview(
            self, columns=("Project", "Elapsed", "Toggle", "Note", "Save", "Remove")
        )
        self.treeview.heading("#0", text="")
        self.treeview.column("#0", width=0, stretch=tk.NO)
        self.treeview.heading("Project", text="Projekt")
        self.treeview.column("Project", anchor=tk.W)
        self.treeview.heading("Elapsed", text="Verstrichene Zeit")
        self.treeview.heading("Toggle", text="Start/Pause")
        self.treeview.heading("Note", text="Notiz")
        self.treeview.heading("Save", text="Speichern")
        self.treeview.heading("Remove", text="Entfernen")
        self.treeview.pack(fill=tk.BOTH, expand=True)

        self.load_stopwatches()

        self.treeview.bind("<Button-1>", self.on_treeview_click)

        self.add_stopwatch_button = ttk.Button(
            self, text="Stoppuhr hinzufügen", command=self.add_stopwatch_popup
        )
        self.add_stopwatch_button.pack()

    def load_stopwatches(self):
        for widget in self.treeview.get_children():
            self.treeview.delete(widget)

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
            self.create_stopwatch_item(stopwatch)

    def create_stopwatch_item(self, stopwatch):
        project_name = self.project_table.get_project(id=stopwatch.project_id).name
        item_id = self.treeview.insert(
            "",
            tk.END,
            values=(
                project_name,
                stopwatch.get_elapsed_time_str(),
                "Start",
                "",
                "Speichern",
                "Entfernen",
            ),
        )
        self.treeview.item(item_id, tags=("stopwatch",))

    def on_treeview_click(self, event):
        region = self.treeview.identify("region", event.x, event.y)
        if region == "separator":
            return

        item = self.treeview.identify_row(event.y)
        column = self.treeview.identify_column(event.x)
        stopwatch_index = self.treeview.index(item)
        stopwatch = self.stopwatches[stopwatch_index]

        if column == "#3":
            stopwatch.toggle()
            if self.treeview.item(item, "values")[2] == "Start":
                self.treeview.set(item, "Toggle", "Pause")
            else:
                self.treeview.set(item, "Toggle", "Start")
            self.update_elapsed_time(stopwatch, item)
        elif column == "#5":
            # Speichern-Logik hier
            self.save_stopwatch(stopwatch)
        elif column == "#6":
            self.remove_stopwatch(stopwatch.id)
            self.stopwatches.pop(stopwatch_index)
            self.treeview.delete(item)

    def update_elapsed_time(self, stopwatch, item):
        self.treeview.set(item, "Elapsed", stopwatch.get_elapsed_time_str())

    def save_stopwatch(self, stopwatch):
        self.stopwatch_table.update_stopwatch(stopwatch)

    def remove_stopwatch(self, stopwatch_id):
        self.stopwatch_table.delete_stopwatch(stopwatch_id)
        self.load_stopwatches()

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
        self.stopwatches.append(stopwatch)
        self.create_stopwatch_item(stopwatch)
