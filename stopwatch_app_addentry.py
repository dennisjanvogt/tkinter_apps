import tkinter as tk
from tkinter import ttk
from stopwatch_database import ProjectTable


class AddStopwatchPopup(tk.Toplevel):
    def __init__(self, parent, on_save_callback):
        super().__init__(parent)

        self.parent = parent
        self.on_save_callback = on_save_callback

        self.title("Stoppuhr hinzufügen")
        self.geometry("300x200")

        self.project_table = ProjectTable()

        self.create_widgets()
        self.load_projects()

    def create_widgets(self):
        self.project_frame = ttk.Frame(self)
        self.project_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=25)

        self.project_label = ttk.Label(self.project_frame, text="Projekt auswählen:")
        self.project_label.pack(pady=5, anchor="center")

        self.project_combobox = ttk.Combobox(
            self.project_frame, values=[], state="readonly"
        )
        self.project_combobox.pack(pady=5, anchor="center")

        self.save_button = ttk.Button(
            self.project_frame, text="Stoppuhr hinzufügen", command=self.save_stopwatch
        )
        self.save_button.pack(pady=5, anchor="center")

        # prevent the frame from resizing based on its contents
        self.project_frame.pack_propagate(0)

    def load_projects(self):
        projects = self.project_table.get_all_projects()
        project_names = [project.name for project in projects]
        self.project_combobox["values"] = project_names
        if project_names:
            self.project_combobox.set(project_names[0])

    def save_stopwatch(self):
        selected_project_name = self.project_combobox.get()
        if selected_project_name:
            project = self.project_table.get_project_by_name(selected_project_name)
            self.on_save_callback(project.id)
            self.destroy()


class StopwatchWidget(ttk.Frame):
    def __init__(self, parent, stopwatch, on_remove_callback):
        super().__init__(parent)

        self.stopwatch = stopwatch
        self.on_remove_callback = on_remove_callback

        self.project_frame = ttk.Frame(self)
        self.project_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.project_label = ttk.Label(
            self.project_frame, text=f"Projekt: {stopwatch.project_id}"
        )
        self.project_label.pack(side=tk.LEFT, padx=5, pady=5, anchor="center")

        self.elapsed_time_label = ttk.Label(self.project_frame, text="00:00:00")
        self.elapsed_time_label.pack(side=tk.LEFT, padx=5, pady=5, anchor="center")

        self.start_pause_button = ttk.Button(
            self.project_frame, text="Start", command=self.toggle
        )
        self.start_pause_button.pack(side=tk.LEFT, padx=5, pady=5, anchor="center")

        self.save_button = ttk.Button(
            self.project_frame, text="Speichern", command=self.save_time
        )
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5, anchor="center")

        self.remove_button = ttk.Button(
            self.project_frame, text="Entfernen", command=self.remove
        )
        self.remove_button.pack(side=tk.LEFT, padx=5, pady=5, anchor="center")

        # prevent the frame from resizing based on its contents
        self.project_frame.pack_propagate(0)
