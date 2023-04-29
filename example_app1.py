import tkinter as tk
from tkinter import ttk

class ExampleApp1(ttk.Frame):
    title = "Beispiel-App 1"

    def __init__(self, parent):
        super().__init__(parent)

        label = ttk.Label(self, text="Willkommen bei Beispiel-App 1!")
        label.pack()
