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
                widget.update_theme()
