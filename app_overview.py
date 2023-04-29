from tkinter import ttk
import tkinter as tk


class AppOverview(ttk.Frame):
    title = "Verfügbare Apps"

    def __init__(self, parent, APPS):
        super().__init__(parent)
        self.main_app = parent.master  # Referenz auf die MainApp-Instanz speichern
        self.APPS = APPS
        self.create_widgets()

    def create_widgets(self):
        self.table = ttk.Treeview(self, columns=("code", "name"), show="headings")
        self.table.heading("code", text="Code")
        self.table.heading("name", text="App Name")

        self.populate_table()

        self.table.pack(expand=True, fill=tk.BOTH)

        # Event-Bindungen hinzufügen
        self.table.bind("<Double-1>", self.open_selected_app)
        self.table.bind("<Return>", self.open_selected_app)

    def populate_table(self, filter_text=""):
        # Tabelle leeren
        for item in self.table.get_children():
            self.table.delete(item)

        # Gefilterte Apps einfügen
        filtered_apps = self.filter_apps(filter_text)
        for code, app_class in filtered_apps:
            self.table.insert("", tk.END, values=(code, app_class.title))

    def filter_apps(self, filter_text):
        if not filter_text:
            return self.APPS.items()

        return [(code, app) for code, app in self.APPS.items() if filter_text.lower() in app.title.lower()]


    def open_selected_app(self, event):
        selected_item = self.table.selection()
        if selected_item:
            item_values = self.table.item(selected_item, "values")
            app_code = item_values[0]
            app_class = self.APPS.get(app_code)

            if app_class:
                self.main_app.load_app(app_class)  # MainApp-Instanz verwenden, um die ausgewählte App zu laden
