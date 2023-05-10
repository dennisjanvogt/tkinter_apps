import tkinter as tk
from tkinter import ttk

class AppFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def update_theme(self):
        for widget in self.winfo_children():
            if isinstance(widget, (ttk.Widget, AppFrame)):
                try:
                    widget.update_theme()
                except AttributeError as attribute_error:
                    print("Update could not be updated. Reason: " + attribute_error)
