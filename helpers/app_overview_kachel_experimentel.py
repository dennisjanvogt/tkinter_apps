import tkinter as tk
from tkinter import font


class AppOverview(tk.Frame):
    title = "Verfügbare Apps"

    def __init__(self, parent, APPS):
        super().__init__(parent)
        self.main_app = parent.master  # Save reference to the MainApp instance
        self.APPS = APPS

        self.create_category_buttons()
        self.create_app_buttons()

    def create_category_buttons(self):
        self.category_frame = tk.Frame(self)
        self.category_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        category_colors = {
            "Adressbuch (AB)": "#080706",
            "Ivy App (ERP)": "#EFEFEF",
            "Stopwatch": "#D1B280",
        }

        for category, color in category_colors.items():
            button = tk.Canvas(
                self.category_frame,
                width=100,
                height=50,
                bg=color,
                highlightthickness=0,
            )
            button.bind(
                "<Button-1>",
                lambda event, cat=category: self.on_click(event, category=cat),
            )
            button.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
            button.create_text(
                50, 25, text=category, fill="white", font=("Arial", 13), anchor="center"
            )

    def create_app_buttons(self):
        self.app_frame = tk.Frame(self)
        self.app_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.app_buttons = {}
        app_colors = {
            "AB_KA": "#080706",
            "AB_KS": "#080706",
            "ERP_CA": "#EFEFEF",
            "ERP_PA": "#EFEFEF",
            "ERP_OA": "#EFEFEF",
            "ERP_VCA": "#EFEFEF",
            "ERP_VPA": "#EFEFEF",
            "ERP_VOA": "#EFEFEF",
            "SW_USE": "#D1B280",
            "SW_VIEW": "#D1B280",
        }

        for category, app_dict in self.APPS.items():
            category_frame = tk.Frame(self.app_frame)
            self.app_buttons[category] = category_frame
            for code, app_class in app_dict.items():
                button = tk.Canvas(
                    category_frame,
                    width=100,
                    height=50,
                    bg=app_colors[code],
                    highlightthickness=0,
                )
                button.bind(
                    "<Button-1>",
                    lambda event, app=app_class: self.on_click(event, app=app_class),
                )
                button.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

                # Measure the text width and center it horizontally
                font_obj = font.Font(family="Arial", size=13)
                text_width = font_obj.measure(app_class.title)
                x_position = 50 - text_width / 2

                button.create_text(
                    x_position,
                    25,
                    text=app_class.title,
                    fill="white",
                    font=("Arial", 13),
                    anchor="center",
                )

    def on_click(self, event, category=None, app=None):
        if category:
            self.display_apps(category)
        elif app:
            self.main_app.load_app(app)

    def display_apps(self, category):
        for frame in self.app_buttons.values():
            frame.pack_forget()

        if category in self.app_buttons:
            self.app_buttons[category].pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def on_click(self, event, category=None, app=None):
        if category:
            self.display_apps(category)
        elif app:
            self.main_app.load_app(app)

    def display_apps(self, category):
        for frame in self.app_buttons.values():
            frame.pack_forget()

        if category in self.app_buttons:
            self.app_buttons[category].pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
