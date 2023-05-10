from tkinter import ttk
import tkinter as tk
import re

from .stopwatch_database import EntryTable, ProjectTable


class EditEntryDialog(tk.Toplevel):
    def __init__(self, parent, entry_id, project, time, note):
        super().__init__(parent)

        self.entry_db_instance = EntryTable()
        self.project_db_instance = ProjectTable()
        project_name = self.project_db_instance.get_project(id=project).name

        self.entry_id = entry_id
        self.title("Eintrag bearbeiten")
        self.geometry("430x200")
        self.resizable(False, False)

        # Configure columns and rows to be responsive
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

        ttk.Label(self, text="Projekt:").grid(
            row=0, column=0, padx=10, pady=10, sticky=tk.E + tk.W
        )
        self.project_entry = ttk.Label(self, text=project_name)
        self.project_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.E + tk.W)

        ttk.Label(self, text="Zeit:").grid(
            row=1, column=0, padx=10, pady=10, sticky=tk.E + tk.W
        )
        self.time_entry = ttk.Entry(self)
        self.time_entry.insert(0, time)
        self.time_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.E + tk.W)

        ttk.Label(self, text="Notiz:").grid(
            row=2, column=0, padx=10, pady=10, sticky=tk.E + tk.W
        )
        self.note_entry = ttk.Entry(self)
        self.note_entry.insert(0, note)
        self.note_entry.grid(row=2, column=1, padx=10, pady=10, sticky=tk.E + tk.W)

        save_button = ttk.Button(self, text="Speichern", command=self.save_entry)
        save_button.grid(row=3, columnspan=2, pady=10, sticky=tk.E + tk.W)

        self.error_label = ttk.Label(self, text="", foreground="red")
        self.error_label.grid(row=4, columnspan=2)

    def save_entry(self):
        time = self.time_entry.get()
        note = self.note_entry.get()

        if not self.validate_time_format(time):
            self.error_label[
                "text"
            ] = "Ungültiges Zeitformat. Bitte verwenden Sie das Format hh:mm:ss."
            return

        self.entry_db_instance.update_entry(self.entry_id, time=time, note=note)  # TODO
        self.master.load_entries()
        self.destroy()

    @staticmethod
    def validate_time_format(time_str):
        pattern = re.compile(r"^\d{2}:\d{2}:\d{2}$")
        return bool(pattern.match(time_str))
