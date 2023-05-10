import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from .stopwatch_database import ProjectTable
from .database_tables import Entrys, Session_Stopwatch
from .edit_entry_dialog import EditEntryDialog


class ViewEntrysApp(ttk.Frame):
    title = "Stopwatcheintrag anzeigen"

    def __init__(self, parent, *args):
        super().__init__(parent)

        self.session = Session_Stopwatch()
        self.project_db_instance = ProjectTable()

        self.entry_tree = ttk.Treeview(
            self, columns=("Projekt", "Zeit", "Notiz"), show="headings"
        )
        self.entry_tree.heading("Projekt", text="Projekt")
        self.entry_tree.heading("Zeit", text="Zeit")
        self.entry_tree.heading("Notiz", text="Notiz")
        self.entry_tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.load_entries()

        self.entry_tree.bind("<Double-1>", self.on_double_click)

        edit_button = ttk.Button(
            self, text="Eintrag bearbeiten", command=self.edit_entry
        )
        edit_button.pack(side=tk.LEFT, padx=(10, 5), pady=(0, 10))

        delete_button = ttk.Button(
            self, text="Eintrag löschen", command=self.delete_entry
        )
        delete_button.pack(side=tk.RIGHT, padx=(5, 10), pady=(0, 10))

    def load_entries(self):
        for i in self.entry_tree.get_children():
            self.entry_tree.delete(i)

        for entry in self.session.query(Entrys).all():
            project_name = self.project_db_instance.get_project(
                id=entry.project_id
            ).name
            self.entry_tree.insert(
                "",
                tk.END,
                iid=entry.id,
                values=(project_name, entry.time, entry.note),  # Änderung hier
            )

    def edit_entry(self):
        entry_id = self.entry_tree.selection()[0]
        entry = self.entry_tree.item(entry_id)

        project_name, time, note = entry["values"]
        project_id = self.project_db_instance.get_project_id_by_name(
            project_name
        )  # Get project_id by project_name
        edit_dialog = EditEntryDialog(self, entry_id, project_id, time, note)
        self.wait_window(edit_dialog)  # Wait until the edit dialog window is closed
        self.load_entries()  # Refresh the customer list

    def delete_entry(self):
        entry_id = self.entry_tree.selection()[0]

        response = messagebox.askyesno(
            title="Eintrag löschen",
            message="Möchten Sie diesen Eintrag wirklich löschen?",
        )
        if response:
            self.session.query(Entrys).filter(Entrys.id == entry_id).delete()
            self.session.commit()
            self.load_entries()

    def on_double_click(self, event):
        self.edit_entry()
