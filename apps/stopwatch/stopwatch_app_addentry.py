import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from .stopwatch_database import ProjectTable


class AddStopwatchPopup(tk.Toplevel):
    def __init__(self, parent, on_save_callback):
        super().__init__(parent)

        self.parent = parent
        self.on_save_callback = on_save_callback

        self.title("Stoppuhr hinzufügen")
        self.geometry("510x400")

        self.project_table = ProjectTable()

        self.create_widgets()
        self.load_projects()

    def create_widgets(self):
        self.project_frame = ttk.Frame(self)
        self.project_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.filter_label = ttk.Label(self.project_frame, text="Filter:")
        self.filter_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        self.filter_entry = ttk.Entry(self.project_frame)
        self.filter_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.filter_entry.bind("<KeyRelease>", self.on_filter_change)

        self.tree = ttk.Treeview(self.project_frame)
        self.tree["columns"] = ("#1",)
        self.tree.heading("#0", text=" Projekt", anchor="w")
        self.tree.column("#0", anchor="w", width=100)
        self.tree.heading("#1", text=" Beschreibung", anchor="w")
        self.tree.column("#1", anchor="w", width=350)

        self.scrollbar = ttk.Scrollbar(
            self.project_frame, orient="vertical", command=self.tree.yview
        )
        self.scrollbar.grid(row=1, column=2, padx=(0, 5), pady=5, sticky="ns")
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.tree.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.bind("<Return>", self.on_double_click)

        self.save_button = ttk.Button(
            self.project_frame,
            text="Stoppuhr hinzufügen",
            command=self.save_stopwatch,
        )
        self.save_button.grid(row=2, column=0, padx=5, pady=5, sticky="w")

    def load_projects(self):
        self.projects = self.project_table.get_all_projects()
        for project in self.projects:
            self.tree.insert(
                "", "end", text=project.name, values=(project.description, project.id)
            )

    def on_double_click(self, event=None):
        selected_item = self.tree.selection()
        if selected_item:
            project_id = int(self.tree.item(selected_item[0], "values")[1])
            self.on_save_callback(project_id)
            self.destroy()

    def save_stopwatch(self):
        selected_item = self.tree.selection()
        if selected_item:
            project_id = int(self.tree.item(selected_item[0], "values")[0])
            self.on_save_callback(project_id)
            self.destroy()
        else:
            messagebox.showerror("Fehler", "Bitte wählen Sie ein Projekt aus.")

    def on_filter_change(self, event):
        filter_value = self.filter_entry.get().lower()
        if len(filter_value.strip()) > 0:
            filtered_projects = [
                project
                for project in self.projects
                if filter_value in project.name.lower()
            ]
        else:
            filtered_projects = self.projects

        self.tree.delete(*self.tree.get_children())

        for project in filtered_projects:
            self.tree.insert(
                "", "end", text=project.name, values=(project.description, project.id)
            )


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
