import tkinter as tk
from tkinter import ttk

import sv_ttk


class AppOverview(ttk.Frame):
    title = "Verfügbare Apps"

    def __init__(self, parent, APPS):
        super().__init__(parent)
        self.main_app = parent.master  # Save reference to the MainApp instance
        self.APPS = APPS
        self.create_widgets()

        # Set the initial background color for the category row
        theme_mode = "dark" if sv_ttk.get_theme() == "dark" else "light"
        self.update_category_row_bg(theme_mode)

    def create_widgets(self):
        self.table = ttk.Treeview(self, columns=("code", "name"), show="tree headings")
        self.table.heading("#0", text="Category")
        self.table.heading("code", text="Code")
        self.table.heading("name", text="App Name")

        # Configure tag for category row
        self.table.tag_configure("category", background="#333")

        self.populate_table()

        self.table.pack(expand=True, fill=tk.BOTH)

        # Add event bindings
        self.table.bind("<Double-1>", self.open_selected_app)
        self.table.bind("<Return>", self.open_selected_app)

    def populate_table(self, filter_text=""):
        # Clear table
        for item in self.table.get_children():
            self.table.delete(item)

        # Insert filtered apps
        filtered_apps = self.filter_apps(filter_text)

        for category, app_list in filtered_apps:
            category_item = self.table.insert(
                "", tk.END, text=category, tags=("category",)
            )
            for code, app_class in app_list:
                self.table.insert(category_item, tk.END, values=(code, app_class.title))
            self.table.item(category_item, open=True)  # Expand category item

        # Set column widths
        self.table.column("#0", width=50)
        self.table.column("code", width=50)
        self.table.column("name", width=200)

    def filter_apps(self, filter_text):
        filtered_apps = []

        for category, app_dict in self.APPS.items():
            filtered_category = [
                (code, app)
                for code, app in app_dict.items()
                if not filter_text or filter_text.lower() in app.title.lower()
            ]
            if filtered_category:
                filtered_apps.append((category, filtered_category))

        return filtered_apps

    def open_selected_app(self, event):
        selected_item = self.table.selection()
        if selected_item:
            item_values = self.table.item(selected_item, "values")
            app_code = item_values[0]
            app_class = None
            for apps in self.APPS.values():
                if app_code in apps:
                    app_class = apps.get(app_code)
                    break

            if app_class:
                self.main_app.load_app(
                    app_class
                )  # Use MainApp instance to load the selected app

    def update_category_row_bg(self, theme_mode):
        if theme_mode == "dark":
            self.table.tag_configure("category", background="#333")
        else:
            self.table.tag_configure("category", background="#bbb")

    def update_theme(self):
        pass
