import os
from levenshtein_distance import Levenshtein
import sv_ttk
import tkinter as tk
from tkinter import PhotoImage, ttk, font
from ttkthemes import ThemedTk

from helpers.app_frame import AppFrame
from helpers.app_overview import AppOverview

from apps.adress_book.add_contact import ContactApp
from apps.adress_book.view_contacts import ViewContactApp

from apps.ivy_erp.add_customer import CreateCustomerApp
from apps.ivy_erp.add_order import CreateOrderApp
from apps.ivy_erp.add_product import CreateProductApp
from apps.ivy_erp.view_customers import ViewCustomersApp
from apps.ivy_erp.view_orders import ViewOrdersApp
from apps.ivy_erp.view_products import ViewProductsApp

from apps.stopwatch.stopwatch_app import StopwatchApp


APPS = {
    "Adressbuch (AB)": {
        "AB_KA": ContactApp,
        "AB_KS": ViewContactApp,
    },
    "Ivy App (ERP)": {
        "ERP_CA": CreateCustomerApp,
        "ERP_PA": CreateProductApp,
        "ERP_OA": CreateOrderApp,
        "ERP_VCA": ViewCustomersApp,
        "ERP_VPA": ViewProductsApp,
        "ERP_VOA": ViewOrdersApp,
    },
    "Stopwatch": {
        "SW_USE": StopwatchApp,
    },
}

APPS_NAMES = {
    "AB_KA": ContactApp,
    "AB_KS": ViewContactApp,
    "ERP_CA": CreateCustomerApp,
    "ERP_PA": CreateProductApp,
    "ERP_OA": CreateOrderApp,
    "ERP_VCA": ViewCustomersApp,
    "ERP_VPA": ViewProductsApp,
    "ERP_VOA": ViewOrdersApp,
    "SW": StopwatchApp,
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

        self.logo_image = PhotoImage(file="helpers/LOGO.png").subsample(2, 2)
        self.logo_label = ttk.Label(self.top_frame, image=self.logo_image)
        self.logo_label.pack(side=tk.RIGHT, padx=(20, 5))

        self.iconphoto(False, self.logo_image)

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
        closest_app_name = min(
            APPS_NAMES.keys(),
            key=lambda x: Levenshtein(APPS_NAMES[x].title, app_name).distance(),
        )
        app_class = APPS_NAMES[closest_app_name]
        self.app_entry.delete(0, tk.END)
        self.load_app(app_class)

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
        self.app_entry.delete(0, tk.END)
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
