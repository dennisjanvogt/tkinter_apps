from Levenshtein import distance
import sv_ttk

import tkinter as tk
from tkinter import ttk, font
from ttkthemes import ThemedTk
from app_frame import AppFrame
from adress_bock_app.contact_app import ContactApp
from adress_bock_app.view_contacts_app import ViewContactApp
from app_overview import AppOverview
from ivy_app.create_customer_app import CreateCustomerApp
from ivy_app.create_order_app import CreateOrderApp
from ivy_app.create_product_app import CreateProductApp

APPS = {
    "Adressbuch (AB)": {
        "AB_KA": ContactApp,
        "AB_KS": ViewContactApp,
    },
    "Ivy App (ERP)": {
        "ERP_CA": CreateCustomerApp,
        "ERP_PA": CreateProductApp,
        "ERP_OA": CreateOrderApp,
    },
}


class MainApp(ThemedTk):
    def __init__(self):
        super().__init__()

        self.bind("<Escape>", self.load_app_overview)

        sv_ttk.set_theme("dark")

        self.title("VQ13")
        self.geometry("1200x700")

        self.current_app = None

        self.top_frame = ttk.Frame(self)
        self.top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self.transaction_label = ttk.Label(self.top_frame, text="Transaktion")
        self.transaction_label.pack(side=tk.LEFT, padx=(5, 20))

        self.app_entry_var = tk.StringVar()
        self.app_entry = ttk.Entry(self.top_frame, textvariable=self.app_entry_var)
        self.app_entry.bind("<Return>", self.open_app)
        self.app_entry.pack(side=tk.LEFT, padx=(0, 20))
        self.app_entry_var.trace("w", self.update_app_overview)

        self.app_title_font = font.Font(size=16)
        self.app_title = ttk.Label(self.top_frame, text="", font=self.app_title_font)
        self.app_title.pack(side=tk.LEFT, padx=(0, 20), expand=True, anchor="center")

        self.logo_font = font.Font(family="Helvetica", size=18, weight="bold")
        self.logo_label = ttk.Label(self.top_frame, text="NoSAP", font=self.logo_font)
        self.logo_label.pack(side=tk.RIGHT, padx=(20, 5))

        self.separator = ttk.Separator(self, orient="horizontal")
        self.separator.pack(side=tk.TOP, fill=tk.X, pady=(5, 10))

        self.app_frame = AppFrame(self)
        self.app_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.bottom_frame = ttk.Frame(self)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

        self.theme_switch_var = tk.BooleanVar(value=True)
        self.theme_switch = ttk.Checkbutton(
            self.bottom_frame,
            text="Dark Mode",
            variable=self.theme_switch_var,
            command=self.toggle_theme,
        )
        self.theme_switch.pack(side=tk.BOTTOM, anchor="se", pady=5, padx=5)

        self.load_app(AppOverview)

    def open_app(self, event):
        app_name = self.app_entry.get().strip()
        closest_app_name = min(APPS.keys(), key=lambda x: distance(x, app_name))
        self.app_entry.delete(0, tk.END)
        self.load_app(APPS[closest_app_name])

    def load_app(self, app_class):
        self.app_frame.clear()
        self.app_title.config(text=app_class.title)
        app_instance = app_class(self.app_frame, APPS)
        app_instance.pack(fill=tk.BOTH, expand=True)
        self.app_frame.current_app = app_instance

    def update_app_overview(self, *args):
        filter_text = self.app_entry_var.get()
        if isinstance(self.app_frame.current_app, AppOverview):
            self.app_frame.current_app.populate_table(filter_text)

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.current_app = None

    def load_app_overview(self, event=None):
        self.load_app(AppOverview)

    def toggle_theme(self):
        current_theme = sv_ttk.get_theme()
        if current_theme == "dark":
            sv_ttk.set_theme("light")
        else:
            sv_ttk.set_theme("dark")
        self.reload_theme()

    def reload_theme(self):
        for widget in self.winfo_children():
            if isinstance(widget, ttk.Widget) and hasattr(widget, "update_theme"):
                widget.update_theme()
            if isinstance(widget, AppFrame) and isinstance(
                widget.current_app, AppOverview
            ):
                theme_mode = "dark" if sv_ttk.get_theme() == "dark" else "light"
                widget.current_app.update_category_row_bg(theme_mode)
                if hasattr(widget.current_app, "update_theme"):
                    widget.current_app.update_theme()


app = MainApp()
app.mainloop()
